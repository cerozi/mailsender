from app.components.mail.controller.mailmanager import Mail
from concurrent.futures import ALL_COMPLETED, wait
from typing import Type, Callable
from time import perf_counter
import os


class MailTesting:

    RECIPIENT = ['omagomaguin@gmail.com']
    MESSAGE = 'TESTING'
    N_TIMES = 100

    """
        Essa classe serve apenas para príncipio
        comparativo de perfomance entre o envio
        de e-mails de maneira síncrona e assíncrona.

        Para isso, o mesmo e-mail foi enviado a mesma
        quantidade de vezes de maneira assíncrona e depois
        de maneira síncrona, e o tempo de envio de cada um
        foi comparado.
    """

    @staticmethod
    def timer(fn: Callable) -> Callable:

        def wrapper(*args, **kwargs) -> float:

            start = perf_counter()
            fn(*args, **kwargs)
            finish = perf_counter()

            time = round(finish - start, 2)
            print(f"{fn.__name__} finished in {time} seconds.")
            
            return time 

        return wrapper

    @timer
    def asyncmail(self, mail: Type[Mail]) -> None:

        futures = mail.send_mail(self.RECIPIENT * self.N_TIMES, self.MESSAGE)
        wait(futures, return_when = ALL_COMPLETED)

        for f in futures:
            print(f.result())

    @timer
    def syncmail(self, mail: Type[Mail]) -> None:

        mail.send_mail(self.RECIPIENT * self.N_TIMES, self.MESSAGE, asynch = False)

    def compare(self, sync_timer: float, async_timer: float) -> None:
        y = (abs(async_timer - sync_timer) / sync_timer) * 100.0
        print(f"Sending e-mails asynchronously ran %{y} faster!")

    def run(self) -> None:

        username = os.environ.get("MAIL_USERNAME")
        password = os.environ.get("MAIL_PASSWORD")

        mail = Mail()
        assert mail.validate_credentials(username, password) is True, ('Invalid credentials.')

        self.asyncmail(mail)

        """
        self.compare(
            self.syncmail(mail),
            self.asyncmail(mail)
        )
        """


if __name__ == '__main__':

    tests = MailTesting()
    tests.run()