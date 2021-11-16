"""队列操作基础类"""
import asyncio

from ratelimit.base.base_decorators import singleton


@singleton
class BaseQueue:
    _has_thread = False

    def __init__(self):
        self._create_task()

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
        raise NotImplementedError('未定义【add_item】方法')

    async def get_item(self):
        """获取队列信息"""
        raise NotImplementedError('未定义【get_item】方法')

    async def _consume(self):
        """消费队列"""
        raise NotImplementedError('未定义【_consume】方法')

    def _create_task(self):
        """起一个协程消费"""
        if not self._has_thread:
            self._has_thread = True
            # 将消费函数函数注册到 event_loop 上
            _loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(self._consume(), _loop)
