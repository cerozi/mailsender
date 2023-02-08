"""
    A classe Email serve como model
    para guardar informações a respeito
    de cada e-mail que foi ou será enviado.
"""


from typing import Type, Tuple

class Email:

    def __init__(self, recipient: str, message: str) -> None:

        """
            Guarda informações à respeito do E-mail
            que posteriormente será enviado.

                Args:
                    >>> recipient: E-mail do recipient.
                    >>> message: Mensagem do e-mail.

        """

        self.recipient = recipient
        self.message = message
        self.__sent = False
        self.__errors = None

    def set_sent(self) -> 'Email':

        """
            Seta o e-mail como enviado.

                Returns:
                    Informações do e-mail.
        """

        self.__sent = True
        return self

    def set_error(self, exception: Type[Exception]) -> 'Email':

        """
            Sinaliza qual exceção que foi gerada
            ao tentar enviar o e-mail. Caso o envio
            seja bem sucedido, a exceção será None.

                Args:
                    >>> exception: Objeto da exceção que foi
                    gerada ao enviar o e-mail.

                Returns:
                    Informações do e-mail.
        """

        self.__errors = exception.__repr__()
        return self

    @property
    def errors(self) -> str | None:

        """
            Retorna a exceção gerada
            ao enviar o e-mail. Se este
            foi enviado, retorna None.
        """

        return self.__errors

    def get_info(self) -> Tuple[str, bool, None | str]:

        """
            Retorna informações referentes ao
            e-mail que foi (ou não) enviado.

                Returns:
                    Tupla contendo:
                        1. Representação em string do objeto Email;
                        2. Booleano que indica se a mensagem foi enviada ou não.
                        3. Exceção gerada caso o envio não tenha sido bem sucedido.

                        ('(to: mcerozi@gmail.com, msg: 'Teste.')', True, None)
        """

        return (
            self.__repr__(),
            self.__sent,
            self.__errors
        )

    def was_sent(self) -> bool:

        """
            Retorna se o e-mail foi enviado com
            sucesso ou não.
        """

        return self.__sent

    def __repr__(self) -> str:
        return f'(to: {self.recipient}, msg: {self.message})'
