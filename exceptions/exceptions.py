class ConnectionException(Exception):
    
    def __init__(self) -> None:
        message = "Connection unsuccesfull. "
        return super().__init__(message)

class HeloException(Exception):

    def __init__(self) -> None:
        message = "The @gmail.com was not started after multiple tries."
        super().__init__(message)