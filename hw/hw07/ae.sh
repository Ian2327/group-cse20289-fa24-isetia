#!/bin/sh
#set -x

if [ "$#" -eq 0 ]; then
	echo "Usage: sh ae.sh <.zip .tar .tar.gz file>"
	exit 1
fi

FILE=$1
FILE_DIR=$(dirname "$FILE")
ARCHIVE_DIR="$FILE_DIR/archive"


if [ ! -d "$ARCHIVE_DIR" ]; then
	echo "archive directory is not present .. creating!"
	mkdir $ARCHIVE_DIR
else
	echo "archive directory already present - no need to create"
fi

if [[ "$FILE" == *.zip ]]; then
	echo "Extracting a zip file via unzip"
	unzip -q $FILE -d $ARCHIVE_DIR > /dev/null 2>&1

elif [[ "$FILE" == *.tar.gz ]] || [[ "$FILE" == *.tgz ]]; then
	echo "Extracting a tar file"
	tar -xzf $FILE -C "$ARCHIVE_DIR" > /dev/null 2>&1

elif [[ "$FILE" == *.tar ]]; then
	tar -xf $FILE -C "$ARCHIVE_DIR" > /dev/null 2>&1

else 
	echo "Unvalid file type. This script only supports .zip, .tar or .tar.gz files."
	exit 1
fi

exit 0



