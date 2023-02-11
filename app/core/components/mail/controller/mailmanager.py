"""
    A classe Mail() é a classe que
    vai servir de interface para o usuário
    autenticar e enviar múltiplos e-mails.
"""


from concurrent.futures import Future
from itertools import repeat
import queue
from typing import Iterable, Tuple

from app.celery_config import celery
from app.core.components.connection.conn import MailConnection
from app.core.components.mail.auth.authentication import Authentication
from app.core.components.mail.models.email import Email
from app.core.exceptions.exceptions import UnauthenticatedException


class Mail(celery.Task):

    name = 'Mail'

    def __init__(self) -> None:

        """
            Envia múltiplos e-mails de maneira
            assíncrona e/ou síncrona.
        """

        self.__emails = list()
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

    def __send(self, credentials: Tuple[str, str], emails: list) -> Tuple[Tuple[str, bool, str | None]]:

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


    def run(self, credentials: Tuple[str, str], emails: list):
        # TODO: adicionar Redis para verificar assinatura;
        return self.__send(credentials, emails)


    def send_mail(self, recipients_addr: Iterable[str], message: str, asynch: bool = True) -> Tuple[Future] | Tuple[Tuple[str, bool, str | None]]:

        """
            Cria instâncias de Email e adiciona elas à
            Queue contendo e-mails a serem enviados. Após
            preencher a Queue, faz o envio do e-mail de
            maneira assíncrona atráves de .delay() ou de
            maneira síncrona atráves de .run().

                Args:
                    >>> recipients_addr: Lista de destinatários.
                    >>> message: Corpo da mensagem do e-mail.
                    >>> asynch: Se o envio dos e-mails deve
                    ser assíncrono ou síncrono.
        """
        
        # valida se o usuário está autenticado
        if not self.__auth.is_authenticated():
            raise UnauthenticatedException()

        # cria instâncias da classe Email para cada recipiente da lista recipients_addr e adiciona estas à Queue
        [self.__emails.append(email) for email in map(lambda args: Email(*args), zip(recipients_addr, repeat(message, len(recipients_addr))))]

        # envia os e-mails de maneira assíncrona
        if asynch:
            # TODO: Adicionar redis para gerar assinatura;
            return self.apply_async(
                args = (self.__auth.get_credentials(), self.__emails),
                serializer = 'pickle'
            )

        # envia os e-mails de maneira síncrona
        return self.run(self.__auth.get_credentials(), self.__emails)


celery.register_task(Mail())