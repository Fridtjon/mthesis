
for i in 1 2 3 4 5
do
	echo "Working on Instance ${i}"
	for j in 1 2 3 4 5
	do
		mkdir Instance${i}/Transaction${j}
		python3 TX_Flow_manager.py Instance${i}/${i}_${j}.pcap
		mv PAVG.txt Instance${i}/Transaction${j}/
		mv PTOT.txt Instance${i}/Transaction${j}/
		mv DAVG.txt Instance${i}/Transaction${j}/
		mv DTOT.txt Instance${i}/Transaction${j}/
		mv information.txt Instance${i}/Transaction${j}/
	done
done
echo "Enjoy!"