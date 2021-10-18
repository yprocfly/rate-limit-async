
class LimitError(Exception):
    """限流器出错"""


class NotDefaultValueError(LimitError):
    """缺少默认返回值"""


class LackParamsError(LimitError):
    """缺少参数信息"""


class NotAllowHandleError(LimitError):
    """不是一个允许的处理类"""


class NotDefineHandleError(LimitError):
    """未定义处理类"""
