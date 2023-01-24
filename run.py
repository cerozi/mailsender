import socket 

ADDRESS = ('smtp.gmail.com', 25)
MAX_LINE_BYTES = 8162

def get_response(mail_communication):
    line = mail_communication.readline(MAX_LINE_BYTES)
    
    msg = list()
    msg.append(line[4:].strip(b' \t\r\n'))
    msg = b"\n".join(msg)

    code = line[:3]

    return (code, msg)


# estabelecendo comunicação com o servidor gmail
conn = socket.create_connection(ADDRESS)
mail_communication = conn.makefile('rb')

code, _ = get_response(mail_communication)
if int(code) == 220:
    print("[CONEXÃO] nova conexão estabelecida...")


# fechando conexão
print("[CONEXÃO] conexão sendo fechada...")
conn.close()

