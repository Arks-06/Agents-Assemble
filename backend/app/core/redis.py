import redis.asyncio as redis

redis_client = redis.Redis.from_url(
    "redis://localhost:6379/1", 
    decode_responses=True
)