from scapy.all import *
import sys
import struct
import os
import random
from myGeo_header import *
from sender import *
from data import *
from myATP import *
from mynetcache import *
from my_zjvlan import *

class Dev:
    def __init__(self) -> None:
        self.iface_list = []
        if os.name == 'windows':
            import wmi
            w=wmi.WMI()
            iface_list=[]
            ifacelist=w.Win32_NetworkAdapterConfiguration ()
            for interface in ifacelist :
                iface_desc=interface.Description
                iface_list.append(iface_desc)
        elif os.name == 'posix':
            print("linux")
            for root, dirs, files in os.walk("/sys/class/net"):
                for dir in dirs:
                    self.iface_list.append(dir)
            self.iface_list = self.iface_list

    def get_iface_desc(self):
        return self.iface_list

def link(sender, data):
    # bind network type to pkt
    sender.bind(NetworkType.IPV4, data.pkt)
    sender.bind(NetworkType.GEO, data.pkt1)
    sender.bind(NetworkType.IPV6, data.pkt2)
    sender.bind(NetworkType.POWERLINK, data.pkt6)
    sender.bind(NetworkType.MF, data.pkt7)
    sender.bind(NetworkType.DSTMAC, [data.pkt8, data.pkt9])
    sender.bind(NetworkType.SRCMAC, data.pkt10)
    sender.bind(NetworkType.DSTIPV4, data.pkt)
    sender.bind(NetworkType.DSTIPV4_DSTMAC, data.pkt11)
    sender.bind(NetworkType.IPV4_PROT, data.pkt12)

# main process
if __name__ == "__main__":
    dev = Dev()
    opt = Opt()
    opt.set_iface_by_dev(dev)
    opt.set_network_type_by_input()
    opt.set_count_by_input()

    sender = Sender(opt)
    data = Data()
    link(sender, data)

    # send pkt
    sender.send(opt)


