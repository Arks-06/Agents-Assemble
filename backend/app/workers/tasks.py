# Contains the background AI agent execution logic and task registration.
# Manages the agent lifecycle, result parsing, database persistence, and event broadcasting to Redis

import json
import asyncio
import pydantic
import re
from app.workers.celery_app import celery_app
from app.agents.researcher import build_research_agent
from app.schemas.agent import ResearchResult
from app.models.research import ResearchTask
from app.services.cache import set_cache
from app.db.session import AsyncSessionLocal, engine 
import orjson
from app.core.redis import redis_client

import time

async def save_research_to_db(topic: str, result_data: dict, task_id: str, user_id: int):
    """Async helper to handle our database insertion outside the FastAPI request."""
    try:
        async with AsyncSessionLocal() as db:
            new_research = ResearchTask(
                topic=topic,
                result_data=result_data,
                user_id=user_id 
            )
            db.add(new_research)
            await db.commit()
            await db.refresh(new_research)

            cache_key = f"research:topic:{topic.lower().strip()}"
            
            cache_payload = {
                "db_id": new_research.id,
                "data": result_data
            }
            await set_cache(cache_key, cache_payload)

            broadcast_payload = {
                "task_id": task_id,
                "status": "SUCCESS",
                "message": "Agent completed successfully.",
                "data": result_data
            }
            
            json_str = orjson.dumps(broadcast_payload).decode('utf-8')
            await redis_client.publish("channel:agent_updates", json_str)

            return new_research.id
    finally:
        await engine.dispose()

@celery_app.task(bind=True, name="run_research_task")
def execute_research_agent(self, topic: str, user_id: int):
    task_id = self.request.id

    # print("SLEEPING FOR 15 SECONDS. GO CONNECT POSTMAN NOW!")
    # time.sleep(15)

    try:
        agent = build_research_agent()
        task_prompt = f"""Research the following topic: {topic}
        
        Step 1: Use your Tavily search tool. You may write out your thoughts and explanations normally.
        Step 2: When you are finished, you MUST append a markdown block at the very bottom containing ONLY this JSON structure:
        
        ```json
        {{
            "topic": "{topic}",
            "summary": "A concise 2-sentence summary.",
            "key_takeaways": ["point 1", "point 2", "point 3"],
            "confidence_score": 0.95
        }}
        ```
        """
        response = agent.run(task_prompt)
        
        structured_data = response.content
        
        if isinstance(structured_data, str):
            marker_idx = structured_data.rfind('```json')
            if marker_idx != -1:
                start_idx = structured_data.find('{', marker_idx)
            else:
                start_idx = structured_data.find('{')
                
            end_idx = structured_data.rfind('}')
            
            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                clean_str = structured_data[start_idx : end_idx + 1]
            else:
                clean_str = structured_data
        else:
            clean_str = json.dumps(structured_data)

        try:
            validated_data = ResearchResult.model_validate_json(clean_str)
            jsonb_payload = validated_data.model_dump()
        except (pydantic.ValidationError, ValueError):
            jsonb_payload = {
                "topic": topic,
                "summary": clean_str[:200] + "...", 
                "key_takeaways": ["Format boundary reached during agent execution."],
                "confidence_score": 0.0
            }

        db_id = asyncio.run(save_research_to_db(topic, jsonb_payload, task_id, user_id))

        return {
            "status": "success",
            "db_id": db_id,
            "data": jsonb_payload
        }
        
    except Exception as e:
        fallback = {
            "topic": topic,
            "summary": "Agent execution failed.",
            "key_takeaways": [str(e)],
            "confidence_score": 0.0
        }
        db_id = asyncio.run(save_research_to_db(topic, fallback, task_id, user_id))
        return {"status": "partial_success", "db_id": db_id, "data": fallback}