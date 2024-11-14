#!/bin/sh

toscan_dir="/escnfs/home/isetia/repos/scandata/toscan"
test_dir="test"

for archive in "$test_dir"/*; do
	cp "$archive" "$toscan_dir"
	sleep 2
done
