#!/bin/bash
testname=small_init
echo "running test with ${testname}"
for i in 1 5 20 50 100
do
	echo "Running tests for $i clients"
	#echo benchmark/hashcode_t4/main.js -c configs/${testname}/${i}client_config.yaml
	node benchmark/hashcode_t4/main.js -c configs/${testname}/${i}client_config.yaml
	echo "Moving report."
	mv report-from-tests.html tests/outputSuccessRate/${testname}_${i}.html
	sleep 5
done

echo "Finished running tests. HAVE FUN! :D"