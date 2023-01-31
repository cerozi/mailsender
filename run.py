from components.connection.conn import MailConnection
from components.mail.models import Email
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

with MailConnection() as mail_conn:
    mail_conn.auth(username, password)

    mail = Email(recipient_addr = ["mcerozi@gmail.com", "matheus.cerozi@jobconvo.com"], message = "Teste com multiplos recipientes. ")
    mail_conn.mail(mail)

    assert mail.was_sent() is True