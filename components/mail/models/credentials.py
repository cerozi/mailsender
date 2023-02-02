from typing import Tuple

class Credentials:

    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password
    
    def get_credentials(self) -> Tuple[str]:
        return (self.__username, self.__password)