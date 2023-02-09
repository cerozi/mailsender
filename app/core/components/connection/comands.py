"""
    Este módulo guarda as constantes que são
    usadas nos comandos enviados para o socket do
    smtp@gmail.com.

        => AUTH_CMD: Autentica o usuário.
        => FROM_CMD: Sinaliza o sender do e-mail.
        => RCPT_CMD: Sinaliza o recipient do e-mail.
        => DATA_CMD: Sinaliza que o próximo mensagem
        será a mensagem/corpo do e-mail.
        => HELO_CMD: Após estabelecer conexão com o servidor,
        o socket executa esse comando para que o servidor
        esteja preparado para chamadas.
"""

AUTH_CMD = "AUTH PLAIN %s"
FROM_CMD = "mail FROM:%s"
RCPT_CMD = "rcpt TO:%s"
DATA_CMD = "data"
HELO_CMD = 'helo %s'