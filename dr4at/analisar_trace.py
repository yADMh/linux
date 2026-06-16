import re

arquivo = "trace.txt"

metodo = None
host = None
status = None
headers = []
ip = None

with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
    for linha in f:

        if not metodo:
            m = re.search(r"(GET|POST|PUT|DELETE|HEAD) ", linha)
            if m:
                metodo = m.group(1)

        if not host and "Host:" in linha:
            host = linha.split("Host:")[1].strip()

        if not status:
            m = re.search(r"HTTP/\d\.\d (\d+)", linha)
            if m:
                status = m.group(1)

        if "Connected to" in linha:
            ip = linha

        if ": " in linha:
            headers.append(linha.strip())

print("Método:", metodo)
print("Host:", host)
print("Status:", status)
print("IP remoto:", ip)

print("\nHeaders:")
for h in headers[:20]:
    print(h)
