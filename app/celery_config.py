from celery import Celery

BROKER_URL = "redis://localhost:6379/2"
CELERY_RESULT_BACKEND = "redis://localhost:6379/3"

celery = Celery(__name__)
celery.conf.broker_url = BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
celery.conf.imports = ['app.core.components.mail.controller.mailmanager']