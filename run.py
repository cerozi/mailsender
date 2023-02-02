from components.mail.controller.manager import AsyncMail
from concurrent.futures import ALL_COMPLETED, wait
import os
import time

username = os.environ.get("MAIL_USERNAME")
password = os.environ.get("MAIL_PASSWORD")

asyncmail = AsyncMail()
asyncmail.validate_credentials(username, password)

def main() -> None:
    futures = asyncmail.send_mail(recipients_addr = ['mcerozi@gmail.com'] * 10, message = "async teste")
    wait(futures, return_when = ALL_COMPLETED)


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    finish = time.perf_counter()

    print(f"Finished in {round(finish - start, 2)} seconds...")