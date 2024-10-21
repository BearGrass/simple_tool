from scapy.all import *
from  myGeo_header import *
from myATP import *
import random

TYPE_GEO = 0x080A
#pad1 = "00000001000000c9c0a81eb8"
pad1 = "00000001c0a81eb800000069"
pad_decode1 = bytes.fromhex(pad1)
netflow =  NetflowHeader()/NetflowHeaderV1()/NetflowRecordV1()

class Calc(Packet):
    name = "MyCalc"
    fields_desc = [StrLenField("Pad","0")]

class geth():
    def __init__(self, src, dst, type) -> None:
        self.src = src
        self.dst = dst
        self.type = type

class gip():
    def __init__(self, src, dst) -> None:
        self.src = src
        self.dst = dst

class gudp():
    def __init__(self, sport, dport) -> None:
        self.sport = sport
        self.dport = dport

class Data():
    def __init__(self) -> None:
        self.pkts = {}
        Maclist = []
        for i in range(1, 20):
            RANDSTR = "".join(random.sample("0123456789abcdef", 2))
            Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        pad2 = "19a5d8"
        pad_decode2 =  bytes.fromhex(pad2)       
        data = 'dataasdfasdfsfasdfadfadsdfva'
        data1='4d4fa2a5dbb4fbecd6e05851c8585625cea624acaa73f49f00403522e86a85e7'

        self.pkt = Ether(src="54:B2:03:91:14:26",dst="54:B2:03:91:33:03")/\
                IP(src='169.254.30.57', dst='169.254.131.41')/\
                data
        
        self.pkt1 =Ether(src="00:0c:29:ab:6d:43",dst="b4:96:91:8d:7c:ac")/\
                MyGeo_gbc()/gbc()/\
                data
        self.pkt2 = Ether(src="54:B2:03:91:32:A0",dst="54:B2:03:91:30:9C")/\
                IPv6(src='1234::5678:9012:3456:7891', dst='fe80::e695:6eff:fe2f:2278')\
                /\
                data
        self.pkt3 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/Dot1Q(vlan=4)/\
                IP(src='192.168.40.182', dst='192.168.30.181',chksum=1)/\
                data
        self.pkt4 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
                data
        self.pkt5 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
                IP(src='192.168.70.182', dst='192.168.30.182')/\
                data
        self.pkt6 = Ether(src="00:e0:4c:68:3c:95",dst="00:e0:4c:68:3c:92",type=0x88ab)/Calc(Pad = pad_decode2)/data
        self.pkt7 = Ether(src="00:e0:4c:68:3c:95",dst="00:e0:4c:68:3c:93",type=0x27c0)/Calc(Pad =  bytes.fromhex("0000000100000066c0a81eb8"))/data
        
        self.pkt8 = Ether(src=RANDMAC, dst="00:e0:4c:68:3c:92") / \
                        IP(src='192.168.40.182', dst='192.168.30.182') / \
                        data
        self.pkt9 = Ether(src=RANDMAC, dst="00:e0:4c:68:3c:95") / \
                        IP(src='192.168.40.182', dst='192.168.30.182') / \
                        data
        
        self.pkt10 = Ether(src="00:e0:4c:68:3c:93", dst=RANDMAC) / \
                IP(src='192.168.40.182', dst='192.168.30.182') / \
                data
        
        self.pkt11 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
                IP(src='192.168.40.182', dst='192.168.30.182')/\
                TCP(sport=100,dport=200)/\
                data
        self.pkt12 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
                IP(src='192.168.40.182', dst='192.168.30.182')/\
                data
    def gen_l2_pkt(self, name, eth, data):
        if self.pkts.get(name) is None:
            self.pkts[name] = []
            self.pkts[name].append(Ether(src=eth.src, dst=eth.dst) / data)
    
    def gen_l3_pkt(self, name, eth, ip, data):
        if self.pkts.get(name) is None:
            self.pkts[name] = []
            self.pkts[name].append(Ether(src=eth.src, dst=eth.dst) / IP(src=ip.src, dst=ip.dst) / data)
    
    def gen_l4_udp_pkt(self, name, eth, ip, udp, data):
        if self.pkts.get(name) is None:
            self.pkts[name] = []
            self.pkts[name].append(Ether(src=eth.src, dst=eth.dst, type=eth.type) / IP(src=ip.src, dst=ip.dst) / UDP(sport=udp.sport, dport=udp.dport) / data)
        else:
            self.pkts[name].append(Ether(src=eth.src, dst=eth.dst, type=eth.type) / IP(src=ip.src, dst=ip.dst) / UDP(sport=udp.sport, dport=udp.dport) / data)