# ex12_http_final.py

import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080

server = socket.socket()
server.bind((HOST, PORT))
server.listen()

while True:

    conn, addr = server.accept()

    req = conn.recv(1024).decode()

    linha = req.splitlines()[0]

    path = linha.split()[1]

    print(
        datetime.now(),
        addr,
        path
    )

    if path == "/":

        status = "200 OK"
        body = "OK"

    elif path == "/admin":

        status = "403 Forbidden"
        body = "Forbidden"

    else:

        status = "404 Not Found"
        body = "Not Found"

    resposta = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Length:{len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    conn.sendall(
        resposta.encode()
    )

    conn.close()
