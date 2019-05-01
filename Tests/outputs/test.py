from pcapfile import savefile
from pcapfile.protocols.network import ip
from pcapfile.protocols.linklayer import *


test_num = 1
test_try = "001"
instance = 2
file = "T{}_INS{}_{}.pcap".format(test_num, instance, test_try)

print(file)
pcapfile = savefile.load_savefile(open(file, 'rb'))


for packet in pcapfile.packets:
	print(packet.timestamp)
	#try:
	eth_packet = ethernet.Ethernet(packet.raw())
	print(eth_packet)
	print(eth_packet.payload)
	#except:
	#	pass # Handle errors like a pro