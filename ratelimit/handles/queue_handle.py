from ratelimit.handles.base import BaseHandle


class QueueHandle(BaseHandle):
    """排队处理"""
    handle_key = 'queue'

    def execute(self):
        """排队处理，支持两种方式：同步等待结果or异步处理"""
        ...
