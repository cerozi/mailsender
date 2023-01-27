from typing import Iterable

class Email:

    def __init__(self, recipient_addr: str | Iterable[str], message: str) -> None:
        self.recipients = self.assert_recipients(recipient_addr)
        self.message = message
        self.__sent = False

    def successfull_email(self) -> None:
        self.__set_sent()
        return self.__success_message()

    def was_sent(self) -> bool:
        return self.__sent

    def assert_recipients(self, recipient_addr) -> None:
        if isinstance(recipient_addr, (list, tuple)):
            return recipient_addr

        return (recipient_addr, )

    def __set_sent(self) -> None:
        self.__sent = True

    def __success_message(self) -> None:
        print("[EMAIL] E-mail enviado com sucesso! ")