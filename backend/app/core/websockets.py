# maintains a live dictionary of active user connections and provides the orchestration logic to push specific messages to the correct browser clients

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # task_id -> {"websocket": WebSocket, "user_id": int}
        self.active_connections: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, task_id: str, user_id: int):
        """Accepts the connection and maps it to BOTH the task and the user."""
        await websocket.accept()
        self.active_connections[task_id] = {
            "websocket": websocket,
            "user_id": user_id
        }

    def disconnect(self, task_id: str):
        """Removes the connection from the roster to prevent memory leaks."""
        if task_id in self.active_connections:
            del self.active_connections[task_id]

    async def send_personal_message(self, message: dict, task_id: str):
        """Sends a JSON payload to a specific task's websocket."""
        if task_id in self.active_connections:
            websocket = self.active_connections[task_id]["websocket"]
            await websocket.send_json(message)

# global manager instance
manager = ConnectionManager()