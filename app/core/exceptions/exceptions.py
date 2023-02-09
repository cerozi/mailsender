"""
    Este módulo guarda todas
    as exceções do projeto.
"""


class ConnectionException(Exception):

    """
        Quando a conexão com o servidor
        não é estabelecida.
    """
    
    def __init__(self) -> None:
        message = "Connection unsuccesfull. "
        return super().__init__(message)


class HeloException(Exception):

    """
        Após a conexão, o servidor espera
        pelo comando HELO para sinalizar
        disponibilidade.

        O comando HELO é enviado algumas vezes
        em caso de erro e, se este falhar todas
        essas vezes, essa exceção é gerada.
    """

    def __init__(self) -> None:
        message = "The @gmail.com was not started after multiple tries. "
        super().__init__(message)


class SenderException(Exception):

    """
        Quando o servidor recusa o e-mail
        do remetente.
    """

    def __init__(self, sender_addr: str) -> None:
        message = f"Sender {sender_addr} was not accepted by the server. "
        super().__init__(message)


class RecipientException(Exception):

    """
        Quando o servidor recusa o e-mail
        do recipiente.
    """

    def __init__(self, recipient_addr:str) -> None:
        message = f"Recipient {recipient_addr} was not accepted by the server. "
        super().__init__(message)


class MailException(Exception):

    """
        Quando o servidor recusa o conteúdo
        do e-mail.
    """

    def __init__(self) -> None:
        message = "The e-mail content was not accepted by the server. "
        super().__init__(message)


class DataException(Exception):

    """
        Antes de enviar o corpo do e-mail,
        o servidor espera o comando DATA,
        o qual sinaliza que a próxima mensagem
        será referente ao corpo do e-mail.

        Quando o comando DATA não é aceito,
        esta exceção é levantada.
    """

    def __init__(self) -> None:
        message = "The server didn't accept the data. "
        super().__init__(message)


class UnauthenticatedException(Exception):

    """
        Quando a função send_mail() da classe
        Mail é chamada e o usuário não está
        autenticado. 
    """

    def __init__(self) -> None:
        message = """To call send_mail(), you need first call 
                    validate_credentials() and make sure that
                    you are authenticated. """
        super().__init__(message)