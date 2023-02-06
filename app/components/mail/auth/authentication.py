from app.components.mail.auth.credentials import Credentials
from typing import Tuple

class Authentication:

    def __init__(self) -> None:

        """
            Gerencia a autenticação do usuário.

            Atráves dessa classe, administra o login
            do usuário e sinaliza se este possui credenciais
            válidas para o envio do e-mail.
        """

        self.__authenticated = False

    def set_credentials(self, username: str, password: str) -> Credentials:

        """
            Quando a autenticação é válida, cria um
            objeto do model Credentials que guarda o
            username e a senha do usuário.

                Args:
                    >>> username: E-mail da conta.
                    >>> password: Senha da conta.
        """

        self.__credentials = Credentials(username, password)
        self.set_authenticated(True)

    def set_authenticated(self, b: bool) -> None:

        """
            Seta o estado de autenticação
            do usuário.

                Args:
                    >>> b: Booleano.
        """

        self.__authenticated = b

    def get_credentials(self) -> Tuple[str]:

        """
            Retorna as credenciais do usuário.

                Returns:
                
                        username            senha
                    ('mcerozi@gmail.com', 'i#P58zZZ')
        """

        return self.__credentials.get_credentials()

    def is_authenticated(self) -> bool:

        """
            Retorna o estado de autenticação
            do usuário.
        """

        return self.__authenticated

    def not_authenticated_message(self) -> None:
        print("[LOGIN] usuário não autenticado. ")

    def authenticated_message(self) -> None:
        print("[LOGIN] usuário autenticado com sucesso! ")