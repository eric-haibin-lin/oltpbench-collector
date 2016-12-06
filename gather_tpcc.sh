#!/bin/bash

for ratio in "44_44_4_4_4" "100_0_0_0_0" "0_0_100_0" "60_0_40_0" "10_0_90_0"; do
	echo $ratio
	for d in `ls | grep tpcc_collected | grep $ratio | sort -t '_' -k9,9 -g`; do
		b=`echo $d | cut -d'_' -f 9`
	    echo -n -e "$b "
	done
	echo ""
	for d in `ls | grep tpcc_collected | grep $ratio | sort -t '_' -k9,9 -g`; do
		#b=`echo $d | cut -d'-' -f 9`
		thrpt=`head -6 ${d}/*.summary | tail -1`
		echo -n -e "$thrpt "
	done
	echo ""
done
