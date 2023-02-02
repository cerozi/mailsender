from typing import Type, Tuple

class Email:

    def __init__(self, recipient: str, message: str) -> None:
        self.recipient = recipient
        self.message = message
        self.__sent = False
        self.__errors = None

    def set_sent(self) -> Tuple[str, bool, None | str]:
        self.__sent = True
        return self.get_info()

    def set_error(self, exception: Type[Exception]) -> Tuple[str, bool, None | str]:
        self.__errors = exception.__repr__()
        return self.get_info()

    @property
    def errors(self) -> str | None:
        return self.__errors

    def get_info(self) -> Tuple[str, bool, None | str]:
        return (
            self.__repr__(),
            self.__sent,
            self.__errors
        )

    def was_sent(self) -> bool:
        return self.__sent

    def __repr__(self) -> str:
        return f'(to: {self.recipient}, msg: {self.message})'
