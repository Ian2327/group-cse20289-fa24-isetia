#!/bin/sh
set -x

DEPTH=0

if [ "$#" -lt 2 ]; then
	echo "Usage: sh ec.sh [-ad <depth>] <archive_file> <bad_urls_csv>"
	exit 1
fi

ARG1=$1
ARG2=$2
ARCHIVE_FILE=$1
BAD_URLS_CSV=$2

if [[ $ARG1 == "-ad" ]]; then
	if ! [[ "$ARG2" =~ ^[0-3]$ ]]; then
		echo "Usage: sh ec.sh [-ad <depth>] <archive_file> <bad-Urls_csv>"
		echo "<depth> must be between 0 and 3."
		exit 1
	fi
	if [ "$#" -lt 4 ]; then
		echo "Usage: sh ec.sh [-ad <depth>] <archive_file> <bad_urls_csv>"
		exit 1
	fi
	DEPTH=$ARG2
	ARCHIVE_FILE=$3
	BAD_URLS_CSV=$4	
fi
	
if [ ! -f $ARCHIVE_FILE ]; then
	echo "The file $ARCHIVE_FILE does not exist."
	exit 1
fi


if [ ! -f $BAD_URLS_CSV ]; then
	echo "The file $BAD_URLS_CSV does not exist."
	exit 1
fi

extract_first () {
	CURR_ARCHIVE_FILE=$1
	sh ae.sh "$CURR_ARCHIVE_FILE" > /dev/null 2>&1
	iterate "archive"
}

iterate () {
	DIR=$1
	for FILE in $DIR/*; do
		parse $FILE
	done
}

parse () {
	CURR_FILE=$1
	if [ -d $CURR_FILE ]; then
		iterate $CURR_FILE
	elif [[ "$CURR_FILE" == *.zip ]] || [[ "$CURR_FILE" == *.tar ]] || [[ "$CURR_FILE" == *.tar.gz ]]; then
		extract $CURR_FILE
	else
		STAT=$(sh sbs.sh "$BAD_URLS_CSV" "$CURR_FILE" | tail -n 1)
		if [[ "$STAT" != "CLEAN" ]]; then
			echo "$STAT"
			exit 1
		fi
		STAT=$(sh sf.sh "$CURR_FILE" | tail -n 1)
		if [[ "$STAT" != "CLEAN" ]]; then
			echo "$STAT"
			exit 1
		fi
	fi	
}

extract () {
	CURR_ARCHIVE_FILE=$1
	sh ae.sh "$CURR_ARCHIVE_FILE" > /dev/null 2>&1
	iterate "$(dirname $CURR_ARCHIVE_FILE)/$(basename $CURR_ARCHIVE_FILE | cut -d '.' -f 1)"

}

extract_first "$ARCHIVE_FILE"
echo "CLEAN"
exit 0
