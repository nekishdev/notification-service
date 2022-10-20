from redis import Redis

from settings import settings

redis_conn = Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=0, decode_responses=True)
