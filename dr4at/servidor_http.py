import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080

ARQUIVO_LOG = "acessos.log"

def registrar_log(ip, metodo, endpoint, status):
    with open(ARQUIVO_LOG, "a") as f:
        f.write(
            f"{datetime.now()},{ip},{metodo},{endpoint},{status}\n"
        )

def montar_resposta(status, corpo):
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(corpo.encode())}\r\n"
        f"\r\n"
        f"{corpo}"
    )

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print(f"Servidor HTTP iniciado na porta {PORT}")

while True:

    conn, addr = server.accept()

    requisicao = conn.recv(4096).decode(errors="ignore")

    if not requisicao:
        conn.close()
        continue

    linhas = requisicao.split("\r\n")

    try:
        metodo, endpoint, versao = linhas[0].split()
    except:
        conn.send(
            montar_resposta(
                "400 Bad Request",
                "<h1>400 Bad Request</h1>"
            ).encode()
        )
        conn.close()
        continue

    idioma = "pt"

    for linha in linhas:
        if linha.lower().startswith("accept-language:"):
            if "en" in linha.lower():
                idioma = "en"

    status = "200 OK"

    if endpoint == "/home.html":

        if idioma == "pt":
            corpo = "<h1>Página Inicial</h1>"
        else:
            corpo = "<h1>Home Page</h1>"

    elif endpoint == "/contato.html":

        if idioma == "pt":
            corpo = "<h1>Contato</h1>"
        else:
            corpo = "<h1>Contact</h1>"

    else:
        status = "404 Not Found"

        if idioma == "pt":
            corpo = "<h1>Página não encontrada</h1>"
        else:
            corpo = "<h1>Page not found</h1>"

    resposta = montar_resposta(status, corpo)

    conn.send(resposta.encode())

    registrar_log(
        addr[0],
        metodo,
        endpoint,
        status.split()[0]
    )

    print(
        f"{addr[0]} {metodo} {endpoint} -> {status}"
    )

    conn.close()
