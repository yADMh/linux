# ex02_udp_client.py

import socket
import random
import string

HOST = "127.0.0.1"
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(10):

    tamanho = random.randint(10, 2000)

    conteudo = ''.join(
        random.choices(
            string.ascii_letters,
            k=tamanho
        )
    )

    msg = f"{i} - {conteudo}"

    sock.sendto(msg.encode(), (HOST, PORT))

    resposta, _ = sock.recvfrom(4096)

    print(resposta.decode()[:60])

sock.close()
