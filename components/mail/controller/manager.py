from components.mail.models.email import Email
from components.connection.conn import MailConnection
from components.mail.controller.authentication import Authentication
from concurrent.futures import ThreadPoolExecutor, Future
from exceptions.exceptions import UnauthenticatedException
from typing import Iterable, Type, Tuple
from queue import Queue
from itertools import repeat


class Mail:

    def __init__(self) -> None:
        self.__pool = ThreadPoolExecutor()
        self.__emails = Queue()
        self.__auth = Authentication()

    def validate_credentials(self, username: str, password: str) -> str:

        with MailConnection() as conn:

            if conn.auth(username, password):
                self.__auth.set_credentials(username, password)
                return self.__auth.authenticated_message()

        self.__auth.set_authenticated(False)
        return self.__auth.not_authenticated_message()

    def __send(self, email: Type[Email]) -> Future:

        with MailConnection() as conn:

            conn.auth(*self.__auth.get_credentials())
            return conn.mail(email)

    def __asyncsend(self) -> Tuple[Future]:
        futures = list()
        while not self.__emails.empty():
            futures.append(self.__pool.submit(self.__send, self.__emails.get()))

        return tuple(futures)

    def __syncsend(self) -> Tuple[Tuple[str, bool, str | None]]:
        result = list()
        while not self.__emails.empty():
            result.append(self.__send(self.__emails.get()))

        return tuple(result)

    def send_mail(self, recipients_addr: Iterable[str], message: str, asynch: bool = True) -> Tuple[Future] | str:
        
        if not self.__auth.is_authenticated():
            raise UnauthenticatedException()

        [self.__emails.put(email) for email in map(lambda args: Email(*args), zip(recipients_addr, repeat(message, len(recipients_addr))))]

        if asynch:
            return self.__asyncsend()

        return self.__syncsend()


        