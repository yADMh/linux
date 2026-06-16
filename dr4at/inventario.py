import nmap

scanner = nmap.PortScanner()

print("Iniciando varredura...\n")

scanner.scan(
    hosts="127.0.0.1",
    ports="1-10000",
    arguments="-sV"
)

for host in scanner.all_hosts():

    print(f"Host: {host}")
    print(f"Estado: {scanner[host].state()}")

    for proto in scanner[host].all_protocols():

        print(f"\nProtocolo: {proto}")

        portas = sorted(scanner[host][proto].keys())

        for porta in portas:

            info = scanner[host][proto][porta]

            print(
                f"Porta: {porta} | "
                f"Estado: {info['state']} | "
                f"Serviço: {info['name']}"
            )
