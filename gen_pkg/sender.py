from scapy.all import *
from enum import Enum

class NetworkType(Enum):
    IPV4 = 1, "ipv4"
    GEO = 2, "geo"
    IPV6 = 3, "ipv6"
    POWERLINK = 4, "powerlink"
    MF = 5, "mf"
    ALL = 6, "all"
    DSTMAC = 7, "dstmac"
    SRCMAC = 8, "srcmac"
    DSTIPV4 = 9, "dstipv4"
    DSTIPV4_DSTMAC = 10, "dstipv4_dstmac"
    IPV4_PROT = 11, "ipv4_prot"

    def __new__(cls, value, name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._name_ = name
        return obj

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

    def get_network_type_by_value(value):
        return NetworkType._value2member_map_[value]

class Opt:
    def __init__(self) -> None:
        self.iface = None
        self.network_type = None
        self.count = None
    
    def set_iface_by_dev(self, dev):
        iface_list = dev.get_iface_desc()
        
        for times in range(0,len(iface_list)):
            print(times, iface_list[times])
        print("chose nic interface: ")
        index=int(input("index:"))
        if(index>len(iface_list)):
            print(" out of range total  interface num: ",len(iface_list)-1)
            exit(1)
        else:
            self.iface=iface_list[index]

    def get_iface(self):
        return self.iface

    def set_network_type_by_input(self):
        print("| ipv4:1 | geo:2 | ipv6:3 | powerllink:4 | mf:5 | all:6 | dstmac:7 | srcmac:8 |dstipv4:9 | dstipv4_dstmac:10 | ipv4_prot:11 |")
        self.network_type = NetworkType.get_network_type_by_value(int(input("network type:")))
    def get_network_type(self):
        return self.network_type
    
    def set_count_by_input(self):
        self.count=int(input("pkt count:"))
    
    def get_count(self):
        return self.count

class Sender:
    def __init__(self, opt):
        self.pkt_tables = {}
        for network_type in NetworkType:
            self.pkt_tables[network_type] = []
        self.count = opt.count
        self.iface = opt.iface

    def bind(self, network_type, pkts):
        for pkt in pkts:
            self.pkt_tables[network_type].append(pkt)
        if network_type == NetworkType.IPV4:
            print("bind", type(network_type))

    def send(self, opt, count=None, iface=None):
        if count is None:
            count = self.count
        if iface is None:
            iface = self.iface
        if opt.network_type == NetworkType.ALL:
            self.send_all_pkt()
        else:
            self.send_single_pkt(opt.network_type, count, iface)
        

    def send_single_pkt(self, network_type, count=None, iface=None):
        if count is None:
            count = self.count
        if iface is None:
            iface = self.iface
        for pkt in self.pkt_tables[network_type]:
            print("debug", str(network_type))
            print(pkt.show())
            sendp(pkt,inter=0,count=count,iface=iface)

    def send_all_pkt(self):
        for network_type in self.pkt_tables.keys():
            self.send_single_pkt(network_type, self.count, self.iface)
    