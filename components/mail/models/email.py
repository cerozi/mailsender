from typing import Type, Union

class Email:

    def __init__(self, recipient: str, message: str) -> None:
        self.recipient = recipient
        self.message = message
        self.__sent = False
        self.__errors = None

    def set_sent(self) -> None:
        self.__sent = True
        return self.was_sent()

    def set_error(self, exception: Type[Exception]) -> None:
        self.__errors = exception.__repr__()
        return self.was_sent()

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
        return f'(to: {self.recipient}, msg: {self.message})'
