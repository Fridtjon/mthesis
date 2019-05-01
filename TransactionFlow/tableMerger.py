import sys
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


def heatmap(matrix, info, instances, title, save=None):
	
	matrix = np.array(matrix)
	plt.figure(figsize=(24, 16))
	fig, ax = plt.subplots()
	sns.heatmap(matrix,
				cmap="Reds",
				linecolor='black',
				linewidths=1,
				xticklabels= ["Inst. " + str(i) if i != 0 else "Caliper" for i in range(len(instances))],
				yticklabels= ["Inst. " + str(i) if i  != 0 else "Caliper" for i in range(len(instances))],
				annot=True,
				fmt=".1f")
	plt.title(title)
	ax.xaxis.tick_top()
	#ax.xaxis.label_top()
	ax.xaxis.set_label_position("top")
	#plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
	plt.ylabel("Source")

	plt.xlabel("Destination")

	if save:
		plt.savefig(save, dpi=600)
	else:
		plt.show()



def dataFromFile(file):
	info = ""
	matrix = []
	instances = None
	for line in file:
		line = line.replace("\n","")
		if line == "":
			continue
		if line[0] == "#":
			info = line[1:]
			continue
		if line[0] == "\t":
			instances = line.split("\t")
			instances.pop(0)
			continue
		#print(line.strip("\t").split("\t"))
		matrix.append([float(data) for data in line.strip("\t").split("\t")])
	return (matrix, info, instances)

def getMasterMatrix(data):
	matrixes = [d[0] for d in data]
	final = [[matrixes[i-1][0][i] if i != 0 else 0 for i in range(len(matrixes) + 1)] if i == 0 else matrixes[i-1][i] for i in range(len(matrixes) + 1)]
	
	return (final, data[0][1], data[0][2])


def timeFromFile(file):
	for line in file:
		if line.split(" ")[0] == "Total":
			return float(line.split(" ")[-1])

def prettyprint(matrix, info, instances):
	s = "To\\From\t\t" + "\t".join(instances) + "\n"
	for i in range(len(matrix)):
		s += '{}\t{} \n'.format(instances[i], "\t\t".join(["{0:.1f}".format(num) for num in matrix[i]]))

	print(s)

def writeable(matrix, info, instances):
	s = "\n#{}\n".format(info)
	s += "To\\From\t" + "\t".join(instances) + "\n"
	for i in range(len(matrix)):
		s += '{}\t{} \n'.format(instances[i], "\t".join(["{0:.1f}".format(num) for num in matrix[i]]))
	s += "\n"
	return s


def main(filetype = None, testNumber = None):
	V = False
	if not filetype and not testNumber and len(sys.argv) != 3:
		print("USAGE: tableMerger.py [type] [TX Number]")
		exit()
	elif len(sys.argv) == 3:
		filetype = sys.argv[1]	
		testNumber = int(sys.argv[2])
		V = False
	
	GOSSIP_BYTES_PER_SECOND = 530
	GOSSIP_PACKETS_PER_SECOND = 3.9025
	
	GOSSIP_TABLE_OUT = "./Finished/TX{}_{}_GOS.txt".format(testNumber, filetype)
	GOSSIP_PLOT_OUT = "./Finished/TX{}_{}_GOS.png".format(testNumber, filetype) if not V else None
	
	NO_GOSSIP_TABLE_OUT = "./Finished/TX{}_{}_NO_GOS.txt".format(testNumber, filetype)
	NO_GOSSIP_PLOT_OUT = "./Finished/TX{}_{}_NO_GOS.png".format(testNumber, filetype)  if not V else None

	filename = f'{filetype}.txt'
	

	datafiles = [dataFromFile(open(f'Instance{i}/Transaction{testNumber}/{filename}', 'r')) for i in range(1, 6)]
	timeUsedList = [timeFromFile(open(f'Instance{i}/Transaction{testNumber}/information.txt', 'r')) for i in range(1, 6)]
	avgTime = sum(timeUsedList) / len(timeUsedList)
	totGossipb = GOSSIP_BYTES_PER_SECOND * avgTime
	totGossipp = GOSSIP_PACKETS_PER_SECOND * avgTime
	filetypes = {"DAVG" : ("Average Bytes Per Transaction", GOSSIP_BYTES_PER_SECOND), "DTOT": ("Total Bytes Per Transaction", totGossipb), "PAVG": ("Average Packets Per Transaction", GOSSIP_PACKETS_PER_SECOND), "PTOT": ("Total Packets Per Transaction", totGossipp)}
	
	masterData = getMasterMatrix(datafiles)
	
	if V:
		print(f"Gossip and {filetypes[filetype][0]}:")
	#prettyprint(*masterData)
	instances = ["Caliper", "Instance 1", "Instance 2", "Instance 3", "Instance 4", "Instance 5"]
	out_gossip = writeable(masterData[0], filetypes[filetype][0] + ", Including Gossip Traffic.", ["Caliper", "Instance 1", "Instance 2", "Instance 3", "Instance 4", "Instance 5"])
	heatmap(masterData[0], masterData[1], instances, "" + filetypes[filetype][0] + ", Including Gossip Traffic.", GOSSIP_PLOT_OUT)	


	if V:
		print(f"Gossipless and {filetypes[filetype][0]}:")
	
	masterData[0][2][3] -= filetypes[filetype][1]
	masterData[0][3][2] -= filetypes[filetype][1]
	masterData[0][5][4] -= filetypes[filetype][1]
	masterData[0][4][5] -= filetypes[filetype][1]
	#prettyprint(*masterData)
	out_no_gossip = writeable(masterData[0], filetypes[filetype][0] + ", Excluding Gossip Traffic.", ["Caliper", "Instance 1", "Instance 2", "Instance 3", "Instance 4", "Instance 5"])
	heatmap(masterData[0], masterData[1], instances, "" + filetypes[filetype][0] + ", Excluding Gossip Traffic.", NO_GOSSIP_PLOT_OUT)
	#heatmap(masterData[0], masterData[1], masterData[2], filetypes[filetype][0])

	# save as tables.
	
	#print(GOSSIP_TABLE_OUT)
	if not V:
		with open(GOSSIP_TABLE_OUT, 'w') as file:
			file.write(out_gossip)
		
		with open(NO_GOSSIP_TABLE_OUT, 'w') as file:
			file.write(out_no_gossip)
	#print(NO_GOSSIP_TABLE_OUT)
	#print(out_no_gossip)
	# save heatmap.
if __name__ == '__main__':
	runFor = ["DAVG", "DTOT", "PAVG", "PTOT"]
	testsTot = 5
	if len(sys.argv) == 2 and sys.argv[1] == "all":
		for testNumber in range(1, testsTot + 1):
			for filetype in runFor:
				print(f'TX: {testNumber}  Type: {filetype}')
				main(filetype = filetype, testNumber = testNumber)

	else:	
		main()