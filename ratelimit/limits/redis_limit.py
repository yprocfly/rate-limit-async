"""基于redis-cell的流量控制器"""
import asyncio
import logging
import traceback

import ujson as json

from ratelimit.base.base_decorators import singleton
from ratelimit.base.constants import LimitConfig
from ratelimit.base.tools import get_redis_connection

logger = logging.getLogger(__name__)


@singleton
class RedisRateLimit:

    async def get_limit_config(self, key_name):
        """
        获取key对应的配置【直接把限流配置信息存在redis中，直接获取】
        :param key_name: redis键名
        :return: 限流配置，如果是用了redis的配置【使用hash类型】，在redis中的存储格式如下
            "service": {
                "key_name": {
                    "total_quota": 100,          # 令牌桶大小
                    "limit_second": 10,          # 生成令牌的单位时间
                    "limit_quota": 3,            # 单位时间内生成的令牌数量
                    "once_quota": 1,             # 每次请求消费的令牌数量
                    "handle": "discard",         # discard丢弃；queue排队；retry重试
                    "handle_params": {},         # 处理方式对应的参数
                }
            }
        """
        limit_config = LimitConfig.rate_limit_config.get(key_name) or {}
        if LimitConfig.use_redis:
            conn = await get_redis_connection()
            limit_config = json.loads(await conn.hget(LimitConfig.service, key_name) or '{}')

        limit_config['service'] = LimitConfig.service
        limit_config['key_name'] = key_name
        limit_config['total_quota'] = limit_config.get('total_quota') or LimitConfig.total_quota
        limit_config['limit_quota'] = limit_config.get('limit_quota') or LimitConfig.limit_quota
        limit_config['limit_second'] = limit_config.get('limit_second') or LimitConfig.limit_second
        limit_config['once_quota'] = limit_config.get('once_quota') or LimitConfig.once_quota
        limit_config['handle'] = limit_config.get('handle') or LimitConfig.default_handle
        limit_config['handle_params'] = limit_config.get('handle_params') or LimitConfig.default_handle_params

        return limit_config

    async def attempt_get_token(self, key_name, limit_config=None):
        """
        尝试获取令牌，如果获取成功，返回true，代表可访问；
        :param key_name: redis键名
        :param limit_config: 配置信息，不传则从redis中获取
        :return: (bool, dict) -> (是否允许通过, 限流配置信息)
        """
        try:
            if not limit_config:
                limit_config = await self.get_limit_config(key_name)

            total_quota = limit_config.get('total_quota') or LimitConfig.total_quota
            limit_quota = limit_config.get('limit_quota') or LimitConfig.limit_quota
            limit_second = limit_config.get('limit_second') or LimitConfig.limit_second
            once_quota = limit_config.get('once_quota') or LimitConfig.once_quota

            conn = await get_redis_connection()
            result = await conn.execute(
                'CL.THROTTLE',
                f'{LimitConfig.service}:{key_name}',
                total_quota,
                limit_quota,
                limit_second,
                once_quota
            )
            logger.debug(f'* limit result【{LimitConfig.service} - {key_name}】', result)
            return result[0] == 0, limit_config
        except Exception as err:
            # 出现报错直接允许【高可用】
            logger.warning(f'尝试获取令牌出错：{traceback.format_exc()}')
            return True, {}


if __name__ == '__main__':
    redis_rate_limit = RedisRateLimit()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(redis_rate_limit.attempt_get_token('key_name'))
    print(loop.run_until_complete(task))
