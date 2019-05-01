import os, sys

def main():
	if len(sys.argv) != 3:
		print("Usage: scprToAll.py source dest")
	ip_addrs = ["158.39.75.116", "158.37.63.164", "158.37.63.165", "158.37.63.175", "158.37.63.184"]
	source = os.path.normpath(sys.argv[1])
	dest = os.path.normpath(sys.argv[2])
	print("Transfering " + source + " to " + dest + ".")
	for ip_addr in ip_addrs:
		print(os.system("scp -r '"+ source + "' fabusr@" + ip_addr + ":" + dest))
	print("All good. Exiting...")

main()