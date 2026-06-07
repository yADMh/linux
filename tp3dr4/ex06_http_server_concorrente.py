# ex06_http_server_concorrente.py

import socket
import multiprocessing

HOST = "0.0.0.0"
PORT = 8080


def handle_client(conn, addr):
    try:
        print(f"Nova conexão: {addr[0]}:{addr[1]}")

        request = conn.recv(1024).decode("utf-8")

        if not request:
            return

        primeira_linha = request.splitlines()[0]
        caminho = primeira_linha.split()[1]

        print(f"Requisição para: {caminho}")

        if caminho == "/":
            body = "<h1>RAIZ</h1>"
            status = "200 OK"

        elif caminho == "/health":
            body = "<h1>HEALTH</h1>"
            status = "200 OK"

        else:
            body = "<h1>404 NOT FOUND</h1>"
            status = "404 Not Found"

        response = (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )

        conn.sendall(response.encode("utf-8"))

        print(
            f"Processo {multiprocessing.current_process().pid} "
            f"atendeu {addr[0]}:{addr[1]}"
        )

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen(10)

    print(f"Servidor HTTP concorrente ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        processo = multiprocessing.Process(
            target=handle_client,
            args=(conn, addr)
        )

        processo.start()

        conn.close()


if __name__ == "__main__":
    main()
