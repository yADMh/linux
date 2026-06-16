from scapy.all import sniff, TCP, Raw
from collections import defaultdict

ARQUIVO_LOG = "acessos.log"

def analisar_logs():

    contagem = defaultdict(int)

    try:

        with open(ARQUIVO_LOG, "r") as f:

            for linha in f:

                campos = linha.strip().split(",")

                if len(campos) < 5:
                    continue

                ip = campos[1]
                endpoint = campos[3]
                status = campos[4]

                if status == "404":

                    chave = (ip, endpoint)

                    contagem[chave] += 1

        for chave, total in contagem.items():

            ip, endpoint = chave

            if total >= 3:

                print("\n*** ANOMALIA DETECTADA ***")
                print(f"IP: {ip}")
                print(f"Endpoint: {endpoint}")
                print(f"Tentativas inválidas: {total}")

    except FileNotFoundError:
        pass

def capturar_http(pkt):

    if pkt.haslayer(TCP) and pkt.haslayer(Raw):

        try:

            payload = pkt[Raw].load.decode(
                errors="ignore"
            )

            if payload.startswith("GET"):

                primeira = payload.split("\r\n")[0]

                print(
                    "[HTTP]",
                    pkt["IP"].src,
                    "->",
                    primeira
                )

        except:
            pass

        analisar_logs()

print("Capturando HTTP na porta 8080...")

sniff(
    filter="tcp port 8080",
    prn=capturar_http,
    store=False
)
