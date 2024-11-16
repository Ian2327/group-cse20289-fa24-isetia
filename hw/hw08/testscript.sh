#!/bin/sh

#Ian Setia
#isetia@nd.edu

if [ $# -ne 2 ];then
	echo "Usage: sh testscript.sh <dir_to_scan> <test_archives_dir>"
fi
toscan_dir=$1
test_dir=$2


if [ ! -d "$toscan_dir" ]; then
	echo "Directory $toscan_dir does not exist."
	exit 1
fi
if [ ! -d "$test_dir" ]; then
	echo "Directory $test_dir does not exist."
	exit 1
fi

for archive in $test_dir/*; do
	if [ -e "$archive" ]; then
		cp "$archive" "$toscan_dir"
		sleep 2
	else 
		echo "No files found in $test_dir"
		break
	fi
done

exit 0
