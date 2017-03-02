#!/bin/sh
if [ $# -lt 2 ]; then
	echo "Please enter the last line number and filename"
	exit
fi


a=1
while [ $a -lt $1 ];
do
	sed -n "$a,$a"p $2 > $a.txt
	a=$((a+1))
done
