# Handles real-time communication between background Celery workers and WebSocket clients via Redis.
# Subscribes to message channels to push asynchronous AI task updates to active user sessions.

import asyncio
import orjson
from app.core.redis import redis_client
from app.core.websockets import manager

async def listen_to_redis_channel():
    """Background loop that listens for Celery broadcasts."""
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("channel:agent_updates")
    print("Broadcaster: Listening for Redis updates on 'channel:agent_updates'...")
    
    try:
        # Continuously yield messages as they arrive
        async for message in pubsub.listen():
            if message["type"] == "message":
                # Parse the raw bytes back into a Python dictionary
                data = orjson.loads(message["data"])
                task_id = data.get("task_id")
                
                if task_id:
                    await manager.send_personal_message(data, task_id)
                    
    except asyncio.CancelledError:
        # clean up if FastAPI shuts down
        await pubsub.unsubscribe("channel:agent_updates")
        print("Broadcaster: Disconnected gracefully.")