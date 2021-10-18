"""一些装饰器"""
from ratelimit.utils.over_limit_handle import OverLimitHandle


def async_rate_limit(key_name, default_return=None):
    """
    异步方法限流装饰器
    :param key_name: 键名，必传，理论上同一个系统中要唯一
    :param default_return: 默认返回值，不传则会抛出异常
    """
    class RateLimitDecorator:
        def __init__(self, func):
            self.func = func

        async def __call__(self, *args, **kwargs):
            return OverLimitHandle(
                func=self.func,
                func_params={
                    'args': args,
                    'kwargs': kwargs,
                },
                key_name=key_name,
                default_return=default_return
            ).execute()

    return RateLimitDecorator
