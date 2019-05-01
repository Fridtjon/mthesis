#####
# Instance class
# This class contains an instance's IP-address, and recieved and sent packets.
##
class Instance:

	def __init__(self, IP_addr):
		self._IP_addr = Instance._sanitize_ip(IP_addr)
		self._p_rec = {}
		self._p_sent = {}

	def __str__(self):
		return self._IP_addr

	def __eq__(self, instance):
		return isinstance(instance, Instance) and self._IP_addr == instance._IP_addr

	@staticmethod
	def _sanitize_ip(IP_Port):
		splittet = IP_Port.split(".")
		split_len = len(splittet)
		ip = "{}".format(splittet[0])
		for i in range(1, split_len - 1):
			ip += ".{}".format(splittet[i])

		return ip
		'''
		assert len(splittet) >= 4, "Error in when sanitizing IP.Port address: {}. Expected four integers but got {}.".format(IP_Port, len(splittet))
		for i in range(0, 4):
			subip = splittet[i]
			try:
				int(subip)
			except Exception as e:
				raise AssertionError("Not a subip: {}".format(subip) )
		
		return "{}.{}.{}.{}".format(splittet[0], splittet[1], splittet[2], splittet[3])
		'''
	def add_rec(self, packet):
		self._add_list(self._p_rec, packet, str(packet.get_sender()))

	def add_sent(self, packet):
		self._add_list(self._p_sent, packet, str(packet.get_receiver()))

	def get_rec(self):
		return self._p_rec

	def get_sent(self):
		return self._p_sent

	def _add_list(self, p_dict, packet, IP_addr):

		if IP_addr not in p_dict:
			p_dict[IP_addr] = []

		if packet not in p_dict[IP_addr]:
			p_dict[IP_addr].append(packet)

	def print_rec(self):
		self._print_p_dict(self._p_rec)

	def print_sent(self):
		self._print_p_dict(self._p_sent)

	def _print_p_dict(self, p_dict):
		linebreak_after = 5
		for IP, packets in p_dict.items():
			print("\n----------- {} ----------".format(IP))
			linebreak = 0
			for packet in packets:
				print(packet, end=", ")
				linebreak += 1
				if linebreak % linebreak_after == 0:
					print()
			print()

class Packet:
	hID = 0

	def __init__(self, sender, receiver, timestamp, length):
		self._sender = sender
		self._receiver = receiver
		self._timestamp = timestamp
		self._length = length
		self._hID = Packet.hID
		Packet.hID += 1

	def __eq__(self, packet):
		return (self._sender == packet._sender) and (self._receiver == packet._receiver) and (self._timestamp == packet._timestamp) and (self._length == packet._length)

	def __str__(self):
		return "{}: {} > {} Length: {}".format(self._timestamp, self._sender, self._receiver, self._length)

	def __lt__(self, other):
		#print(self._timestamp)
		if int(self._timestamp.split(":")[0]) > int(other._timestamp.split(":")[0]):
			return False

		if int(self._timestamp.split(":")[1]) > int(other._timestamp.split(":")[1]):
			return False

		if float(self._timestamp.split(":")[2]) >= float(other._timestamp.split(":")[2]):
			return False

		return True

	def get_sender(self):
		return self._sender

	def get_receiver(self):
		return self._receiver

	def get_hour(self):
		return int(self._timestamp.split(":")[0])

	def get_min(self):
		return int(self._timestamp.split(":")[1])

	def get_sec(self):
		return int(float(self._timestamp.split(":")[2]))


	def diff(self, other):
		hh = (other.get_hour() - self.get_hour()) * 60 * 60
		mm = (other.get_min() - self.get_min()) * 60
		ss = (other.get_sec() - self.get_sec())
		return hh + mm + ss


def test_packet():
	i1 = Instance("192.168.1.0")
	i2 = Instance("10.0.0.0")

	p1 = Packet(i1, i2, "1:0:0.1", 20)
	p2 = Packet(i1, i2, "0:0:0.2", 20)
	print(p1 < p2)
	
	i1.print_sent()
	i2.print_sent()
	i1.print_rec()
	i2.print_rec()

def test_instance():
	i1 = Instance("192.168.1.0")
	i2 = Instance("10.0.0.0")
	i3 = Instance("8.8.8.8")

	i1.add_rec(i2, "1", 20)
	i1.add_rec(i2, "2", 10)
	i1.add_rec(i3, "2", 10)

	i1.add_rec(i2, "1", 20)
	i1.add_rec(i2, "2", 10)
	i1.add_rec(i3, "2", 10)

	i1.add_sent(i2, "1", 20)
	i1.add_sent(i2, "2", 10)
	i1.add_sent(i3, "2", 10)

	i1.add_sent(i2, "1", 20)
	i1.add_sent(i2, "2", 10)
	i1.add_sent(i3, "2", 10)

	i1.add_sent(i2, "1", 20)
	i1.add_sent(i2, "2", 10)
	i1.add_sent(i3, "2", 10)

	#i1.print_rec()
	#i1.print_sent()

	assert i1 == Instance("{}.2000".format(str(i1)))
	assert i1 != "Hello"
	assert i1 != None

#test_instance()
#test_packet()