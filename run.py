from components.connection.conn import MailConnection
from components.mail.controller.manager import MailManager
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

mail = MailManager()

with MailConnection() as mail_conn:
    mail_conn.auth(username, password)

    mail.create_email(
        recipients_addr = ['matheus.cerozi@jobconvo.com', 'mcerozi@gmail.com'], 
        message = "Teste usando manager"
    )

    mail_conn.mail(mail)
