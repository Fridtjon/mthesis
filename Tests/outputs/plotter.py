from pcap_file import PCAP
from instance import Instance
import subprocess
import sys

def main():
	test_num = 3
	test_try = "001"
	instances = ["158.39.75.116", "158.37.63.164", "158.37.63.165", "158.37.63.175", "158.37.63.184"]
	ac_instances = {}
	for ip in instances:
		new_ins = Instance(ip + ".0")
		ac_instances[str(new_ins)] = new_ins

	instances_instances = ac_instances
	#print(instances_instances)
	pfiles = []
	lowest = None
	#print(instances_instances)

	for i in range(len(instances)):
		#if i == 3 or i == 2: #kb Skip the hacked node.
		#	continue
		instance_num = str(i+1)
		#folder = "Test{}".format(test_num)
		#test_id = "T{}_INS{}_{}".format(test_num, instance_num, test_try)
		test_id = "{}_transaction_flow".format(instance_num)
		filename = "{}.pcap".format(test_id)
		if len(sys.argv) > 1:
			filename = f"{instance_num}_{sys.argv[1]}.pcap"
		try:
			pfile = PCAP(filename, instances[i], instances=instances_instances, filt=False)
		except subprocess.CalledProcessError as e:
			print("Could not read {}.pcap".format(test_id))
		#	print(e)
			continue
		pfiles.append((test_id,pfile))

		if not lowest or pfile.find_lowest() < lowest:
			lowest = pfile.find_lowest()



	for i in range(len(pfiles)):
		#print("i:{}, {}".format(i, pfiles[i][1].instances()))
		savefile = pfiles[i][0] + ".png"
		pfiles[i][1].plot(lowest=lowest, saveas=savefile)

main()
