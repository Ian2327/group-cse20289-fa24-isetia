#!/bin/sh

usage () {
	echo "Usage: sh scanner.sh <toscan_dir> <approved_content_dir> <quarantined_content_dir> <log_dir> <malicious_urls_file>"
}

extract () {
	archive=$1
	if [ -z $archive ]; then
		#echo "Blank file inputted to extraction function."
		return 2
	fi
	if [ ! -d "./extracted" ]; then
		#echo "Directory 'extracted' does not yet exist. Creating ..."
		mkdir extracted
	#else 
		#echo "Directory 'extracted' already exists"
	fi 

	base_name=$(basename "$archive" | sed 's/\.[^.]*$//')
	extract_dir="./extracted/$base_name"
	mkdir "$extract_dir"
	case $archive in 
		*.zip)
			echo "Unzipping .zip file"
			unzip -o "$archive" -d "$extract_dir"
			;;
		*.tar.gz | *.tgz)
			echo "Extracting .tar.gz file"
			tar -xzf "$archive" -C "$extract_dir" --overwrite
			;;
		*.tar)
			echo "Extracting .tar file"
			tar -xf "$archive" -C "$extract_dir" --overwrite
			;;
		*)
			echo "Unsupported file type. Removing $archive ..."
			rm "$archive"
			return 1
			;;
	esac

	echo "Checking for nested archives within extracted directory..."
	find "$extract_dir" -type f \( -name "*.zip" -o -name "*.tar.gz" -o -name "*.tgz" -o -name "*.tar" \) | while read nested_archive; do
		echo "Found nested archive: $nested_archive"
		extract "$nested_archive"
		rm "$nested_archive"
	done


	return 0
}

if [ $# -ne 5 ]; then
	usage
	exit 2
fi

toscan_dir=$1
approved_dir=$2
quarantined_dir=$3
log_dir=$4
malicious_urls_file=$5

for dir in "$toscan_dir" "$approved_dir" "$quarantined_dir" "$log_dir"; do 
	if [ ! -d "$dir" ]; then
		echo "$dir is not a valid directory or does not exist"
		usage
		exit 1
	fi
done

if [ ! -f "$malicious_urls_file" ]; then
	echo "$malicious_urls_file is not a valid file or does not exist"
	usage
	exit 1
fi

log_event () {
	local message="$1"
	local log_file="$log_dir/$(date +'%Y-%m-%d').log"
	echo "$(date +'%Y-%m-%d %H:%M:%S') $message" >> $log_file
}

quarantine () {
	local archive="$1"
	local reason="$2"
	local trigger="$3"
	local archive_name=$(basename "$archive")

	mv -f "$archive" "$quarantined_dir"
	echo -e "Filename: $archive_name\nReason: $reason\nTrigger: $trigger" > "$quarantined_dir/$archive_name.reason"
	log_event "$archive_name QUARANTINE $reason $trigger"
}

approve () {
	local archive="$1"
	mv -f "$archive" "$approved_dir"
	log_event "$(basename "$archive") APPROVE"
}

scan_files () {
	local dir="$1"
	local malicious_urls_file="$2"
	BAD_SITES_DATA=$(grep -v '^#' "$malicious_urls_file" | cut -d ',' -f 3)
	PATTERN=$(echo "$BAD_SITES_DATA" | tr '\n' '|')
	PATTERN=${PATTERN%|}
	found=0

	for file in $(find "$dir" -type f); do
		echo "DIR = $dir; FILE = $file"
		if grep -Eq "$PATTERN" "$file"; then
			quarantine "$file" "MALICIOUSURL" "$(grep -Eo "$PATTERN" "$file")"
			found=1
		elif grep -Eq '[0-9]{3}-[0-9]{2}-[0-9]{4}' "$file"; then 
			quarantine "$file" "SENSITIVE" "SSN found"
			found=1
		elif grep -Eq '90[0-9]{7}' "$file"; then
			quarantine "$file" "SENSITIVE" "NDID found"
			found=1
		elif grep -q '\*SENSITIVE\*' "$file"; then
			quarantine "$file" "SENSITIVE" "Marked SENSITIVE"
			found=1
		else
			approve "$file" 
		fi
	done
	if [ "$found" -eq 0 ]; then
		return 0
	else
		return 1
	fi
	
}

clean_up () {
	log_event 'Scanner stopped'
	rm -r extracted
	exit 0
}

trap 'clean_up' SIGINT

log_event "Scanner started"

while true; do
	for archive in "$toscan_dir"/*; do
		if [[ -f "$archive" ]]; then
			if extract "$archive"; then
				base_name=$(basename "$archive" | sed 's/\.[^.]*$//')
				extract_dir="./extracted/$base_name"
				echo "EXTRACTED DIR = $extract_dir"
				scan_files "$extract_dir" "$malicious_urls_file"
				rm "$archive"
		
			else 
				quarantine "$archive" "CANNOTEXTRACT" "Extraction failed"
			fi
			
		fi



	done
	sleep 1
done


