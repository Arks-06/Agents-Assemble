# Configures the Celery application instance and Redis broker settings.
# Initializes the distributed task queue environment

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "agents_assemble_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"] # where to look for work
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)