from app.core.components.mail.controller.mailmanager import Mail
from app.celery_config import set_addr
from celery_config import BROKER_URL, CELERY_RESULT_BACKEND
import os

set_addr(BROKER_URL, CELERY_RESULT_BACKEND)
mail = Mail()

assert mail.validate_credentials(
    os.environ.get("MAIL_USERNAME"),
    os.environ.get("MAIL_PASSWORD")
) is True, ('Invalid credentials.')


mail.send_mail(recipients_addr = ['omagomaguin@gmail.com'] * 5, message = '...', asynch = 1)