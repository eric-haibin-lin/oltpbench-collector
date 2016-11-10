#!/bin/bash
for d in `ls | grep tpcc_collected | sort -t '_' -k10,10 -g`; do
		b=`echo $d | cut -d'_' -f 10`
	    echo -n -e "$b\t"
done
echo ""
for d in `ls | grep tpcc_collected | sort -t '_' -k10,10 -g`; do
		#b=`echo $d | cut -d'-' -f 9`
		thrpt=`head -6 ${d}/*.summary | tail -1`
		echo -n -e "$thrpt\t"
done
echo ""
