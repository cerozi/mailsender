from app.core.components.mail.controller.mailmanager import Mail
from time import sleep
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

mail = Mail()
assert mail.validate_credentials(username, password) is True


task = mail.send_mail(recipients_addr = ['omagomaguin@gmail.com'] * 5, message = "Celery async test.")
print(type(task))

while not task.ready():
    sleep(1)
    print("Task running...")