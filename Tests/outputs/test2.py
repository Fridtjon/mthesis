import subprocess
import matplotlib.pyplot as plt
from instance import Instance

def getsecfromts(timestamp):
	return int((timestamp.split(".")[0]).split(":")[2])

test_num = 1
test_try = "001"
instance = 2
file = "T{}_INS{}_{}.pcap".format(test_num, instance, test_try)
instances = ["158.39.75.116", "158.37.63.164", "158.37.63.165", "158.37.63.175", "158.37.63.184", ""]

output = subprocess.check_output("tcpdump -r {}".format(file), shell=True)

seconds = 1

from_data = []
to_data = []

curr_times = -1
curr_times2 = -1
c1 = seconds - 1
c2 = seconds - 1

debugger = []
for line in str(output).split("\\n"):
	data = line.split()
	if len(data) > 4 and data[1] == "IP":
		timestamp = data[0]
		addr_from = data[2]
		addr_to   = data[4]


		try:
			length    = int(data[len(data) - 1])
		except:
			print("Err: Length is NaN.")
			continue

		if "t:" + addr_from not in debugger:
			print("To: " + addr_from)
			debugger.append("t:" + addr_from)

		if "f:" + addr_to not in debugger:
			print("From: " + addr_to)
			debugger.append("f:" + addr_to)

		if instances[instance] in addr_from:
			cts = getsecfromts(timestamp)
			if cts != curr_times:
				curr_times = cts
				c1 += 1

			#print("{} : {}".format(c1, seconds))
			if c1 == seconds:
				c1 = 0
				
				to_data.append(0)
			
			to_data[len(to_data) - 1] += length

		else:
			cts = getsecfromts(timestamp)
			if cts != curr_times2:
				curr_times2 = cts
				c2 += 1

			if c2 == seconds:
				c2 = 0
				from_data.append(0)
			
			from_data[len(from_data) - 1] += length
			#print("TO ME")

		#print(line)
		#print("{}: {} > {} - Length: {}\n".format(timestamp, addr_from, addr_to, length))

#print(to_data)
# 0			1		2	 3 4   5	 6	 7   		 ..  len(-1)
# Timestamp NetType From > To: Flags [], ack/seq num ..  length

plt.ylabel("Data : {}".format(instances[instance]))
plt.xlabel("Time")
plt.plot(from_data, label = "Outgoing traffic")
plt.plot(to_data, label = "Incomming traffic")

plt.legend()
plt.show()
########
# 
#
#
#