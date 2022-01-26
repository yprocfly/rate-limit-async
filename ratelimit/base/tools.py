import base64
import dill as pickle
import aioredis_cluster

from ratelimit.base.constants import RedisConfig

try:
    from aioredis import create_redis_pool, ConnectionsPool
except:
    raise Exception('未安装 aioredis 库，支持 1.X.X 版本')


def encode_serialize(obj):
    """
    将对象序列化成字符串
    :param obj: 要序列化的对象
    :return: obj_str
    """
    return base64.b64encode(pickle.dumps(obj)).decode()


def decode_serialize(obj_str):
    """
    将字符串反序列化成对象
    :param obj_str: 被序列化的字符串
    :return: obj
    """
    try:
        return pickle.loads(base64.b64decode(obj_str))
    except Exception as err:
        return None


async def get_redis_connection():
    """获取一个redis连接"""
    if RedisConfig.conn:
        return RedisConfig.conn

    if RedisConfig.is_cluster:
        # 集群模式
        assert RedisConfig.startup_nodes, '集群节点未配置'
        RedisConfig.conn = await aioredis_cluster.create_redis_cluster(
            startup_nodes=RedisConfig.startup_nodes,
            password=RedisConfig.password,
            pool_minsize=RedisConfig.minsize,
            pool_maxsize=RedisConfig.maxsize,
            connect_timeout=RedisConfig.timeout,
            **(RedisConfig.kwargs or {})
        )
    else:
        # 单机模式
        RedisConfig.conn = await create_redis_pool(
            address=[RedisConfig.host, RedisConfig.port],
            db=RedisConfig.db,
            password=RedisConfig.password,
            minsize=RedisConfig.minsize,
            maxsize=RedisConfig.maxsize,
            timeout=RedisConfig.timeout,
            **(RedisConfig.kwargs or {})
        )

    return RedisConfig.conn
