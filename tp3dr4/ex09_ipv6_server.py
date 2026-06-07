# ex09_ipv6_server.py

import socket

server = socket.socket(
    socket.AF_INET6,
    socket.SOCK_STREAM
)

server.bind(("::1", 12345))
server.listen()

conn, addr = server.accept()

print("Conectado:", addr)

msg = conn.recv(1024)

print(msg.decode())

conn.close()
