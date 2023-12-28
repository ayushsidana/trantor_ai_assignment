from trantor_ai_assignment.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from kombu import Exchange, Queue

CELERY_BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "UTC"
CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
)
