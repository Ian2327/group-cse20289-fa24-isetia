#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "Usage: sh sf.sh <file_to_check>"
	exit 1
fi

FILE=$1

if [ ! -f $FILE ]; then
	echo "The file $FILE does not exist."
	exit 1
fi

if file "$FILE" | grep -q "binary"; then
	echo "The file $FILE is a binary file"
	exit 1
fi

echo "Scanning for sensitive information"
echo "File to scan: $FILE"

if grep -q "\*SENSITIVE\*" "$FILE"; then
	echo "SENSITIVE, MARKED SENSITIVE"
	exit 0
fi

if grep -Eq '[0-9]{3}-[0-9]{2}-[0-9]{4}' "$FILE"; then
	echo "SENSITIVE, SSN"
	exit 0
fi

if grep -Eq '90[0-9]{7}' "$FILE"; then
	echo "SENSITIVE, STUDENTID"
	exit 0
fi

echo "CLEAN"
