from components.controller.manager import MailManager
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

with MailManager() as conn:
    conn.auth(username, password)