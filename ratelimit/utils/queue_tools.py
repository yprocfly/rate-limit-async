import threading
from asyncio import Queue


class QueueTools:
    """队列工具类"""

    _queue = None
    _has_thread = False

    def __init__(self):
        self._queue = Queue()

    async def add(self, item):
        """
        加入队列
        :param item: 这里队列的格式如下：
            {
                "func": func
                "func_args": [],
                "func_kwargs": {},
                "limit_config": {},
                "limit_cls": RedisRateLimit
            }
        """
        await self._queue.put(item)

    async def get(self):
        """获取队列信息"""
        return await self._queue.get() or {}

    async def _consume(self):
        """消费队列【内存队列，这里可能会存在任务丢失的情况】"""
        while True:
            item = await self.get()
            if not item:
                continue

            func = item.get('func')
            func_args = item.get('func_args')
            func_kwargs = item.get('func_kwargs')
            limit_config = item.get('limit_config')
            limit_cls = item.get('limit_cls')
            key_name = limit_config.get('key_name')

            # 这里也要判断是否超限
            result, _ = await limit_cls().attempt_get_token(key_name, limit_config)
            if not result:
                continue

            await func(*func_args, **func_kwargs)

    async def execute(self):
        """起一个永久线程消费"""
        if not self._has_thread:
            self._has_thread = True
            task = threading.Thread(target=self.execute)
            task.start()
