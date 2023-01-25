import socket
from ssl import SSLSocket, create_default_context
from exceptions.exceptions import ConnectionException
from typing import Tuple
class MailClientSocket:

    DOMAIN = 'smtp.gmail.com'
    PORT = 465
    ENCODING = 'ascii'
    MAX_BYTES = 8162
    CRLF = "\r\n"

    def __init__(self) -> None:
        self.__sock = self.__set_sock()
        self.__file = self.__sock.makefile('rb')
        self.__clienthost = socket.gethostbyname(socket.gethostname()) 
        self.__available = False

        if not self.__check_conn():
            self.__sock.close()
            raise ConnectionException()
            
        self.__send_helo()

    def send_cmd(self, msg: str) -> Tuple[int, str]:
        self.__docmd(msg)
        return self.__get_reply()
    
    def __send_helo(self) -> Tuple[int, str]:
        cmd = f'helo {self.__clienthost}'
        code, _ = self.send_cmd(cmd)
        
        if code == 250:
            self.__available = True
            print('[CONNECTION] Servidor @gmail.com disponível para chamadas. ')
    
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
        
    def __check_conn(self) -> bool:
        self.__sock.connect((self.DOMAIN, self.PORT))
        code, _ = self.__get_reply()
        
        if code != 220:
            return False
        
        print(f"[CONNECTION] conexão com o {self.DOMAIN} estabelecida!")
        return True

    def __set_sock(self) -> SSLSocket:
        context = create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname = self.DOMAIN, do_handshake_on_connect = False)

        return ssl_sock