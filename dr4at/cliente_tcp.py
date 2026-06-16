import socket

HOST='127.0.0.1'
PORT=5000

s=socket.socket()
s.connect((HOST,PORT))

msg="HELLO"

pacote=f"{len(msg):04d}".encode()+msg.encode()

s.send(pacote)

print(s.recv(1024).decode())

s.close()
