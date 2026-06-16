from scapy.all import *

def pkt(p):
    if p.haslayer(TCP):
        print(p.summary())

sniff(filter="tcp port 5000",prn=pkt)
