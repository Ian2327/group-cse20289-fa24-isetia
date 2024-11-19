CC=gcc
EXEC=redextract
CFLAGS=-c -Wall -std=c99
GFLAGS=-g
LIBS=-lpthread -lm
OBJS=main.o packet.o pcap-process.o pcap-read.o

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(GFLAGS) -o $(EXEC) $(OBJS) $(LIBS)

main.o: main.c
	$(CC) $(CFLAGS) $(GFLAGS) -o main.o main.c

packet.o: packet.c packet.h
	$(CC) $(CFLAGS) $(GFLAGS) -o packet.o packet.c

pcap-read.o: pcap-read.c pcap-read.h
	$(CC) $(CFLAGS) $(GFLAGS) -o pcap-read.o pcap-read.c

pcap-process.o: pcap-process.c pcap-process.h
	$(CC) $(CFLAGS) $(GFLAGS) -o pcap-process.o pcap-process.c

clean: 
	rm $(EXEC)
	rm $(OBJS)

# Given previous code
#redextract: packet.c packet.h pcap-read.c pcap-read.h pcap-process.c pcap-process.h main.c
#	gcc packet.c pcap-process.c pcap-read.c main.c -Wall --std=c99 -lpthread -lm -o redextract
