from ratelimit.base.base_decorators import singleton
from ratelimit.base.errors import NotDefineHandleError, NotAllowHandleError
from ratelimit.handles.base import BaseHandle
from ratelimit.handles.discard_handle import DiscardHandle
from ratelimit.handles.queue_handle import QueueHandle
from ratelimit.handles.retry_handle import RetryHandle


@singleton
class HandleFactory:
    """处理工厂类"""
    handle_dict = {}

    def __init__(self):
        self._register(DiscardHandle)
        self._register(QueueHandle)
        self._register(RetryHandle)

    def _register(self, handle_cls):
        """把处理方法注册进来"""
        if not issubclass(handle_cls, BaseHandle):
            raise NotAllowHandleError(f'处理类【{handle_cls}】不允许注册')

        self.handle_dict[handle_cls.handle_key] = handle_cls

    def get_handle_cls(self, handle_key):
        """获取真正的处理类"""
        handle_cls = self.handle_dict.get(handle_key)
        if not handle_cls:
            raise NotDefineHandleError(f'未定义【{handle_key}】的处理类')

        return handle_cls
