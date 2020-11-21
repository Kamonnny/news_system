from flask import current_app
from redis import StrictRedis


# noinspection SpellCheckingInspection
class Redis:

    @staticmethod
    def _get_r():
        """
        连接 Redis 连接池
        :return:
        """
        pool = current_app.config['REDIS_POOL']
        return StrictRedis(connection_pool=pool)

    @classmethod
    def set(cls, key: str, value: str, expire=None) -> None:
        """
        写入键值对
        :param key:
        :param value:
        :param expire:
        :return:
        """
        r = cls._get_r()
        r.set(key, value, ex=expire)

    @classmethod
    def get(cls, key: str) -> str:
        """
        读取键值对内容
        :param key:
        :return:
        """
        r = cls._get_r()
        value = r.get(key)
        return value

    @classmethod
    def hset(cls, name: str, key: str, value: str) -> None:
        """
        写入hash表
        :param name:
        :param key:
        :param value:
        :return:
        """
        r = cls._get_r()
        r.hset(name, key, value)

    @classmethod
    def hget(cls, name: str, key: str) -> str:
        """
        读取指定hash表的键值
        :param name:
        :param key:
        :return:
        """
        r = cls._get_r()
        value = r.hget(name, key)
        return value

    @classmethod
    def hmget(cls, name: str, keys: tuple) -> list:
        """
        读取指定hash表的所有给定字段的值
        :param keys:
        :param name:
        :return:
        """
        r = cls._get_r()
        value = r.hmget(name, keys)
        return value

    @classmethod
    def hgetall(cls, name: str) -> dict:
        """
        获取指定hash表所有的值
        :param name:
        :return:
        """
        r = cls._get_r()
        return r.hgetall(name)

    @classmethod
    def hdel(cls, name: str, key: str) -> None:
        """
        删除指定hash表的键值
        :param name:
        :param key:
        :return:
        """
        r = cls._get_r()
        r.hdel(name, key)

    @classmethod
    def expire(cls, name: str, expire: int) -> None:
        """
        设置过期时间
        :param name:
        :param expire:
        :return:
        """
        r = cls._get_r()
        r.expire(name, expire)

    @classmethod
    def delete(cls, *names: str) -> None:
        """
        删除一个或者多个
        :param names:
        :return:
        """
        r = cls._get_r()
        r.delete(*names)

    @classmethod
    def flushall(cls) -> None:
        """
        清空整个 Redis
        :return:
        """
        r = cls._get_r()
        r.flushall()
