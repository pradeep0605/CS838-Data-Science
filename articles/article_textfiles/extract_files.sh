#!/bin/sh

a=1
while [ $a -lt 463 ];
do
	sed -n "$a,$a"p article.json > $a.txt
	a=$((a+1))
done
