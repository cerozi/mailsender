from celery import Celery

celery = Celery(__name__)
celery.conf.imports = ['app.core.components.mail.controller.mailmanager']
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']

def set_addr(
    broker_url: str,
    result_url: str
) -> None:

    celery.conf.broker_url = broker_url
    celery.conf.result_backend = result_url  
