class ConnectionException(Exception):
    
    def __init__(self) -> None:
        message = "Connection unsuccesfull. "
        return super().__init__(message)


class HeloException(Exception):

    def __init__(self) -> None:
        message = "The @gmail.com was not started after multiple tries. "
        super().__init__(message)


class SenderException(Exception):

    def __init__(self, sender_addr: str) -> None:
        message = f"Sender {sender_addr} was not accepted by the server. "
        super().__init__(message)


class RecipientException(Exception):

    def __init__(self, recipient_addr:str) -> None:
        message = f"Recipient {recipient_addr} was not accepted by the server. "
        super().__init__(message)


class MailException(Exception):

    def __init__(self) -> None:
        message = "The e-mail content was not accepted by the server. "
        super().__init__(message)


class DataException(Exception):

    def __init__(self) -> None:
        message = "The server didn't accept the data. "
        super().__init__(message)


class UnauthenticatedException(Exception):

    def __init__(self) -> None:
        message = """To call send_mail(), you need first call 
                    validate_credentials() and make sure that
                    you are authenticated. """
        super().__init__(message)