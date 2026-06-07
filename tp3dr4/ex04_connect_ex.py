# ex04_connect_ex.py

import socket
import time

host = "127.0.0.1"

portas = [22, 80, 9999]

for porta in portas:

    s = socket.socket()

    inicio = time.time()

    codigo = s.connect_ex((host, porta))

    fim = time.time()

    print(
        f"Porta={porta} "
        f"Retorno={codigo} "
        f"Tempo={(fim-inicio):.5f}s"
    )

    s.close()
