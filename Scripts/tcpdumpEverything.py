import appscript, sys




def main():
	ip_addrs = ["158.39.75.116", "158.37.63.164", "158.37.63.165", "158.37.63.175", "158.37.63.184"]
	pcap_filename = "flow_1"
	if len(sys.argv) != 1:
		ip_addrs = []
		for i in range(1, len(sys.argv)):
			ip_addrs.append(sys.argv[i])
	i = 1

	for IP in ip_addrs:
		command = f"\"sudo tcpdump -x -i ens3 port not 22 -w {i}_{pcap_filename}.pcap\""
		appscript.app('Terminal').do_script("ssh fabusr@" + IP + " " + command)
		i += 1
if __name__ == '__main__':
	main()