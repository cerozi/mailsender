"""
    A classe Mail() é a classe que
    vai servir de interface para o usuário
    autenticar e enviar múltiplos e-mails.
"""


from itertools import repeat
import queue
from typing import Iterable, Tuple

from colorama import Fore
from threading import Thread
from app.celery_config import celery
from app.core.components.connection.conn import MailConnection
from app.core.components.mail.auth.authentication import Authentication
from app.core.components.mail.models.email import Email
from app.core.exceptions.exceptions import UnauthenticatedException


class Mail:

    def __init__(self) -> None:

        """
            Envia múltiplos e-mails de maneira
            assíncrona e/ou síncrona.
        """

        self.__auth = Authentication()

    def validate_credentials(self, username: str, password: str) -> bool:

        """
            Valida as credenciais do usuário que
            enviará os e-mails. Se estas não forem 
            válidas, seta o usuário como não autenticado
            e futuras chamadas pra função send_mail() 
            levantarão exceções.

                Args:
                    >>> username: E-mail da conta.
                    >>> password: Senha da conta.

                Returns:
                    Booleano indicando se o usuário foi
                    autenticado.
        """

        with MailConnection() as conn:

            if conn.auth(username, password):
                self.__auth.set_credentials(username, password)
                return self.__auth.set_authenticated(True)

        return self.__auth.set_authenticated(False)

    
    @staticmethod
    @celery.task
    def __send(credentials: Tuple[str, str], emails: list) -> Tuple[Tuple[str, bool, str | None]]:

        """
            Abre conexão com o servidor do Gmail,
            autentica o usuário e envia os e-mails
            da Queue.

                Returns:
                    Tupla contendo informações referentes ao envio
                    de cada E-mail.
        """

        sent_emails = list()
        
        mailsqueue = queue.Queue()
        mailsqueue.queue = queue.deque(emails)

        with MailConnection() as conn:

            conn.auth(*credentials)
            while not mailsqueue.empty():
                email = conn.mail(mailsqueue.get())
                sent_emails.append(email)

        return tuple([email.get_info() for email in sent_emails])

    def send_mail(self, recipients_addr: Iterable[str], message: str, asynch: int = 0) -> None:

        if not self.__auth.is_authenticated():
            raise UnauthenticatedException()
        
        if not asynch in range(0, 3):
            raise ValueError("Asynch arg must be 1 (for celery) or 2 (for threading)! ")

        emails = tuple(map(lambda args: Email(*args), zip(recipients_addr, repeat(message, len(recipients_addr)))))

        if asynch == 1:

            return self.__send.apply_async(
                args = (self.__auth.get_credentials(), emails), serializer = 'pickle'
            )

        if asynch == 2:

            return Thread(
                target = self.__send.run, daemon = False,
                args = (self.__auth.get_credentials(), emails), 
                ).start()

        return self.__send.run(
            self.__auth.get_credentials(), emails
        )
