from components.connection.socket import MailClientSocket
from email.base64mime import body_encode as encode_base64

class MailManager:

    def __init__(self) -> None:
        self.__sock = MailClientSocket()

    def auth(self, username: str, password: str) -> None:
        credentials = "\0%s\0%s" % (username, password)
        encrypt = encode_base64(credentials.encode(MailClientSocket.ENCODING), eol='')
        code, _ = self.__sock.send_cmd(f"AUTH PLAIN {encrypt}")

        if code == 235:
            return self.__success_auth()

        return self.__invalid_auth()

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