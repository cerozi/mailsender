from components.mail.models.email import Email
from components.connection.conn import MailConnection
from components.mail.controller.authentication import Authentication
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Type
from queue import Queue
import time


class AsyncMail:

    def __init__(self) -> None:
        self.__pool = ThreadPoolExecutor()
        self.__emails = Queue()
        self.__auth = Authentication()

    def validate_credentials(self, username: str, password: str):

        with MailConnection() as conn:

            if conn.auth(username, password):
                self.__auth.set_credentials(username, password)
                return self.__auth.authenticated_message()

        self.__auth.set_authenticated(False)
        return self.__auth.not_authenticated_message()

    def __asyncsend(self, email: Type[Email]) -> None:

        with MailConnection() as conn:

            conn.auth(*self.__auth.get_credentials())
            return conn.mail(email)

    def send_mail(self, recipients_addr: Iterable[str], message: str):
        
        if not self.__auth.is_authenticated():
            return self.__auth.not_authenticated_message()

        for recipient in recipients_addr:
            email = Email(recipient, message)
            self.__emails.put(email)

        future_list = list()
        while not self.__emails.empty():
            future_list.append(self.__pool.submit(self.__asyncsend, self.__emails.get()))

        return future_list


        