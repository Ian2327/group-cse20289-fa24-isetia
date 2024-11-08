#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Usage: sh sbs.sh <malicious_urls_csv_file> <file_to_check>"
	exit 1
fi

CSV=$1
FILE=$2

if [ ! -f $CSV ]; then
	echo "The file $CSV does not exist."
	exit 1
fi

if [ ! -f $FILE ]; then
	echo "The file $FILE does not exist."
	exit 1
fi

if file "$FILE" | grep -q "binary"; then
	echo "The file $FILE is a binary file."
	exit 1
fi

BAD_SITES_DATA=$(grep -v '^#' "$CSV" | cut -d ',' -f 3)

echo "Loaded site information .. success!"
echo "Scanning file named $FILE"

for BAD_URL in $BAD_SITES_DATA; do 
	if grep -q "$BAD_URL" "$FILE"; then
		echo "Malicious URL detected!"
		echo "MALICIOUSURL: $BAD_URL"
		exit 0
	fi
done

echo "CLEAN"

