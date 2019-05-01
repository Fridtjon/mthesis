import sys
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import time

def average_heatmap(heatmap, seconds):
	for i in range(len(heatmap)):
		for j in range(len(heatmap[i])):
			heatmap[i][j] = heatmap[i][j]/seconds
	return heatmap

def printable_timestamp(ts, resol):
	ts_sec = ts // resol
	ts_subsec = ts % resol
	ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
	return '{}.{}'.format(ts_sec_str, ts_subsec)

def timeassec(ts, resol):
	ts_sec = ts // resol
	ts_subsec = ts % resol
	return float(f'{ts_sec}.{ts_subsec}')

def write_heatmap(heatmap, instances, name, info=None):
	file = open(f'{name}.txt', 'w')
	file.write("\n")
	if info:
		file.write(f"#{info}\n")

	file.write("\t")
	for instance in instances:
		file.write(f'{instance}\t')
	file.write("\n")

	for i in range(len(heatmap)):
		for j in range(len(heatmap[i])):
			#if j == 0:
				#file.write(instances[i])
			
			info = heatmap[i][j]
			file.write(f'{str(info).replace(".",".")}\t')
		file.write("\n")
	file.write("\n")
	file.close()


def print_heatmap(heatmap, instances, info=None):
	print()
	if info:
		print(f"#{info}")

	print("\t", end="")
	for instance in instances:
		print(f'{instance}\t', end ="")
	print()

	for i in range(len(heatmap)):
		for j in range(len(heatmap[i])):
			#if j == 0:
				#print(instances[i], end ="\t")
			
			info = heatmap[i][j]
			print(f'{str(info).replace(".",".")}\t', end = "")
		print("")
	print()


def process_pcap(file_name, VERBOSE = False):
	if VERBOSE:
		print('Opening {}...'.format(file_name))

	ip_srcs = []
	ip_dsts = []
	instances = ['193.157.198.10','158.39.75.116', '158.37.63.164', '158.37.63.165', '158.37.63.175', '158.37.63.184']
	
	#   Logical heatmap
	#
	#     -		1 > 2	1 > 3	1 > 4	1 > 5
	#	2 > 1	  -  	2 > 3	2 > 4	2 > 5
	#	3 > 1	3 > 2	  -  	3 > 4	3 > 5
	#	4 > 1	4 > 2	4 > 3	  -  	4 > 5
	#	5 > 1	5 > 2	5 > 3	5 > 4	  -  
	#
	#   heatmap[sender][receiver]
	

	heatmap_p = [[0 for _ in instances] for _ in instances]
	heatmap_d = [[0 for _ in instances] for _ in instances]

	count = 0
	count_2 = 0
	non_ip = 0
				#	(src, dst, seq)
	counted_packets = []
	for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
		ether_pkt = Ether(pkt_data)
		if 'type' not in ether_pkt.fields:
			continue

		#ignore non ipv4 packets
		if ether_pkt.type != 0x0800:
			continue

		ip_pkt = ether_pkt[IP]

		# if not IP
		if ip_pkt.proto != 6:
			non_ip += 1
			ip_pkt.show()
			#print(f"{ip_pkt.src} -> {ip_pkt.dst}")
			continue

		if ip_pkt.src not in ip_srcs:
			ip_srcs.append(ip_pkt.src)

		if ip_pkt.dst not in ip_dsts:
			ip_dsts.append(ip_pkt.dst)

		if ip_pkt.dst in instances and ip_pkt.src in instances:
			i_src = instances.index(ip_pkt.src)
			i_dst = instances.index(ip_pkt.dst)
			tcp_pkt = ip_pkt[TCP]
			seqno = tcp_pkt.seq
			p_id = (i_src, i_dst, seqno)
			#ip_pkt.show()
			if p_id not in counted_packets:
				#counted_packets.append(p_id)
				heatmap_p[i_src][i_dst] += 1
				heatmap_d[i_src][i_dst] += ip_pkt.len

				count_2 += 1
			#print(ip_pkt.len)
				
		else:
			ip_pkt.show()

		count += 1

		if count == 1:
			first_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
			first_pkt_timestamp_resolution = pkt_metadata.tsresol
			first_pkt_ordinal = count

		last_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
		last_pkt_timestamp_resolution = pkt_metadata.tsresol
		last_pkt_ordinal = count

	f = open("infomation.txt", 'w')
	if VERBOSE:
		f.write('{} contains {} packets\n'.format(file_name, count))
		f.write('{} contains {} non-ip packets\n'.format(file_name, non_ip))
		f.write(f"SRC: {ip_srcs} \nDST: {ip_dsts}\n")
		f.write(f"Non-duplicate packets: {count_2 / 2}\n")


	tot_time = timeassec(last_pkt_timestamp - first_pkt_timestamp, first_pkt_timestamp_resolution)
	
	if VERBOSE:
		write_heatmap(heatmap_p, instances, "PTOT", "Packets sent and reveived")
		write_heatmap(average_heatmap(heatmap_p, tot_time), instances, "PAVG", "Average packets sent / reveived per second.")


		write_heatmap(heatmap_d, instances, "DTOT", "Data sent and reveived")
		write_heatmap(average_heatmap(heatmap_d, tot_time), instances, "DAVG", "Average data sent / received per second.")
	
		
		f.write('First packet in connection: Packet #{} {}\n'.format(first_pkt_ordinal,printable_timestamp(first_pkt_timestamp,first_pkt_timestamp_resolution)))

		f.write('Last packet in connection: Packet #{} {}\n'.format(last_pkt_ordinal, printable_timestamp(last_pkt_timestamp, last_pkt_timestamp_resolution)))

		f.write(f'Total time used: {timeassec(last_pkt_timestamp - first_pkt_timestamp, first_pkt_timestamp_resolution)}\n')
	return (heatmap_p, heatmap_d)

if __name__ == '__main__':
	VERBOSE = False
	if len(sys.argv) < 2:
		print("PROVIDE A FILE")
		exit()
	if len(sys.argv) >= 3:
		print("Verbose mode on.")
		VERBOSE = True

	process_pcap(sys.argv[1], VERBOSE=True)
