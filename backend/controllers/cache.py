from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'redis://localhost:6379/3', 'CACHE_DEFAULT_TIMEOUT': 300})
