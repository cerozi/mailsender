from components.mail.models.email import Email
from typing import Iterable, Type, Tuple

class MailManager:

    def __init__(self) -> None:
        self.__emails = list()

    def create_email(self, recipients_addr: str | Iterable[str], message: str) -> Type[Email]:

        if not isinstance(recipients_addr, (list, tuple)):
            recipients_addr = (recipients_addr, )

        email = Email(recipients_addr, message)
        self.__emails.append(email)

        return email

    def result(self) -> Tuple[Tuple[str, bool, str]]:
        return (email.get_info() for email in self.__emails)

    def sent(self) -> Tuple[str]:
        return (email.__repr__() for email in self.__emails if email.was_sent())

    def not_sent(self) -> Tuple[Tuple[str, str]]:
        return ((email.__repr__(), email.errors) for email in self.__emails if not email.was_sent())

    def is_successfull(self) -> bool:
        return all(email.was_sent() for email in self.__emails)