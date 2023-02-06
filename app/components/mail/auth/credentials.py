from typing import Tuple

class Credentials:

    def __init__(self, username: str, password: str) -> None:

        """
            Model que guarda as credenciais
            do usuário.
        """

        self.__username = username
        self.__password = password
    
    def get_credentials(self) -> Tuple[str]:

        """
            Retorna as credenciais do usuário.

                Returns:
                    Tupla com o e-mail e senha do usuário, respectivamente.
                            ('mcerozi@gmail.com', 'i#P58zZZ')
        """

        return (self.__username, self.__password)