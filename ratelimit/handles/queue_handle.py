from ratelimit.utils.queue_tools import QueueTools
from ratelimit.handles.base import BaseHandle


class QueueHandle(BaseHandle):
    """排队处理"""
    handle_key = 'queue'
    queue_tools = QueueTools()

    async def execute(self):
        """排队处理"""
        item = {
            'func': self.func,
            'func_args': self._get_func_args(),
            'func_kwargs': self._get_func_kwargs(),
            'limit_config': self.limit_config,
            'limit_cls': self.limit_cls
        }
        await self.queue_tools.add(item)
