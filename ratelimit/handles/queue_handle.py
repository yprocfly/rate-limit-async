from ratelimit.queue_tools import QueueFactory
from ratelimit.handles.base import BaseHandle


class QueueHandle(BaseHandle):
    """排队处理"""
    handle_key = 'queue'

    async def execute(self):
        """
        排队处理，配置信息 self.handle_params 格式如下：
            {
                "delay": 3,             # 延时执行时间，单位【秒】
                "limit_delay": 1,         # 执行再次被限制的情况下，延迟执行时间，单位【秒】
                "queue_type": "redis",  # 队列类型：redis、local
            }
        """
        func_args = self._get_func_args()
        func_kwargs = self._get_func_kwargs()
        handle_params = self._get_handle_params()

        queue_type = handle_params.get('queue_type') or 'local'
        delay = handle_params.get('delay') or 0

        item = {
            'func': self.func,
            'func_args': func_args,
            'func_kwargs': func_kwargs,
            'limit_config': self.limit_config,
            'delay': delay
        }

        queue_cls = QueueFactory().get_queue_cls(queue_type)
        await queue_cls().add_item(item)
