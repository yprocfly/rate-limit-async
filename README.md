### 安装方式
pip install rate-limit-async

### 使用说明
基于redis-cell扩展的限流，使用该包需要安装redis-cell扩展，支持分布式限流。

目前只支持异步方法的限流，使用方式如下：
``` 
from ratelimit.decorators import async_rate_limit

# 这里的key_name必须要在一个服务中唯一，不然会有冲突
@async_rate_limit("key_name")
async def need_limit_method():
    ...
```

### 修改配置
```
from ratelimit.base.constants import RedisConfig, LimitConfig

# 这里是redis连接信息
RedisConfig.host = '127.0.0.1'
RedisConfig.port = 6379
RedisConfig.passwors = ''
RedisConfig.db = 0

# 这里是默认的限流配置
LimitConfig.service = 'default'         # 限流器所属服务
LimitConfig.total_quota = 100           # 总令牌桶数量
LimitConfig.quota = 3                   # 单位时间内生成的令牌数
LimitConfig.limit_second = 1            # 单位时间
LimitConfig.once_quota = 1              # 一次请求获取的令牌数
LimitConfig.default_handle = 'discard'  # 被限流时的处理方式，默认丢弃【discard丢弃；queue排队；retry重试】
```

### 配置写在redis中
```
在redis中可以根据实际情况配置限流信息，格式如下：
    "service": {
        "key_name": {
            "total_quota": 100,          # 令牌桶大小
            "limit_second": 10,          # 生成令牌的单位时间
            "limit_quota": 3,            # 单位时间内生成的令牌数量
            "once_quota": 1,             # 每次请求消费的令牌数量
            "handle": "discard",         # discard丢弃；queue排队；retry重试
            "handle_params": {},         # 处理方式对应的参数
        }
    }
这里的key_name要对应装饰器的key_name

handle_params的配置如下：
1、handle 为 discard 类型的，无需配置
2、handle 为 queue 类型的，配置如下：
    {
        "delay": 3,               # 延时执行时间，单位【秒】
        "limit_delay": 1,         # 执行再次被限制的情况下，延迟执行时间，单位【秒】
        "queue_type": "redis",    # 队列类型：redis【基于redis队列】、local【基于本地内存队列】
    }
3、handle 为 retry 类型的，配置如下：
    {
        "retry_count": 3,    # 重试次数
        "retry_wait": 0,     # 每次重试间隔，默认不等待，单位【秒】
        "current_count": 0,  # 当前已重试几次
    }
```
