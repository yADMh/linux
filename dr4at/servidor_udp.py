import socket
import random

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(("0.0.0.0",6000))

while True:

    dados,addr=s.recvfrom(1024)

    print("Recebido:",dados.decode())

    if random.random()<0.5:
        print("ACK perdido")
    else:
        s.sendto(b"ACK",addr)
        print("ACK enviado")
        
        
