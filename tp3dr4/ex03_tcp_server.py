# ex03_tcp_server.py

import socket
import multiprocessing

HOST = "0.0.0.0"
PORT = 12345

def handle_client(conn, addr):

    ip, porta = addr

    print(f"Cliente {ip}:{porta}")

    while True:

        data = conn.recv(1024)

        if not data:
            break

        print(
            f"{ip}:{porta} -> "
            f"{data.decode()}"
        )

        conn.sendall(data)

    conn.close()

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

while True:

    conn, addr = server.accept()

    p = multiprocessing.Process(
        target=handle_client,
        args=(conn, addr)
    )

    p.start()
