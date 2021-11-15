from ratelimit.base.base_decorators import singleton
from ratelimit.base.errors import NotDefineHandleError, NotAllowHandleError
from ratelimit.queue_tools.base import BaseQueue
from ratelimit.queue_tools.local_queue import LocalQueueTools
from ratelimit.queue_tools.redis_queue import RedisQueueTools


@singleton
class QueueFactory:
    """队列工厂类"""
    queue_dict = {}

    def __init__(self):
        self._register(LocalQueueTools)
        self._register(RedisQueueTools)

    def _register(self, queue_cls):
        """把队列方法注册进来"""
        if not issubclass(queue_cls, BaseQueue):
            raise NotAllowHandleError(f'队列类【{queue_cls}】不允许注册')

        self.queue_dict[queue_cls.queue_type] = queue_cls

    def get_queue_cls(self, queue_type):
        """获取真正的队列类"""
        queue_cls = self.queue_dict.get(queue_type)
        if not queue_cls:
            raise NotDefineHandleError(f'未定义【{queue_type}】的队列类')

        return queue_cls
