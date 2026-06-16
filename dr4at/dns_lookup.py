import dns.resolver

dominio = "www.google.com"

print("Registros A:")
for resposta in dns.resolver.resolve(dominio, "A"):
    print(resposta)

print("\nRegistros AAAA:")
for resposta in dns.resolver.resolve(dominio, "AAAA"):
    print(resposta)
