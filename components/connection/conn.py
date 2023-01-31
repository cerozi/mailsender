from components.connection.socket import MailClientSocket
from components.connection.comands import AUTH_CMD, FROM_CMD, RCPT_CMD, DATA_CMD
from components.mail.models import Email
from email.base64mime import body_encode as encode_base64
from exceptions.exceptions import SenderException, RecipientException, MailException, DataException
from typing import Tuple


class MailConnection:

    def __init__(self) -> None:
        self.__sock = MailClientSocket()
        self.__authenticated = False

    def auth(self, username: str, password: str) -> None:
        credentials = "\0%s\0%s" % (username, password)
        encrypt = encode_base64(credentials.encode(MailClientSocket.ENCODING), eol='')
        code, _ = self.__sock.send_cmd(AUTH_CMD % encrypt)

        if code == 235:
            self.__set_authenticated(username)
            return self.__success_auth()

        return self.__invalid_auth()

    def __mailfrom(self, username: str) -> Tuple[int, str]:
        addr = "<%s>" % username
        return self.__sock.send_cmd(FROM_CMD % addr)

    def __mailrecipient(self, recipient: str) -> Tuple[int, str]:
        addr = "<%s>" % recipient
        return self.__sock.send_cmd(RCPT_CMD % addr)

    def __maildata(self, message: str) -> Tuple[int, str]:
        code, _ = self.__sock.send_cmd(DATA_CMD)
        if code != 354:
            raise DataException()

        msg = f"{message}{MailClientSocket.CRLF}."
        return self.__sock.send_cmd(msg)

    def __sendmail(self, sender: str, recipient: str, message: str) -> None:
        code, _ = self.__mailfrom(sender)
        if code != 250:
            raise SenderException(self.__username)

        code, _ = self.__mailrecipient(recipient)
        if code != 250:
            raise RecipientException(recipient)

        code, _ = self.__maildata(message)
        if code != 250:
            raise MailException()

    def mail(self, email: Email) -> None:
        if not self.__authenticated:
            return self.__invalid_auth()

        for recipient in email.recipients:
            self.__sendmail(sender = self.__username, recipient = recipient, message = email.message)

        return email.successfull_email()

    def __set_authenticated(self, username: str) -> None:
        self.__authenticated = True
        self.__username = username

    def __success_auth(self) -> None:
        print("[LOGIN] Usuário autenticado com sucesso. ")

    def __invalid_auth(self) -> None:
        print("[LOGIN] Usuário não autenticado. ")

    def close(self) -> None:
        self.__sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()