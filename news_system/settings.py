from os import getenv

from redis import ConnectionPool

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
REDIS_POOL = ConnectionPool(host='localhost', port=6379, decode_responses=True)
