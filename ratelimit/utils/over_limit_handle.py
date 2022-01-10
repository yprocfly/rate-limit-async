from ratelimit.handles import HandleFactory
from ratelimit.limits.redis_limit import RedisRateLimit


class OverLimitHandle:

    def __init__(self, func, func_params, key_name, default_return=None):
        """
        当流量超限时的处理类
        :param func: 超限的方法
        :param func_params: 超限方法的参数
        :param key_name: 获取超限配置的key
        :param default_return: 默认返回值
        """
        self.func = func
        self.func_params = func_params
        self.key_name = key_name
        self.default_return = default_return

    async def _can_do_func(self):
        """检查流量是否限制"""
        result, self.limit_config = await RedisRateLimit().attempt_get_token(key_name=self.key_name)
        return result

    async def _do_if_limit(self):
        """如果被限流了，根据配置信息做相应的处理"""
        handle_cls = HandleFactory().get_handle_cls(self.limit_config.get('handle'))
        return await handle_cls(
            func=self.func,
            func_params=self.func_params,
            limit_config=self.limit_config,
            default_return=self.default_return
        ).execute()

    async def _run_func(self):
        """运行监听的方法"""
        func_args = self.func_params.get('args') or []
        func_kwargs = self.func_params.get('kwargs') or {}
        return await self.func(*func_args, **func_kwargs)

    async def execute(self, exec_default_handle=True):
        """
        :param exec_default_handle: 是否执行默认操作
        :return:
        """
        if await self._can_do_func():
            return await self._run_func()

        # 如果不执行默认配置的操作，直接返回默认结果
        if not exec_default_handle:
            return self.default_return

        return await self._do_if_limit()
