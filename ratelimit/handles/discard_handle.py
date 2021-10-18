from ratelimit.base.errors import NotDefaultValueError
from ratelimit.handles.base import BaseHandle


class DiscardHandle(BaseHandle):
    """丢弃处理"""
    handle_key = 'discard'

    def execute(self):
        """直接返回默认值"""
        if self.default_return is None:
            raise NotDefaultValueError('缺少默认返回值')
        return self.default_return
