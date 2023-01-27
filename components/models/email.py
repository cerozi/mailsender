class Email:

    def __init__(self, recipient_addr: str, message: str) -> None:
        self.recipient = recipient_addr
        self.message = message
        self.__sent = False

    def successfull_email(self) -> None:
        self.__set_sent()
        return self.__success_message()

    def was_sent(self) -> bool:
        return self.__sent

    def __set_sent(self) -> None:
        self.__sent = True

    def __success_message(self) -> None:
        print("[EMAIL] E-mail enviado com sucesso! ")