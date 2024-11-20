Ian Setia, Andrew Linares
isetia@nd.edu, alinare2@nd.edu

- Initially created Makefile and ensured that all works
- Renamed initial README.md to Assignment9.md
- Uncommented and added print statements to see different variables and error messages
- Ran redextract-debug using gdb to locate where code stops running
- Found the error in 2500 in pcap-read.h
- Ran redextract-debug using valgrind with --leak-check=full --show-leak-kinds=all -s to show all memory related errors and locations
- Freed theInfo.FileName to resolve one valgrind error
- Set BigTable contents to NULL and freed BigTable to resolve valgrind error
