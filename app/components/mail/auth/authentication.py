from app.components.mail.auth.credentials import Credentials
from typing import Tuple

class Authentication:

    def __init__(self) -> None:
        self.__authenticated = False

    def set_credentials(self, username: str, password: str) -> Credentials:
        self.__credentials = Credentials(username, password)
        self.set_authenticated(True)

    def set_authenticated(self, b: bool) -> None:
        self.__authenticated = b

    def get_credentials(self) -> Tuple[str]:
        return self.__credentials.get_credentials()

    def is_authenticated(self) -> bool:
        return self.__authenticated

    def not_authenticated_message(self) -> None:
        print("[LOGIN] usuário não autenticado. ")

    def authenticated_message(self) -> None:
        print("[LOGIN] usuário autenticado com sucesso! ")