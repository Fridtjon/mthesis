from instance import Instance, Packet
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np

class PCAP:
	figid = 0
	def __init__(self, filename, owner_ip, instances={}, filt=False):
		self._filename = filename
		self._instances = instances
		self._owner_ip = owner_ip

		if filt:
			#print(instances)
			self._owner_instance = instances[owner_ip]
			assert self._owner_instance != None, "Error in PCAP init. Owner instance is none."
		else:
			self._owner_instance = Instance(owner_ip)
			self._instances = {owner_ip : self._owner_instance}

		if not owner_ip in self._instances: 
			self._instances[owner_ip] = self._owner_instance
		if not os.path.isfile(filename):
			raise OSError("File not found: {}".format(filename))

		if filename.split(".")[1] != "pcap":
			raise OSError("Wrong file ending. Expected pcap but found {}.".format(filename.split(".")[1]))

		
		self.p_file = self._read_file(filename, filt)

	def __len__(self):
		return len(self.p_file)

	def _add_packet(self, packet):
		if packet.get_sender() == self._owner_instance:
			self._owner_instance.add_sent(packet)
		elif packet.get_receiver() == self._owner_instance:
			self._owner_instance.add_rec(packet)
		else:
			print("ERROR: Got a packet, but file owner is neither sender nor reveiver")

	def _read_file(self, filename, filt):

		def extract_data(line):
			err = None
			data = line.split()
			#print(data)
			if len(data) < 5 or data[1] == "LLDP,":
				return None,None,None,None,True

			timestamp = data[0]
			try:
				sender = Instance(data[2])
				receiver = Instance(data[4])
			except Exception as e:
				sender = None
				receiver = None
				err = e
			try: 
				length = int(data[len(data) - 1])
			except:
				length = None

			return timestamp, sender, receiver, length, err

		file = str(subprocess.check_output("tcpdump -r {}".format(filename), shell=True)).split("\\n")
		instances = self._instances
		packet_file = []
		for line in file:
			timestamp, sender, receiver, length, err = extract_data(line)
			#print("{}.{}.{}.{}.{}".format(timestamp,sender, receiver, length, err))
			if err:
				continue

			cont = 0
			if str(sender) in instances:
				sender = instances[str(sender)]
			elif filt:
				#print("DAFUQ:" + str(sender))
				#print(instances)
				continue
			else:
				print("Received from: {}".format(sender))
				instances[str(sender)] = sender

			if str(receiver) in instances:
				receiver = instances[str(receiver)]
			elif filt:
				#print("DAFUQ: " +  str(receiver))
				continue
			else:
				print(f"Sent to: {receiver}")
				instances[str(receiver)] = receiver

			packet = Packet(sender, receiver, timestamp, length)
			try:
				if packet < packet:
					continue
			except:
				continue

			self._add_packet(packet)
			packet_file.append(packet)
			#print(timestamp)
		#print(instances)
		return packet_file

	def get_owner(self):
		return self._owner_instance

	def instances(self):
		return list(self._instances.keys())

	def _plot_sent(self, plt, start):
		sent = self._owner_instance.get_sent()
		plt.subplot(211)

		for receiver in sent:
			diff = [start.diff(p) for p in sent[str(receiver)]]
			length = [p._length for p in sent[str(receiver)]]
			
			timelen = [0]

			for i in range(len(diff)):
				if i != 0 and diff[i - 1] != diff[i]:
					for j in range(diff[i] - diff[i-1]):
						timelen.append(0)

				timelen[len(timelen) - 1] += length[i]

			plt.plot(timelen, label = str(receiver))
		
		plt.ylabel("Bytes Sent")
		plt.legend()

	def _plot_rec(self, plt, start):
		sent = self._owner_instance.get_rec()
		plt.subplot(212)

		for receiver in sent:
			diff = [start.diff(p) for p in sent[str(receiver)]]
			length = [p._length for p in sent[str(receiver)]]
			
			timelen = [0]

			for i in range(len(diff)):
				if i != 0 and diff[i - 1] != diff[i]:
					for j in range(diff[i] - diff[i-1]):
						timelen.append(0)

				timelen[len(timelen) - 1] += length[i]

			plt.plot(timelen, label = str(receiver))

		plt.ylabel("Bytes Received")
		plt.legend()

	def find_lowest(self):
		sent = self._owner_instance.get_sent()
		rec = self._owner_instance.get_rec()
		lowest = None
		
		for packets in sent.values():
			for p in packets:
				if not lowest or lowest > p:
					lowest = p

		for packets in rec.values():
			for p in packets:
				if not lowest or lowest > p:
					lowest = p

		#print("LOWEST: " + str(lowest))
		return lowest

	
	@staticmethod
	def FIGID():
		PCAP.figid += 1
		return PCAP.figid


	def plot(self, lowest = None, saveas=None):
		if not lowest:
			lowest = self.find_lowest()

		#plt.title(self._owner_ip)
		figid = PCAP.FIGID()
		fig = plt.figure(figid)
		#print(figid)
		info = "Instance IP: {}".format(self._owner_ip)
		fig.text(0.2, 0.93, info, fontsize=10)
		self._plot_sent(plt, lowest)
		self._plot_rec(plt, lowest)
		plt.xlabel("Time in Seconds")

		if not saveas:
			plt.show()
			plt.close()
		else:
			plt.savefig(saveas)

def test_pcap():
	p1 = PCAP("T1_INS2_001.pcap", "158.37.63.164")
	#print(p1.instances())
	#print(p1.get_owner().print_rec())
	p1.plot()
#test_pcap()