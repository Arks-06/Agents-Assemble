# manages secure, real-time TCP connections, authenticates users via URL tokens, 
# links them to a specific AI task's broadcast channel, and keeps the socket open for live updates

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.websockets import manager
from app.workers.celery_app import celery_app
from app.api.deps import get_current_user_ws
from app.models.core import User

router = APIRouter()

@router.websocket("/ws/research/status/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    task_id: str,
    current_user: User = Depends(get_current_user_ws) 
):
    """Secure endpoint for real-time updates."""
    
    await manager.connect(websocket, task_id, current_user.id)
    
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.status == "SUCCESS":
            await websocket.send_json({
                "task_id": task_id,
                "status": "SUCCESS",
                "message": "Task was already completed before you connected.",
                "data": task_result.result
            })

        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(task_id)