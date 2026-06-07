# ex07_tls_client.py

import ssl
import socket

host = "google.com"

context = ssl.create_default_context()

with socket.create_connection((host, 443)) as sock:
    with context.wrap_socket(
        sock,
        server_hostname=host
    ) as tls:

        print("TLS:", tls.version())
        print("Cipher:", tls.cipher())

        cert = tls.getpeercert()

        print(cert)

        pem = ssl.DER_cert_to_PEM_cert(
            tls.getpeercert(binary_form=True)
        )

        print(pem)
