Ian Setia, Andrew Linares
isetia@nd.edu, alinare2@nd.edu

- Initially created Makefile and ensured that all works (Ian)
- Renamed initial README.md to Assignment9.md
- Uncommented and added print statements to see different variables and error messages
- Ran redextract-debug using gdb to locate where code stops running
- Found the error in 2500 in pcap-read.h (Ian)
	- The value 2500 for defult read buffer variable was larger than the set maximum value (1500)
- Ran redextract-debug using valgrind with --leak-check=full --show-leak-kinds=all -s to show all memory related errors and locations
- Found malloc'ed and unfreed variable, theInfo.FileName, and updated main.c to free theInfo.FileName to resolve one valgrind error (Ian)
- Set BigTable contents to NULL and freed BigTable to resolve valgrind error (Ian)
