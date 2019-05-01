
for i in 1 2 3 4 5
do
	editcap -A "2019-03-21 12:19:39" -B "2019-03-21 12:20:13" Instance${i}/${i}_transaction_flow.pcap Instance${i}/${i}_1.pcap
	editcap -A "2019-03-21 12:20:14" -B "2019-03-21 12:20:46" Instance${i}/${i}_transaction_flow.pcap Instance${i}/${i}_2.pcap
	editcap -A "2019-03-21 12:20:47" -B "2019-03-21 12:21:20" Instance${i}/${i}_transaction_flow.pcap Instance${i}/${i}_3.pcap
	editcap -A "2019-03-21 12:21:21" -B "2019-03-21 12:23:31" Instance${i}/${i}_transaction_flow.pcap Instance${i}/${i}_4.pcap
	editcap -A "2019-03-21 12:23:32" -B "2019-03-21 12:25:15" Instance${i}/${i}_transaction_flow.pcap Instance${i}/${i}_5.pcap
done

echo "Done"
