import asyncio
import base64
# import pickle
import contextvars
import functools

import dill as pickle

from ratelimit.base.constants import RedisConfig
from ratelimit.base.errors import ReWriteStopIteration

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
        print(err)
        return None


async def get_redis_connection():
    """获取一个redis连接"""
    if RedisConfig.conn is None:
        RedisConfig.conn = await create_redis_pool(
            f"redis://:{RedisConfig.password}@{RedisConfig.host}:{RedisConfig.port}/{RedisConfig.db}",
            minsize=RedisConfig.minsize,
            maxsize=RedisConfig.maxsize,
            **(RedisConfig.kwargs or {})
        )

    return RedisConfig.conn
