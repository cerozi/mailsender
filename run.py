from components.controller.manager import MailManager
import os

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

recipient_addr = "mcerozi@gmail.com"
message = "Testing"

with MailManager() as conn:
    conn.auth(username, password)
    conn.mail(recipient = recipient_addr, message = message)