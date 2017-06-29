import pypcap
import dpkt
a=pcap.pcap()
a.setfilter('arp')   # 可以是'tcp' 'udp' 'port 80'等过滤用的
for i,j in a:
tem=dpkt.ethernet.Ethernet(j)
print ("%s %x",i,tem)