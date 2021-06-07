CFLAGS = -Wall -g -std=gnu99
# CFLAGS = -Wall -Wextra -g -ansi -pedantic -Werror -std=gnu99

CC = gcc

FILES = encrypt decrypt

all: $(FILES) clear

# seg-perf:
# 	$(CC) $(CFLAGS) -o seg-perf seg-perf.c -lgmp -L.

decrypt: rijndael.o
	$(CC) $(CFLAGS) -o decrypt decrypt.c rijndael.o

encrypt: rijndael.o
	$(CC) $(CFLAGS) -o encrypt encrypt.c rijndael.o

# Librería rijndael
rijndael.o: rijndael.c rijndael.h
	$(CC) $(CFLAGS) -c rijndael.c


clear:
	rm -rf *.o *.gch

clean:
	rm -rf *.o *.gch $(FILES)