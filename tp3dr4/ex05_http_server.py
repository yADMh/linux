# ex05_http_server.py

import socket

HOST = "0.0.0.0"
PORT = 8080

server = socket.socket()
server.bind((HOST, PORT))
server.listen()

while True:

    conn, addr = server.accept()

    req = conn.recv(1024).decode()

    path = req.split()[1]

    if path == "/":
        body = "<h1>RAIZ</h1>"
    elif path == "/health":
        body = "<h1>HEALTH</h1>"
    else:
        body = "<h1>404</h1>"

    resposta = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    conn.sendall(resposta.encode())

    conn.close()
