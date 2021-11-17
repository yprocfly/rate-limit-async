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

    # 处理方式对应的默认配置参数
    default_handle_params = {}

    # 是否使用redis的配置，这里如果是True，会优先去redis中获取配置
    use_redis = False

    """
    详细配置，这里可以分别给每个具体的方法配置，具体格式如下：
    {
        "key_name": {
            "total_quota": 100,          # 令牌桶大小
            "limit_second": 10,          # 生成令牌的单位时间
            "limit_quota": 3,            # 单位时间内生成的令牌数量
            "once_quota": 1,             # 每次请求消费的令牌数量
            "handle": "discard",         # discard丢弃；queue排队；retry重试
            "handle_params": {},         # 处理方式对应的参数，详细见handles的注释
        }
    }
    """
    rate_limit_config = {}


class RedisConfig:
    # 地址
    host = '129.204.145.169'

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

    # 初始化连接池
    conn = None
