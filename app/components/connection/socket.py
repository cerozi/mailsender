"""
    MailClientSocket é a classe coração para 
    a conexão entre a nossa máquina e o servidor
    do Gmail.
"""

import socket
from ssl import SSLSocket, create_default_context

from typing import Tuple

from app.components.connection.comands import HELO_CMD
from app.exceptions.exceptions import ConnectionException, HeloException


class MailClientSocket:

    DOMAIN = 'smtp.gmail.com'
    PORT = 465
    ENCODING = 'ascii'
    MAX_BYTES = 8162
    CRLF = "\r\n"
    MAX_HELO_TRY = 5

    def __init__(self) -> None:

        """
            Cria um Socket cliente que faz a comunicação
            diretamente com o socket servidor smtp.gmail.com.
        """

        self.__sock = self.__set_sock()
        self.__file = self.__sock.makefile('rb')
        self.__connected = False
        self.__available = False

    def __set_connected(self) -> None:

        """
            Sinaliza que o socket cliente está
            conectado com o servidor.
        """

        self.__connected = True
        print("Conexão estabelecida!")

    def __set_available(self) -> None:

        """
            Sinaliza que o servidor está
            disponível.
        """

        self.__available = True
        print("O servidor está disponível para receber chamadas!")

    def __send(self, msg: str):

        """
            Envia o comando para o servidor e
            retorna sua resposta.

                Args:
                    >>> msg: Comando para enviar ao socket.
        """

        self.__docmd(msg)
        return self.__get_reply()

    def send_cmd(self, msg: str):

        """
            Antes de enviar o comando para o socket
            servidor, checa se os sockets estão conectados
            e se o socket servidor está disponível.

                Args:
                    >>> msg: Comando para enviar ao socket.
        """

        if not self.__connected or not self.__available:
            self.start_conn()

        return self.__send(msg)
    
    def __send_hello(self) -> None:

        """
            Envia o comando HELO para o servidor. Se este
            retornar um código diferente de 250 (código que
            sinaliza sucesso), não há nenhum retorno. Caso
            houver sucesso, o estado da conexão é setado
            como disponível
        """

        _client = socket.gethostbyname(socket.gethostname()) 
        cmd = HELO_CMD % _client
        code, _ = self.__send(cmd)
        
        if code != 250:
            return

        return self.__set_available()
    
    def __docmd(self, msg) -> None:

        """
            Codifica os dados e os envia. A codificação
            serve para aumentar a segurança no envio/tráfego
            da informação pela rede.
        """

        msg = f'{msg}{self.CRLF}'.encode(self.ENCODING)
        self.__sock.sendall(msg)

    def __get_reply(self) -> Tuple[int, str]:

        """
            Retorna a resposta do servidor. 
            
            Esta função é chamada apenas após o envio de 
            um comando do socket client ao servidor.

                Returns:
                    (250, b'smtp.gmail.com is available for new calls.')
        """

        msg = list()
        
        while (True):

            # lê os bytes enviados como resposta pelo servidor 
            bytes_line = self.__file.readline(8162)
            
            # guarda o código resposta do servidor
            code = bytes_line[:3]
            msg.append(bytes_line[4:].strip(b' \t\r\n'))
            
            # caso a resposta for multi-linhas
            if bytes_line[3:4] != '-':
                break
                
        # retorna a mensagem e o código referente à resposta do servidor
        bytes_msg = b"\n".join(msg)
        return (int(code), repr(bytes_msg))

    def start_conn(self) -> None:

        """
            Inicia a conexão com socket do smtp.gmail.com.
            
            Primeiro é estabelecida a conexão com o servidor; Caso essa conexão não tenha êxito, 
            a exceção ConnectionException() é levantada. Em seguida, envia o comando HELO para 
            que o servidor esteja ciente que novas requisições estão por vir. Caso esse comando 
            falhe, algumas novas tentativas são feitas e, se em nenhuma dessas houver sucesso, a 
            exceção HeloException() é levantada.
        """

        if not self.__connected:
            self.__conn()

        if not self.__available:
            self.__hello()

    def __hello(self) -> None:

        """
            Envia o comando HELO para o servidor. Se este não aceitar,
            tenta fazer o envio mais algumas vezes. Caso não houver 
            sucesso em nenhuma destas, a exceção HeloException() é
            levantada
        """

        requests = 0 
        while not self.__available:
            self.__send_hello()
            requests += 1

            if requests >= self.MAX_HELO_TRY:
                raise HeloException()
        
    def __conn(self) -> None:

        """
            Estabelece a conexão entre o nosso socket cliente
            com o socket do servidor do gmail. Caso essa conexão
            não tiver êxito, levanta uma exceção. Caso contrário,
            seta o socket para conectado.
        """

        self.__sock.connect((self.DOMAIN, self.PORT))
        code, _ = self.__get_reply()
        
        if code != 220:
            self.__sock.close()
            raise ConnectionException()
        
        return self.__set_connected()

    def __set_sock(self) -> SSLSocket:

        """
            Cria um socket e usa um wrapper para
            tornar este socket seguro e criptografado.
        """

        context = create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname = self.DOMAIN, do_handshake_on_connect = False)

        return ssl_sock

    def close(self) -> None:

        """
            Fecha a conexão entre os sockets.
        """

        print("[CONNECTION] Fechando conexão...")
        return self.__sock.close()
