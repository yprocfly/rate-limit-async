"""一些常量"""


class LimitConfig:
    # 限流器所属服务
    service = 'default'

    # 总令牌桶数量
    total_quota = 100

    # 单位时间内生成的令牌数
    limit_quota = 3

    # 单位时间
    limit_second = 1

    # 一次请求获取的令牌数
    once_quota = 1

    # 被限流时的处理方式，默认丢弃【discard丢弃；queue排队；retry重试】
    default_handle = 'discard'


class RedisConfig:
    # 地址
    host = 'localhost'

    # 端口
    port = 6380

    # 数据库
    db = 0

    # 密码
    password = ''

    # 最小连接数
    minsize = 1

    # 最大连接数
    maxsize = 10

    # 超时时间【毫秒】
    timeout = 5000

    # 额外参数
    kwargs = None
