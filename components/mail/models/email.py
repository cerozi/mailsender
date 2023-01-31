from typing import Iterable, Type, Union

class Email:

    def __init__(self, recipients_addr: Iterable[str], message: str) -> None:
        self.recipients = recipients_addr
        self.message = message
        self.__sent = False
        self.__errors = None

    def set_sent(self) -> None:
        self.__sent = True

    def set_errors(self, exception: Type[Exception]) -> None:
        self.__errors = exception.__repr__()

    @property
    def errors(self) -> Union[str, None]:
        return self.__errors

    def get_info(self) -> str:
        return (
            self.__repr__(),
            self.__sent,
            self.__errors
        )

    def was_sent(self) -> bool:
        return self.__sent

    def __repr__(self) -> str:
        return f'(to: {self.recipients}, msg: {self.message})'
