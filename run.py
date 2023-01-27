from components.controller.manager import MailManager
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

recipient_addr = "mcerozi@gmail.com"
message = "Teste"

with MailManager() as mail_conn:
    mail_conn.auth(username, password)
    mail_conn.mail(recipient = recipient_addr, message = message)