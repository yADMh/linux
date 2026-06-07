# ex01_inventario_socket.py

import socket

PORT = 12345

configs = [
    ("IPv4 TCP", socket.AF_INET, socket.SOCK_STREAM),
    ("IPv4 UDP", socket.AF_INET, socket.SOCK_DGRAM),
    ("IPv6 TCP", socket.AF_INET6, socket.SOCK_STREAM),
    ("IPv6 UDP", socket.AF_INET6, socket.SOCK_DGRAM),
]

for nome, familia, tipo in configs:
    s = None

    try:
        s = socket.socket(familia, tipo)

        if familia == socket.AF_INET:
            s.bind(("127.0.0.1", PORT))
        else:
            s.bind(("::1", PORT))

        if tipo == socket.SOCK_STREAM:
            s.listen(1)

        print(f"[OK] {nome}")

    except Exception as e:
        print(f"[ERRO] {nome}: {e}")

    finally:
        if s:
            s.close()
