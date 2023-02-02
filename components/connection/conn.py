from components.connection.socket import MailClientSocket
from components.connection.comands import AUTH_CMD, FROM_CMD, RCPT_CMD, DATA_CMD
from components.mail.models.email import Email
from components.mail.controller.manager import MailManager
from email.base64mime import body_encode as encode_base64
from exceptions.exceptions import SenderException, RecipientException, MailException, DataException
from typing import Tuple, Type, List


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

    def __sendmail(self, email: Type[Email]) -> bool:
        code, _ = self.__mailfrom(self.__username)
        if code != 250:
            return email.set_error(SenderException(self.__username))

        code, _ = self.__mailrecipient(email.recipient)
        if code != 250:
            return email.set_error(RecipientException(email.recipient))

        code, _ = self.__maildata(email.message)
        if code != 250:
            return email.set_error(MailException())

        return email.set_sent()

    def mail(self, mail_manager: Type[MailManager]) -> List[Tuple[str, bool, None | str]]:
        if not self.__authenticated:
            return self.__invalid_auth()
        
        return [self.__sendmail(email) for email in mail_manager.get_emails()]

    def __set_authenticated(self, username: str) -> None:
        self.__authenticated = True
        self.__username = username

    def __success_auth(self) -> None:
        print("[LOGIN] Usuário autenticado com sucesso. ")

    def __invalid_auth(self) -> None:
        print("[LOGIN] Usuário não autenticado. ")

    def close(self) -> None:
        self.__sock.close()

    def connect(self) -> None:
        self.__sock.start_conn()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()