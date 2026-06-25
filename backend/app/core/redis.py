import redis.asyncio as redis
from app.core.config import settings

# Force the client to use the cloud URL from your settings
redis_client = redis.Redis.from_url(
    settings.CELERY_BROKER_URL, 
    decode_responses=True
)