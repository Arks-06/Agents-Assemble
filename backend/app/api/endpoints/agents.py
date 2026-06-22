# provides the HTTP API for triggering asynchronous AI tasks
# authenticates users, checks the Redis cache, dispatches jobs to Celery workers, and retrieves specific research history from PostgreSQL

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.future import select

from app.services.cache import get_cache
from app.db.session import get_db
from app.models.research import ResearchTask
from app.workers.tasks import execute_research_agent
from app.workers.celery_app import celery_app
from app.api.deps import get_current_user
from app.models.core import User

router = APIRouter()

class ResearchRequest(BaseModel):
    topic: str

@router.post("/research", status_code=status.HTTP_202_ACCEPTED)
async def run_agent_research(
    payload: ResearchRequest,
    current_user: User = Depends(get_current_user) 
):
    """
    Checks cache first. If miss, sends task to Celery attached to the authenticated user.
    """
    clean_topic = payload.topic.lower().strip()
    cache_key = f"research:topic:{clean_topic}"
    
    cached_data = await get_cache(cache_key)
    if cached_data:
        return {
            "status": "success",
            "message": "Cache Hit! Returned instantly.",
            "db_id": cached_data["db_id"],
            "data": cached_data["data"]
        }
        
    # CACHE MISS
    task = execute_research_agent.delay(payload.topic, current_user.id)
    
    return {
        "status": "processing",
        "message": "Cache Miss. Research task added to the queue.",
        "task_id": task.id 
    }

@router.get("/research/status/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(
    task_id: str,
    # Only logged-in users can poll status
    current_user: User = Depends(get_current_user)
):
    """Checks the Redis result backend for the current status of the agent run."""
    task_result = celery_app.AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
    }
    
    if task_result.status == "SUCCESS":
        response["result"] = task_result.result
    elif task_result.status == "FAILURE":
        response["error"] = str(task_result.info)
        
    return response

@router.get("/research/history", status_code=status.HTTP_200_OK)
async def get_research_history(
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    # Identify the user making the request
    current_user: User = Depends(get_current_user)
):
    """Retrieves the most recent research tasks owned by the authenticated user."""
    try:
        # Query the DB for ONLY this user's tasks
        query = (
            select(ResearchTask)
            .filter(ResearchTask.user_id == current_user.id) 
            .order_by(ResearchTask.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        history = [
            {
                "id": task.id,
                "topic": task.topic,
                "result_data": task.result_data,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
        
        return {
            "status": "success",
            "count": len(history),
            "history": history
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch research history: {str(e)}"
        )