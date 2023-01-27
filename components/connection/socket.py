import socket
from ssl import SSLSocket, create_default_context
from exceptions.exceptions import ConnectionException, HeloException
from typing import Tuple
from components.connection.comands import HELO_CMD


class MailClientSocket:

    DOMAIN = 'smtp.gmail.com'
    PORT = 465
    ENCODING = 'ascii'
    MAX_BYTES = 8162
    CRLF = "\r\n"
    MAX_HELO_TRY = 5

    def __init__(self) -> None:
        self.__sock = self.__set_sock()
        self.__file = self.__sock.makefile('rb')
        self.__available = False
        
        self.__check_conn()
        self.__send_helo()
    
    def __set_available(self) -> None:
        self.__available = True
        print("[CONNECTION] O servidor @gmail.com está pronto para receber chamadas.")

    def __send(self, msg: str):
        self.__docmd(msg)
        return self.__get_reply()

    def send_cmd(self, msg: str) -> Tuple[int, str]:
        requests = 0 
        while not self.__available:
            self.__send_helo()
            requests += 1

            if requests >= self.MAX_HELO_TRY:
                raise HeloException()

        return self.__send(msg)
    
    def __send_helo(self) -> Tuple[int, str]:
        _client = socket.gethostbyname(socket.gethostname()) 
        cmd = HELO_CMD % _client
        code, _ = self.__send(cmd)
        
        if code == 250:
            self.__set_available()
    
    def __docmd(self, msg) -> None:
        msg = f'{msg}{self.CRLF}'.encode(self.ENCODING)
        self.__sock.sendall(msg)

    def __get_reply(self):
        msg = list()
        
        while (True):
            bytes_line = self.__file.readline(8162)
            
            code = bytes_line[:3]
            msg.append(bytes_line[4:].strip(b' \t\r\n'))
            
            if bytes_line[3:4] != '-':
                break
                
        bytes_msg = b"\n".join(msg)
        return (int(code), repr(bytes_msg))
        
    def __check_conn(self) -> SSLSocket:
        self.__sock.connect((self.DOMAIN, self.PORT))
        code, _ = self.__get_reply()
        
        if code != 220:
            self.__sock.close()
            raise ConnectionException()
        
        print(f"[CONNECTION] conexão com o {self.DOMAIN} estabelecida!")
        return self.__sock

    def __set_sock(self) -> SSLSocket:
        context = create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname = self.DOMAIN, do_handshake_on_connect = False)

        return ssl_sock

    def close(self) -> None:
        print("[CONNECTION] Fechando conexão...")
        self.__sock.close()