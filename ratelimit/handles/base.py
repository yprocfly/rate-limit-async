from ratelimit.limits.redis_limit import RedisRateLimit


class BaseHandle:
    """公共处理类"""
    handle_key = None

    def __init__(
            self,
            func=None,
            func_params=None,
            limit_config=None,
            default_return=None,
            limit_cls=RedisRateLimit
    ):
        """
        :param func: 被限流的方法
        :param func_params: 被限流的方法的参数
        :param limit_config: 限流配置信息
        :param default_return: 默认返回值【丢弃处理的时候需要返回值】
        :param limit_cls: 判断超限的类【默认使用redis-cell】
        """
        self.func = func
        self.func_params = func_params or {}
        self.limit_config = limit_config or {}
        self.default_return = default_return
        self.limit_cls = limit_cls

    def _get_func_args(self):
        return self.func_params.get('args') or []

    def _get_func_kwargs(self):
        return self.func_params.get('kwargs') or {}

    def _get_handle_params(self):
        return self.limit_config.get('handle_params') or {}

    def _get_key_name(self):
        return self.limit_config.get('key_name')

    async def execute(self):
        """所有处理方式都要重写该方法"""
        raise NotImplementedError('未定义执行方法')
