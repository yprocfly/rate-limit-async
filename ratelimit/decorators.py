"""一些装饰器"""
import asyncio

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
            return await OverLimitHandle(
                func=self.func,
                func_params={
                    'args': args,
                    'kwargs': kwargs,
                },
                key_name=key_name,
                default_return=default_return
            ).execute()

    return RateLimitDecorator


if __name__ == '__main__':
    async def test_limit():
        @async_rate_limit('test')
        async def test(number):
            from datetime import datetime
            print('*********', datetime.now(), number)

        import random
        from ratelimit.base.constants import LimitConfig
        LimitConfig.total_quota = 0
        LimitConfig.limit_quota = 1
        LimitConfig.default_handle = 'queue'
        LimitConfig.default_handle_params = {
            'delay': 3,
            'limit_delay': 1,
            'queue_type': 'local'
        }

        await test(random.random())
        await test(random.random())

        await asyncio.sleep(5)

        await test(random.random())
        print('----------------3')
        await test(random.random())
        await test(random.random())
        print('----------------4')
        await asyncio.sleep(10)

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(test_limit())
    loop.run_until_complete(task)
