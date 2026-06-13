from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.rabbitmq_url,
    result_backend=settings.redis_url,
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["app.tasks"])
