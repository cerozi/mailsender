class ConnectionException(Exception):
    
    def __init__(self) -> None:
        message = "Connection unsuccesfull. "
        return super().__init__(message)