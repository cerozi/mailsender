from app.celery_config import celery

BROKER_URL = "redis://localhost:6379/2"
CELERY_RESULT_BACKEND = "redis://localhost:6379/3"

celery.conf.broker_url = BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
