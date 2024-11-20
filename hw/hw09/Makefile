CC=gcc
CFLAGS=-c -Wall -std=c99
DEBUGFLAGS=-g -O0
LIBS=-lpthread -lm

EXEC=redextract
DEBUG_EXEC=redextract-debug
SOURCE=$(wildcard *.c)
OBJS=$(SOURCE:.c=.o)

all: $(EXEC)

# $@: Target
# $^: Dependencies
# $<: First Dependency

$(EXEC): $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

$(DEBUG_EXEC): CFLAGS += $(DEBUGFLAGS)
$(DEBUG_EXEC): $(OBJS)
	$(CC) -o $@ $^ $(LIBS)

%.o: %.c %.h
	$(CC) $(CFLAGS) -o $@ $<

main.o: main.c
	$(CC) $(CFLAGS) -o $@ $<

clean: 
	rm $(EXEC) $(DEBUG_EXEC) $(OBJS)

# Given previous code
#redextract: packet.c packet.h pcap-read.c pcap-read.h pcap-process.c pcap-process.h main.c
#	gcc packet.c pcap-process.c pcap-read.c main.c -Wall --std=c99 -lpthread -lm -o redextract
