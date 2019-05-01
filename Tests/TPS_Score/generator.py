import sys

print(len(sys.argv))

if len(sys.argv) != 2:
	print("Usage: generator.py [file]")
	exit(0)


data = []
with open(sys.argv[1]) as file:
	for line in file:
		line = line.replace(",",".")
		numbers = [float(i) for i in line.strip().split("\t")]
		print(numbers)
		for i in range(len(numbers)):
			if i == 0:
				numbers[i] = 100 / 10 * numbers[i] / 100
			elif i == 1:
				numbers[i] = 100 / 100 * numbers[i] / 100
			elif i == 2:
				numbers[i] = 100 / 1000 * numbers[i] / 100
			elif i == 3:
				numbers[i] = 100 / 10000 * numbers[i] / 100


		data.append(numbers)


for line in data:
	first = True
	for number in line:
		number = round(number, 2)
		if first:
			first = False
			print(number, end="")
		else:
			print(f"\t{number}",end="")

	print()
print()

[print(sum(line)/len(line), end="\t") for line in data]
print()
