import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.settimeout(2)

tentativa=1

while tentativa<=5:

    print("Tentativa",tentativa)

    s.sendto(b"Teste",("127.0.0.1",6000))

    try:
        resp,addr=s.recvfrom(1024)
        print("Recebido",resp.decode())
        break

    except socket.timeout:
        print("Timeout")

    tentativa+=1
