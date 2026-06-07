# ex10_port_scanner.py

import socket
import time

inicio = time.time()

for porta in range(20, 101):

    s = socket.socket()

    s.settimeout(0.5)

    resultado = s.connect_ex(
        ("127.0.0.1", porta)
    )

    if resultado == 0:
        print(
            f"Porta aberta: {porta}"
        )

    s.close()

fim = time.time()

print(
    "Tempo:",
    fim - inicio
)
