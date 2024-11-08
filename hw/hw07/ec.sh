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

extract_archive () {
	local CURR_DEPTH=$1
	local CURR_ARCHIVE_FILE=$2
	sh ae.sh "$CURR_ARCHIVE_FILE" > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "There was an error extracting the archive: $CURR_ARCHIVE_FILE"
		rm -rf archive
		exit 1
	fi
	DIR="archive"
	scan_dir "$DIR" "$CURR_DEPTH"
}

scan_dir () {
	for FILE in "$1"/*; do
		parse_file "$FILE" "$2"
	done
}

parse_file () {
	FILE=$1
	CURR_DEPTH=$2
	if [ -d "$FILE" ]; then
		scan_dir "$FILE" "$CURR_DEPTH"
		return 0
	fi
	if [ "$CURR_DEPTH" -lt "$DEPTH" ]; then
		case "$FILE" in
			*.zip|*.tar|*.tar.gz)
				next=$((CURR_DEPTH+1))
				echo "$FILE"
				extract_archive "$next" "$FILE"
				;;
		esac
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

}

extract_archive 0 "$ARCHIVE_FILE"

echo "CLEAN"
exit 0
