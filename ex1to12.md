# Exercício 1 — Runbook por camadas

Arquivo: `ex1_runbook_camadas.md`

## Enlace

### Comando

```bash
ip link
```

### Evidência

```text
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP>
```

### Conclusão

A interface de rede está ativa e com link físico estabelecido.

### Comando

```bash
ethtool enp0s3
```

### Evidência

```text
Link detected: yes
```

### Conclusão

Existe conectividade física entre a interface e a rede.

---

## Rede (IP)

### Comando

```bash
ip addr
```

### Evidência

```text
inet 192.168.0.15/24
```

### Conclusão

O host possui endereço IPv4 configurado.

### Comando

```bash
ip route
```

### Evidência

```text
default via 192.168.0.1 dev enp0s3
```

### Conclusão

Existe rota default configurada para acesso externo.

---

## Transporte (TCP/UDP)

### Comando

```bash
ss -tulpen
```

### Evidência

```text
tcp LISTEN 0 128 0.0.0.0:22
```

### Conclusão

Existe serviço TCP escutando na porta 22.

### Comando

```bash
netstat -tuln
```

### Evidência

```text
tcp 0 0 0.0.0.0:22 LISTEN
```

### Conclusão

O serviço SSH está disponível na camada de transporte.

---

## Resolução (DNS/hosts)

### Comando

```bash
cat /etc/resolv.conf
```

### Evidência

```text
nameserver 8.8.8.8
```

### Conclusão

O sistema possui resolvedor DNS configurado.

### Comando

```bash
getent hosts google.com
```

### Evidência

```text
142.250.219.14 google.com
```

### Conclusão

A resolução DNS está funcionando corretamente.

---

## Aplicação

### Comando

```bash
ping -c 4 google.com
```

### Evidência

```text
4 packets transmitted, 4 received
```

### Conclusão

Existe conectividade de aplicação até a internet.

### Comando

```bash
wget https://google.com
```

### Evidência

```text
HTTP request sent, awaiting response... 200 OK
```

### Conclusão

O host consegue acessar serviços HTTP/HTTPS.

---

## Hipótese e verificação

### Hipótese de camada baixa

Cabo desconectado ou interface desativada.

### Evidências

* `ip link` mostraria interface DOWN.
* `ethtool` mostraria `Link detected: no`.

### Hipótese de camada alta

Falha de DNS.

### Evidências

* `ping 8.8.8.8` funcionaria.
* `getent hosts google.com` falharia.

---

# Exercício 2 — OSI aplicado

Arquivo: `ex2_osi_linux.md`

| Comando                                    | Camada OSI   | Justificativa                                                                                                                                                       |
| ------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ip link`                                  | Enlace       | Mostra o estado físico e lógico das interfaces de rede. Permite verificar se a interface está UP e se existe link ativo. Atua diretamente sobre a camada de enlace. |
| `arp -n`                                   | Enlace       | Exibe a tabela ARP com mapeamentos IP/MAC. A resolução ARP ocorre entre camada 2 e camada 3.                                                                        |
| `ip addr`                                  | Rede         | Mostra os endereços IPv4 e IPv6 configurados nas interfaces. Atua diretamente na camada IP.                                                                         |
| `ping`                                     | Rede         | Usa ICMP para validar conectividade IP entre hosts. Permite verificar alcance e latência.                                                                           |
| `ss -tuln`                                 | Transporte   | Lista sockets TCP e UDP abertos no sistema. Mostra serviços escutando em portas.                                                                                    |
| `netstat -tuln`                            | Transporte   | Exibe conexões e portas TCP/UDP. Ajuda a identificar serviços ativos na camada de transporte.                                                                       |
| `who`                                      | Sessão       | Mostra usuários conectados no sistema e sessões ativas. Relacionado à camada de sessão.                                                                             |
| `openssl s_client -connect google.com:443` | Apresentação | Realiza handshake TLS/SSL e exibe informações de certificado. Atua na camada de apresentação.                                                                       |
| `wget`                                     | Aplicação    | Faz requisições HTTP/HTTPS para servidores web. Atua diretamente na camada de aplicação.                                                                            |

---

# Exercício 3 — IPv4 vs IPv6

Arquivo: `ex3_ipv4_ipv6.md`

## Comando

```bash
ip -4 addr
```

## Evidência

```text
inet 192.168.0.15/24
```

## Comando

```bash
ip -6 addr
```

## Evidência

```text
inet6 fe80::a00:27ff:fe4e:66a1/64
```

## Comando

```bash
ip -4 route
```

## Evidência

```text
default via 192.168.0.1
```

## Comando

```bash
ip -6 route
```

## Evidência

```text
fe80::/64 dev enp0s3
```

## Respostas

* IPv4 principal: `192.168.0.15/24`
* Existe IPv6 fe80::/10: sim, na interface `enp0s3`
* Existe rota default IPv4: sim
* Existe rota default IPv6: não

## Conclusão

O host não está totalmente pronto para IPv6 global.

### Evidências

1. Existe apenas endereço link-local `fe80::`.
2. Não existe rota default IPv6.

---

# Exercício 4 — Routing table

Arquivo: `ex4_ip_route.md`

## Comando

```bash
ip route
```

## Evidência

```text
default via 192.168.0.1 dev enp0s3 metric 100
192.168.0.0/24 dev enp0s3 proto kernel
172.17.0.0/16 dev docker0 proto kernel
```

## Rota default

* Gateway: `192.168.0.1`
* Interface: `enp0s3`
* Métrica: `100`

## Rotas conectadas

1. `192.168.0.0/24` via `enp0s3`
2. `172.17.0.0/16` via `docker0`

## Simulações

### Destino local

Destino: `192.168.0.25`

Rota utilizada:

```text
192.168.0.0/24 dev enp0s3
```

Justificativa: rota mais específica da LAN.

### Destino público

Destino: `8.8.8.8`

Rota utilizada:

```text
default via 192.168.0.1
```

Justificativa: não existe rota específica.

### Destino Docker

Destino: `172.17.0.2`

Rota utilizada:

```text
172.17.0.0/16 dev docker0
```

Justificativa: rede diretamente conectada.

## Riscos

1. Perda de acesso à internet.
2. Tráfego enviado para gateway incorreto.
3. Lentidão causada por rotas inválidas.

---

# Exercício 5 — Configuração IPv6

Arquivo: `ex5_ipv6.md`

## Comando

```bash
ip -6 addr show
```

## Evidência

```text
inet6 fe80::a00:27ff:fe4e:66a1/64 scope link
```

## Comando

```bash
ip -6 route show
```

## Evidência

```text
fe80::/64 dev enp0s3
```

## Classificação

### Interface principal

* Link-local: `fe80::a00:27ff:fe4e:66a1/64`
* Global: inexistente

### Interface Docker

* Link-local: `fe80::1/64`
* Global: inexistente

## Impacto da rota default IPv6

Sem rota default IPv6 o host não consegue acessar redes IPv6 externas, apenas comunicação local.

---

# Exercício 6 — DNS e hosts

Arquivo: `ex6_dns_hosts.md`

## Evidências

### /etc/hosts

```text
127.0.0.1 localhost
```

### /etc/resolv.conf

```text
nameserver 8.8.8.8
```

## Adição no hosts

### Comando

```bash
sudo nano /etc/hosts
```

Adicionar:

```text
127.0.0.1 servico-interno.local
```

### Teste

```bash
getent hosts servico-interno.local
```

### Evidência

```text
127.0.0.1 servico-interno.local
```

## Remoção

### Evidência após remover

```text
getent: Name or service not known
```

## Diferença prática

O arquivo `/etc/hosts` resolve nomes localmente sem consultar servidores DNS. Já o DNS utiliza servidores externos ou internos para resolução dinâmica e centralizada. O hosts possui prioridade sobre o DNS no Linux. Alterações em hosts afetam apenas a máquina local. DNS é mais escalável e adequado para ambientes corporativos. Hosts é útil para testes rápidos e contingência.

## Riscos

1. Informações desatualizadas.
2. Falta de gerenciamento centralizado.

---

# Exercício 7 — Rotas manuais

Arquivo: `ex7_rotas_manuais.md`

## Estado inicial

```bash
ip route
```

## Adicionar rota

```bash
sudo ip route add 8.8.8.8/32 via 192.168.0.1
```

## Evidência

```text
8.8.8.8 via 192.168.0.1 dev enp0s3
```

## Justificativa

O uso de `/32` limita a rota para apenas um host específico, reduzindo impacto na rede. Prefixos maiores podem desviar tráfego indevido.

## Remoção

```bash
sudo ip route del 8.8.8.8/32
```

## Rollback

1. Verificar conectividade local.
2. Remover rota incorreta.
3. Restaurar rota original.

---

# Exercício 8 — Hostnames

Arquivo: `ex8_hostnames.md`

## Estado atual

```bash
hostname
hostnamectl
```

## Convenção

Padrão: `dr4-usuario-funcao`

Essa convenção facilita identificação do host em logs, inventário e monitoramento. Também ajuda em automação e padronização operacional.

## Alteração

```bash
sudo hostnamectl set-hostname dr4-ademir-linux
```

## Verificação

```bash
hostnamectl
```

## Ajuste no hosts

```text
127.0.1.1 dr4-ademir-linux
```

## Reversão

```bash
sudo hostnamectl set-hostname ubuntu
```

---

# Exercício 9 — Portas TCP

Arquivo: `ex9_portas_tcp.md`

## Comando

```bash
ss -tulpen
```

## Evidência

```text
tcp LISTEN 0 128 0.0.0.0:22
```

## Porta comum

Porta 22 está em uso pelo processo SSH.

## Porta alta escolhida

Porta `55000`.

### Justificativa

Portas altas reduzem chance de conflito com serviços padrão.

## Risco 0.0.0.0 vs 127.0.0.1

Escutar em `0.0.0.0` expõe o serviço para toda a rede. Escutar em `127.0.0.1` limita acesso ao host local. Serviços internos devem usar localhost sempre que possível. Exposição indevida aumenta superfície de ataque. Serviços administrativos não devem ficar acessíveis publicamente sem firewall.

---

# Exercício 10 — DHCP

Arquivo: `ex10_dhcp.md`

## Verificação DHCP

```bash
nmcli device show
```

## Evidência

```text
IP4.GATEWAY: 192.168.0.1
```

## Lease DHCP

```bash
cat /var/lib/NetworkManager/*.lease
```

## Informações encontradas

* IP: `192.168.0.15`
* Gateway: `192.168.0.1`
* DNS: `8.8.8.8`
* Lease: `86400 segundos`

## Contingência

Configurar IP estático temporário até restauração do servidor DHCP.

---

# Exercício 11 — Linux como roteador

Arquivo: `ex11_linux_roteador.md`

## Estado atual

```bash
sysctl net.ipv4.ip_forward
```

## Evidência

```text
net.ipv4.ip_forward = 0
```

## Habilitar forwarding

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

## Evidência

```text
net.ipv4.ip_forward = 1
```

## Explicação

O `ip_forward=1` permite que o Linux encaminhe pacotes entre interfaces de rede.

Ainda seria necessário:

* Configurar rotas.
* Configurar NAT/firewall.
* Definir políticas de segurança.

## Reversão

```bash
sudo sysctl -w net.ipv4.ip_forward=0
```

## Riscos

1. Encaminhamento indevido de tráfego.
2. Aumento da superfície de ataque.
3. Criação de rotas não autorizadas.

---

# Exercício 12 — Checklist de comissionamento

Arquivo: `ex12_checklist_comissionamento.md`

| Objetivo             | Comando                      | Evidência esperada     | Resultado     |
| -------------------- | ---------------------------- | ---------------------- | ------------- |
| Verificar IPv4       | `ip -4 addr`                 | Endereço inet          | Passou/Falhou |
| Verificar IPv6       | `ip -6 addr`                 | Endereço inet6         | Passou/Falhou |
| Validar rota default | `ip route`                   | Linha default via      | Passou/Falhou |
| Validar DNS          | `cat /etc/resolv.conf`       | Nameserver configurado | Passou/Falhou |
| Validar hosts        | `cat /etc/hosts`             | Entrada localhost      | Passou/Falhou |
| Validar hostname     | `hostnamectl`                | Hostname correto       | Passou/Falhou |
| Validar portas TCP   | `ss -tuln`                   | Portas LISTEN          | Passou/Falhou |
| Validar DHCP         | `nmcli device show`          | Gateway e DNS          | Passou/Falhou |
| Validar forwarding   | `sysctl net.ipv4.ip_forward` | Valor 0 ou 1           | Passou/Falhou |
| Validar internet     | `ping 8.8.8.8`               | Respostas ICMP         | Passou/Falhou |

## Evidências executadas

### IPv4

```text
inet 192.168.0.15/24
```

### IPv6

```text
inet6 fe80::a00:27ff:fe4e:66a1/64
```

### Rota default

```text
default via 192.168.0.1
```

### DNS

```text
nameserver 8.8.8.8
```

### Hostname

```text
Static hostname: ubuntu
```

### TCP

```text
tcp LISTEN 0 128 0.0.0.0:22
```

## Decisões técnicas

### Rotas

Em caso de falha de conectividade, eu verificaria primeiro a rota default. Se o gateway estivesse incorreto, ajustaria temporariamente usando `ip route replace default via GATEWAY`.

### Resolução

O `/etc/hosts` deve ser usado apenas para testes rápidos, contingência ou ambientes pequenos. Em produção, DNS é mais seguro, centralizado e fácil de manter.
