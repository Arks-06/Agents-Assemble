import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth
from app.core.config import settings
from app.api.endpoints import agents
from app.api.endpoints import websockets
from app.services.broadcaster import listen_to_redis_channel

@asynccontextmanager
async def lifespan(app: FastAPI):
    broadcaster_task = asyncio.create_task(listen_to_redis_channel())
    yield
    broadcaster_task.cancel()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Distributed Multi-Agent Orchestration Hub",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(websockets.router, tags=["Real-Time WebSockets"])
@app.get("/")
async def root():
    return {"status": "online", "message": "Agents Assemble Backend is running!"}