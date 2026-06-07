# ex11_file_server.py

import socket

server = socket.socket()

server.bind(("1.0.0.1", 12346))
server.listen()

conn, addr = server.accept()

nome = conn.recv(1024).decode()
tamanho = conn.recv(1024).decode()
conteudo = conn.recv(100000)

print(nome)
print(tamanho)
print(conteudo.decode())

with open(
    "recebido.txt",
    "wb"
) as f:
    f.write(conteudo)

conn.close()
