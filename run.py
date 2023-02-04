from components.mail.controller.manager import Mail
from concurrent.futures import ALL_COMPLETED, wait
import os
import time

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

mail = Mail()
mail.validate_credentials(username, password)

def asyncmail() -> None:
    futures = mail.send_mail(recipients_addr = ['mcerozi@gmail.com'] * 10, message = "Sendind e-mails asynchronously.")
    wait(futures, return_when = ALL_COMPLETED)

def syncmail() -> None:
    mail.send_mail(recipients_addr = ['mcerozi@gmail.com'] * 10, message = "Sending e-mails synchronously. ", asynch = False)


if __name__ == '__main__':
    async_start = time.perf_counter()
    asyncmail()
    async_finish = time.perf_counter()

    sync_start = time.perf_counter()
    syncmail()
    sync_finish = time.perf_counter()

    print(f"asyncmail() finished in {round(async_finish - async_start, 2)} seconds...")
    print(f"syncmail() finished in {round(sync_finish - sync_start, 2)} seconds...")