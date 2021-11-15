"""队列操作基础类"""
import threading

from ratelimit.base.base_decorators import singleton


@singleton
class BaseQueue:
    _has_thread = False

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

    async def execute(self):
        """起一个永久线程消费"""
        if not self._has_thread:
            self._has_thread = True
            await self._consume()
            # task = threading.Thread(target=self._consume)
            # task.start()
