import sys


def generateHeader(data):
	s = "\t"

	if(len(data) == 4):
		data.insert(0, "")

	for d in range(len(data) - 1):
		s += "{} & ".format(data[d])
	s += "{} \\\\ [0.5ex] \n\\hline\n".format(data[-1])
	return s

def generateData(data):
	s = "\t"
	for d in range(len(data) - 1):
		s += "{} & ".format(data[d])
	s += "{} \\\\ [0.5ex] \n".format(data[-1])
	return s

print(len(sys.argv))

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("Usage: tablify.py [file] <caption>")
	exit(0)

caption = ""
if len(sys.argv) == 3:
	caption += "\\caption{" + sys.argv[2] + "}\n"
tables = []
with open(sys.argv[1]) as file:
	newTable = True
	print("\n")
	for line in file:
		if line == "\n":
			if not newTable:
				tables[-1] += "\\hline\n\\end{tabular}\n\\end{table}\n"
			newTable = True
			continue
		if line[0] == "#":
			caption = "\\caption{" + line[1:] + "}\n"
			continue

		line = line.replace("%", "\%")
		data = line.split("\t")
		if newTable:
			newTable = False
			tables.append("\\begin{table}\\center\n" + caption + "\t\\begin{tabular}{|c | c c c c|}\n\\hline\n")
			tables[-1] += generateHeader(data)
		else:
			tables[-1] += generateData(data)

	print(" ")
for table in tables:
	print(table)
