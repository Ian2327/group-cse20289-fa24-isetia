#!/bin/sh

toscan_dir="/escnfs/home/isetia/repos/scandata/toscan"
test_dir="./test"

if [ ! -d "$test_dir" ]; then
	echo "Direcotry $test_dir does not exist."
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
