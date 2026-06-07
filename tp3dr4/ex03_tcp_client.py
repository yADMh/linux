# ex03_tcp_client.py

import socket

HOST = "127.0.0.1"
PORT = 12345

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect((HOST, PORT))

print("Cliente:", sock.getsockname())

msg = "Mensagem TCP"

sock.sendall(msg.encode())

resp = sock.recv(1024)

print(resp.decode())

sock.close()
