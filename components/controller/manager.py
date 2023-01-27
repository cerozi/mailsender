from components.connection.socket import MailClientSocket
from email.base64mime import body_encode as encode_base64
from exceptions.exceptions import SenderException, RecipientException, MailException, DataException
from typing import Tuple

class MailManager:

    def __init__(self) -> None:
        self.__sock = MailClientSocket()
        self.__username = None

    def auth(self, username: str, password: str) -> None:
        credentials = "\0%s\0%s" % (username, password)
        encrypt = encode_base64(credentials.encode(MailClientSocket.ENCODING), eol='')
        code, _ = self.__sock.send_cmd(f"AUTH PLAIN {encrypt}")

        if code == 235:
            self.__set_username(username)
            return self.__success_auth()

        return self.__invalid_auth()

    def __mailfrom(self, username: str) -> Tuple[int, str]:
        addr = "<%s>" % username
        return self.__sock.send_cmd(f"mail FROM:{addr}")

    def __mailrecipient(self, recipient: str) -> Tuple[int, str]:
        addr = "<%s>" % recipient
        return self.__sock.send_cmd(f"rcpt TO:{addr}")

    def __maildata(self, message: str) -> Tuple[int, str]:
        code, _ = self.__sock.send_cmd("data")
        if code != 354:
            raise DataException()

        msg = f"{message}{MailClientSocket.CRLF}."
        return self.__sock.send_cmd(msg)

    def mail(self, recipient: str, message: str) -> None:
        if self.__username is None:
            return self.__invalid_auth()

        code, _ = self.__mailfrom(self.__username)
        if code != 250:
            raise SenderException(self.__username)

        code, _ = self.__mailrecipient(recipient)
        if code != 250:
            raise RecipientException(recipient)

        code, _ = self.__maildata(message)
        if code != 250:
            raise MailException()

        return self.__success_mail()

    def __set_username(self, username: str) -> None:
        self.__username = username

    def __success_mail(self) -> None:
        print("[EMAIL] E-mail enviado com sucesso! ")

    def __success_auth(self) -> None:
        print("[LOGIN] Usuário autenticado com sucesso. ")

    def __invalid_auth(self) -> None:
        print("[LOGIN] Login inválido. ")

    def close(self) -> None:
        self.__sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()