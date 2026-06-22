# Manages high-speed data retrieval for AI research tasks using Redis.
# Provides utility functions to store and fetch serialized task results, minimizing redundant agent executions.

import orjson
from typing import Optional, Any
from app.core.redis import redis_client

async def get_cache(key: str) -> Optional[Any]:
    """Retrieves and deserializes data from Redis."""
    try:
        data = await redis_client.get(key)
        if data:
            return orjson.loads(data)
        return None
    except Exception as e:
        print(f"Redis Cache Read Error: {e}")
        return None

async def set_cache(key: str, value: Any, expire: int = 3600):
    """Serializes and saves data to Redis with a 1-hour expiration."""
    try:
        # orjson.dumps returns bytes, decode to string for Redis
        json_str = orjson.dumps(value).decode('utf-8')
        await redis_client.set(key, json_str, ex=expire)
    except Exception as e:
        print(f"Redis Cache Write Error: {e}")