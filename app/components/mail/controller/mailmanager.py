"""
    A classe Mail() é a classe que
    vai servir de interface para o usuário
    autenticar e enviar múltiplos e-mails.
"""


from concurrent.futures import Future, ThreadPoolExecutor, ALL_COMPLETED, wait
from itertools import repeat
from queue import Queue
from typing import Iterable, Tuple, Type
from time import sleep

from app.components.connection.conn import MailConnection
from app.components.mail.auth.authentication import Authentication
from app.components.mail.models.email import Email
from app.exceptions.exceptions import UnauthenticatedException


class Mail:


    def __init__(self) -> None:

        """
            Envia múltiplos e-mails de maneira
            assíncrona ou síncrona.
        """

        self.__pool = ThreadPoolExecutor()
        self.__emails = Queue()
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
                    Mensagem sinalizando se o usuário
                    foi autenticado ou não.
        """

        with MailConnection() as conn:

            if conn.auth(username, password):
                return self.__auth.set_credentials(username, password)

        return self.__auth.set_authenticated(False)

    def __send(self, email: Type[Email]) -> Future:

        """
            Loga o usuário e envia
            o e-mail.

                Args:
                    >>> email: Instância da classe E-mail.
        """

        with MailConnection() as conn:

            conn.auth(*self.__auth.get_credentials())
            return conn.mail(email)

    def __asyncsend(self) -> Tuple[Future]:

        """
            Envia múltiplos e-mails
            de maneira assíncrona.

                Returns:
                    Tupla contendo objetos Future.
        """

        futures = list()
        chunks = list()
        n = 0

        while not self.__emails.empty():
            email, n = self.__emails.get(), n + 1
            chunks.append(self.__pool.submit(self.__send, email))

            if (n % self.__pool._max_workers == 0):
                print('...')
                wait(chunks, return_when = ALL_COMPLETED, timeout = 180) and sleep(2.5)

                futures.extend(chunks)
                chunks = list()

        return tuple(futures)

    def __syncsend(self) -> Tuple[Tuple[str, bool, str | None]]:

        """
            Envia múltiplos e-mails
            de maneira síncrona.

                Returns:
                    Tupla contendo informações referentes ao envio
                    de cada E-mail.
        """

        result = list()
        while not self.__emails.empty():
            result.append(self.__send(self.__emails.get()))

        return tuple(result)

    def send_mail(self, recipients_addr: Iterable[str], message: str, asynch: bool = True) -> Tuple[Future] | Tuple[Tuple[str, bool, str | None]]:

        """
            Cria instâncias de Email e adiciona elas à
            Queue contendo e-mails a serem enviados.

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
        [self.__emails.put(email) for email in map(lambda args: Email(*args), zip(recipients_addr, repeat(message, len(recipients_addr))))]

        if asynch:
            # envia os e-mails de maneira assíncrona
            return self.__asyncsend()

        # envia os e-mails de maneira síncrona
        return self.__syncsend()


        