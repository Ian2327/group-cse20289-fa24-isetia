Ian Setia, Andrew Linares
isetia@nd.edu, alinare2@nd.edu

How to run server/client with user input:
- $ gcc -o client client.c -lzmq
- $ ./client
- $ python3 theServer.py path/to/data.json port_number
	- We used port 41005 for our testing
- Run the command (list, more, various stats) with the terminal you ran ./client from

When running either the shell script or the client executable with wildcard * for the year, month, day, or hour, type as '*' to prevent it from doing a wildcard on the files in the directory

When running client through bb.sh, it allows the user to input the date, time, and string filters upon execuing ./bb.sh and simply call 'list', 'more', 'count', ..., 'exit' without having to reenter the filters initially set upon calling the execution of bb.sh

Rather than writing a separate bbf script, the client.c script has been altered to have nicely formatted outputs

Example usage of bb.sh: ./bb.sh -query 'iface=eth0;dir=downlink;type=iperf' '*' '*' '*' '*'


Test.sh:
- Tests the client with various commands, both valid and invalid
- Tests the client executable with both valid and invalid arguments
