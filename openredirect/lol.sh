#!/bin/sh
counter=0 
while read -r line;
	counter=$((counter+1))
    if [ "$counter" -gt "30" ];
    then
        exit 0
    fi
	echo "========== $counter ==========="
	do python redirect.py target.list $line;done < payloads.list
