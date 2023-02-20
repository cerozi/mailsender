"""
    Módulo principal do pacote connection.
    A classe MailConnection() é usada como
    intermédio/API para conexão, autenticação
    e envio do e-mail.
"""

from email.base64mime import body_encode as encode_base64

from typing import Tuple, Type

from app.core.components.connection.comands import (AUTH_CMD, DATA_CMD, FROM_CMD,
                                               RCPT_CMD)
from app.core.components.connection.socket import MailClientSocket
from app.core.components.mail.models.email import Email
from app.core.exceptions.exceptions import (DataError, MailError,
                                       RecipientError, SenderError)


class MailConnection:

    def __init__(self) -> None:

        """
            Faz as operações básicas de autenticação
            e envio do e-mail a partir da conexão gerada
            pelo MailClientSocket().
        """

        self.__sock = MailClientSocket()

    def auth(self, username: str, password: str) -> bool:

        """
            Valida as credenciais de autenticação
            da conta que vai ser usada para o envio
            do e-mail.

                Args:
                    >>> username: Email da conta.
                    >>> password: Senha da conta.

                Returns:
                    True | False
        """

        # autentica o usuário
        credentials = "\0%s\0%s" % (username, password)
        encrypt = encode_base64(credentials.encode(MailClientSocket.ENCODING), eol='')
        code, _ = self.__sock.send_cmd(AUTH_CMD % encrypt)

        # valida se as credencias são válidas
        if code == 235:
            self.__set_username(username)
            return True

        return False

    def __set_username(self, username: str) -> None:

        """
            Seta o username para ser usado
            em requisições posteriores.

                Args:
                    >>> username: Email da conta logada.
        """

        self.__username = username

    def __mailfrom(self, username: str) -> Tuple[int, str]:

        """
            Especifica o remetente
            do e-mail.

                Args:
                    >>> username: Email do remetente.
        """

        addr = "<%s>" % username
        return self.__sock.send_cmd(FROM_CMD % addr)

    def __mailrecipient(self, recipient: str) -> Tuple[int, str]:

        """
            Especifica o recipiente
            do e-mail.

                Args:
                    >>> recipient: Email do destinatário.
        """

        addr = "<%s>" % recipient
        return self.__sock.send_cmd(RCPT_CMD % addr)

    def __maildata(self, message: str) -> Tuple[int, str]:

        """
            Envia o comando DATA para o servidor,
            sinalizando que a requisição será o
            corpo da mensagem do e-mail. Caso o
            servidor não responda o comando DATA
            com sucesso, a exceção DataError()
            é levantada.

                Args:
                    >>> message: Corpo do e-mail.
        """

        code, _ = self.__sock.send_cmd(DATA_CMD)
        if code != 354:
            return (code, _)

        msg = f"{message}{MailClientSocket.CRLF}."
        return self.__sock.send_cmd(msg)

    def mail(self, email: Type[Email]) -> Tuple[str, bool, None | str]:

        """
            Responsável pelo envio do e-mail. Ao enviar o e-mail,
            o seguinte fluxo é traçado:
                1. Especificar o remetente (o usuário logado)
                2. Especifica o recipiente do e-mail.
                3. Envia o comando DATA, sinalizando que
                a próxima mensagem será o corpo do e-mail.
                4. Envia o corpo do e-mail.

                Args:
                    >>> email: Instância da classe Email.
                    Esse model contém as informações do
                    recipiente e corpo da mensagem.

                Returns:
                    Informações referentes ao envio do e-mail.
                        1. Representação em string do objeto Email;
                        2. Booleano que indica se a mensagem foi enviada ou não.
                        3. Exceção gerada caso o envio não tenha sido bem sucedido.

                    ('(to: mcerozi@gmail.com, msg: 'Teste.')', True, None)
        """

        # especifica o remetente
        code, _ = self.__mailfrom(self.__username)
        if code != 250:
            return email.set_error(SenderError(self.__username))

        # especifica o recipiente
        code, _ = self.__mailrecipient(email.recipient)
        if code != 250:
            return email.set_error(RecipientError(email.recipient))

        # especifica a mensagem 
        code, _ = self.__maildata(email.message)
        if code != 250:
            return email.set_error(MailError())

        return email.set_sent()

    def close(self) -> None:

        """
            Fecha a conexão com o
            servidor do gmail.
        """

        return self.__sock.close()

    def connect(self) -> None:

        """
            Abre conexão e valida
            disponibilidade do servidor.
        """

        return self.__sock.start_conn()

    def __enter__(self):

        """
            Ao usar essa classe atráves de um 
            gerenciador de contexto, abre a conexão
            com o servidor.
        """

        self.connect()
        return self

    def __exit__(self, *args) -> None:

        """
            Fecha a conexão ao usar a classe
            atráves de um gerenciador de contexto.
        """

        return self.close()
