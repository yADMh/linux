# ex11_file_client.py

import socket
import os

arquivo = "teste.txt"

with open(arquivo, "rb") as f:
    conteudo = f.read()

sock = socket.socket()
sock.connect(("1.0.0.1", 12346))

sock.send(arquivo.encode())
sock.send(str(len(conteudo)).encode())
sock.send(conteudo)

sock.close()
