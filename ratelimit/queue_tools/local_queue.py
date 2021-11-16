"""基于本地队列，可能会出现数据丢失的问题"""
import asyncio
from asyncio import Queue

from ratelimit.limits.redis_limit import RedisRateLimit
from ratelimit.queue_tools.base import BaseQueue


class LocalQueueTools(BaseQueue):
    """本地内存队列工具类"""

    _queue = None
    queue_type = 'local'

    def __init__(self):
        self._queue = Queue()
        super().__init__()

    async def add_item(self, item):
        """
        加入队列
        :param item: 这里队列的格式如下：
            {
                "func": func
                "func_args": [],
                "func_kwargs": {},
                "limit_config": {},
                "delay": 3
            }
        """
        await self._queue.put(item)

    async def get_item(self):
        """获取队列信息"""
        return await self._queue.get() or {}

    async def _consume(self):
        """消费队列【内存队列，这里可能会存在任务丢失的情况】"""
        item = await self.get_item()
        if not item:
            await asyncio.sleep(1)
            return await self._consume()

        func = item.get('func')
        func_args = item.get('func_args')
        func_kwargs = item.get('func_kwargs')
        limit_config = item.get('limit_config')
        key_name = limit_config.get('key_name')

        # 这里也要判断是否超限
        result, _ = await RedisRateLimit().attempt_get_token(key_name, limit_config)
        if not result:
            return await self._consume()

        await func(*func_args, **func_kwargs)
        await asyncio.sleep(0)
        return await self._consume()


