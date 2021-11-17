"""基于redis队列，使用pickle进行序列化，不支持跨语言"""
import asyncio
import time

from ratelimit.base.constants import LimitConfig
from ratelimit.base.tools import encode_serialize, get_redis_connection, decode_serialize
from ratelimit.limits.redis_limit import RedisRateLimit
from ratelimit.queue_tools.base import BaseQueue


class RedisQueueTools(BaseQueue):
    """redis队列工具类"""

    queue_key = f'{LimitConfig.service}:limit:queue'
    queue_type = 'redis'

    async def add_item(self, item):
        """
        加入队列，使用定时队列处理
        :param item: 这里队列的格式如下：
            {
                "func": func
                "func_args": [],
                "func_kwargs": {},
                "limit_config": {},
                "delay": 3
            }
        """
        delay = int(item.get('delay') or 0)
        score = int(time.time()) + delay
        conn = await get_redis_connection()
        item['score'] = score
        await conn.zadd(
            key=self.queue_key,
            score=score,
            member=encode_serialize(item)
        )

    async def get_item(self):
        """
        获取队列信息，这里会返回多条数据
        :return:
        """
        conn = await get_redis_connection()
        min_score = 0
        max_score = time.time()

        pl = conn.pipeline()
        pl.zrangebyscore(
            key=self.queue_key,
            min=min_score,
            max=max_score
        )
        pl.zremrangebyscore(self.queue_key, min=min_score, max=max_score)
        item_list, _ = await pl.execute()
        return item_list

    async def _consume(self):
        """消费队列"""
        while True:
            item_list = await self.get_item()
            if not item_list:
                await asyncio.sleep(1)
                continue

            for obj_str in item_list:
                item = decode_serialize(obj_str)
                if not item:
                    continue

                func = item.get('func')
                func_args = item.get('func_args')
                func_kwargs = item.get('func_kwargs')
                limit_config = item.get('limit_config')
                key_name = limit_config.get('key_name')

                # 这里也要判断是否超限
                result, _ = await RedisRateLimit().attempt_get_token(key_name, limit_config)
                if not result:
                    # 若再次被限制时，延时执行时间修改为limit_delay
                    handle_params = limit_config.get('handle_params') or {}
                    item['delay'] = handle_params.get('limit_delay') or 0
                    await self.add_item(item)
                    continue

                await func(*func_args, **func_kwargs)
                await asyncio.sleep(0)
