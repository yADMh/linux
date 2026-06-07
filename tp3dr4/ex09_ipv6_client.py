# ex09_ipv6_client.py

import socket

sock = socket.socket(
    socket.AF_INET6,
    socket.SOCK_STREAM
)

sock.connect(("::1", 12345))

sock.sendall(
    b"Teste IPv6"
)

sock.close()
