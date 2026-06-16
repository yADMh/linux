import socket

HOST='0.0.0.0'
PORT=5000

s=socket.socket()
s.bind((HOST,PORT))
s.listen()

print("Servidor iniciado")

conn,addr=s.accept()
print("Cliente:",addr)

while True:
    tamanho=conn.recv(4)

    if not tamanho:
        break

    tamanho=int(tamanho.decode())

    dados=conn.recv(1024)

    recebido=len(dados)

    if recebido != tamanho:
        resposta=f"ERRO esperado={tamanho} recebido={recebido}"
    else:
        resposta=f"OK tamanho={recebido}"

    conn.send(resposta.encode())

conn.close()
