# ex02_udp_server.py

import socket

HOST = "0.0.0.0"
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Servidor UDP ouvindo em {PORT}")

while True:
    data, addr = sock.recvfrom(4096)

    ip, porta = addr

    print(
        f"IP={ip} "
        f"PORTA={porta} "
        f"TAMANHO={len(data)}"
    )

    print(data.decode())

    sock.sendto(data, addr)
