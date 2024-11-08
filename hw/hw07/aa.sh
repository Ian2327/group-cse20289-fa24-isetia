#!/bin/sh

#set -x

if [ "$#" -ne 2 ]; then
	echo "Usage: sh aa.sh <archive_file> <bad_urls_csv>"
	exit 1
fi

ARCHIVE_FILE=$1
BAD_URLS_CSV=$2

if [ ! -f $ARCHIVE_FILE ]; then
	echo "The file $ARCHIVE_FILE does not exist."
	exit 1
fi

if [ ! -f $BAD_URLS_CSV ]; then
	echo "The file $BAD_URLS_CSV does not exist."
	exit 1
fi

sh ae.sh $ARCHIVE_FILE > /dev/null 2>&1

if [ $? -ne 0 ]; then
	echo "There was an error extracting the archive."
	exit 1
fi

if [ ! -d archive ]; then
	echo "Failed to extract: directory 'archive' was not found."
	exit 1
fi

findr () {
	DIR=$1
	for FILE in `ls $DIR`; do
		if [ -d "$FILE" ]; then
			findr "$FILE"
		fi
		sh sbs.sh "$BAD_URLS_CSV" "$FILE" > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			SBS_RESULTS=$(sh sbs.sh "$BAD_URLS_CSV" "$FILE" | tail -n 1)
			if [ "$SBS_RESULTS" != "CLEAN" ]; then
				echo "$SBS_RESULTS"
				rm -rf archive
				exit 0
			fi
		fi
		sh sf.sh "$FILE" > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			SF_RESULTS=$(sh sf.sh "$FILE" | tail -n 1)
			if [ "$SF_RESULTS" != "CLEAN" ]; then
				echo "$SF_RESULTS"
				rm -rf archive
				exit 0
			fi
		fi

	done
}

findr "archive/*"

if [ -d archive ]; then
	rm -rf archive
fi
echo "CLEAN"

