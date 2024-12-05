#!/bin/sh
# Ian Setia
# isetia@nd.edu

CONFIG_FILE=".config"

if [[ ! -f $CONFIG_FILE ]]; then
	echo "Error: Config file $CONFIG_FILE cannot be found."
	exit 1
fi

EXE=$(grep '^EXE' $CONFIG_FILE | cut -d '=' -f 2)
HOST=$(grep '^HOST' $CONFIG_FILE | cut -d '=' -f 2)
PORT=$(grep '^PORT' $CONFIG_FILE | cut -d '=' -f 2)

if [[ ! -x $EXE ]]; then
	echo "Error: Executable file name is missing in $CONFIG_FILE or is not executable"
	exit 1
fi

if [[ -z $HOST ]]; then
	echo "Error: Hostname is missing in $CONFIG_FILE"
	exit 1
fi 

if [[ -z $PORT ]]; then 
	echo "Error: Port is missing in $CONFIG_FILE"
	exit 1
fi

if [[ $# -lt 1 ]]; then
	echo "Usage: $0 [-query <filter_string>] <year> <month> <day> <hour>"
	exit 1
fi

ARG1=$1
if [[ $ARG1 == "-query" ]]; then
	if [ $# -ne 6 ]; then
		echo $#
		echo "Usage: $0 -query <filter_string> <year> <month> <day> <hour>"
		exit 1
	fi
	FILTER_STRING=$2
	YEAR=$3
	MONTH=$4
	DAY=$5
	HOUR=$6
	./$EXE "$HOST" "$PORT" "$YEAR" "$MONTH" "$DAY" "$HOUR" "$FILTER_STRING"
else
	if [ $# -ne 4 ]; then
		echo $#
		echo "Usage: $0 <year> <month> <day> <hour>"
		exit 1
	fi
	YEAR=$1
	MONTH=$2
	DAY=$3
	HOUR=$4
	./$EXE "$HOST" "$PORT" "$YEAR" "$MONTH" "$DAY" "$HOUR"
fi
