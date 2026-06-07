# ex08_tls_server.py

import ssl
import socket

context = ssl.SSLContext(
    ssl.PROTOCOL_TLS_SERVER
)

context.load_cert_chain(
    "server.crt",
    "server.key"
)

sock = socket.socket()
sock.bind(("0.0.0.0", 8443))
sock.listen(5)

with context.wrap_socket(
    sock,
    server_side=True
) as server:

    conn, addr = server.accept()

    conn.send(
        b"Resposta via TLS local"
    )

    conn.close()
