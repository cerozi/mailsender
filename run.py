from components.controller.manager import MailManager
from components.models.email import Email
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

with MailManager() as mail_conn:
    mail_conn.auth(username, password)

    mail = Email(recipient_addr = ["mcerozi@gmail.com", "matheus.cerozi@jobconvo.com"], message = "Teste com multiplos recipientes. ")
    mail_conn.mail(mail)

    assert mail.was_sent() is True