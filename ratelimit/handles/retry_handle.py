import asyncio

from ratelimit.base.errors import NotDefaultValueError
from ratelimit.handles.base import BaseHandle
from ratelimit.limits.redis_limit import RedisRateLimit


class RetryHandle(BaseHandle):
    """流量超限做重试处理"""
    handle_key = 'retry'

    async def execute(self):
        """
        重试处理，配置信息 self.handle_params 格式如下：
            {
                "retry_count"：3,    # 重试次数
                "retry_wait": 0,     # 每次重试间隔，默认不等待，单位【秒】
                "current_count": 0,  # 当前已重试几次
            }
        """
        func_args = self._get_func_args()
        func_kwargs = self._get_func_kwargs()
        handle_params = self._get_handle_params()
        key_name = self._get_key_name()

        current_count = 0
        retry_count = handle_params.get('retry_count') or 1
        retry_wait = handle_params.get('retry_wait') or 0
        while current_count < retry_count:
            await asyncio.sleep(retry_wait)
            # 这里也要判断是否超限
            result, _ = await RedisRateLimit().attempt_get_token(key_name, self.limit_config)
            if not result:
                current_count += 1
                continue
            return await self.func(*func_args, **func_kwargs)

        # 重试失败，则返回默认值
        if self.default_return is None:
            raise NotDefaultValueError('重试失败，缺少默认返回值')
        return self.default_return
