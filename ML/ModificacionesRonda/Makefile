CFLAGS = -Wall -g -std=gnu99
# CFLAGS = -Wall -Wextra -g -ansi -pedantic -Werror -std=gnu99

CC = gcc

FILES = generar_dataset

all: $(FILES) clear

generar_dataset: rijndael.o
	$(CC) $(CFLAGS) -o generar_dataset generar_dataset.c rijndael.o

# Librería rijndael
rijndael.o: rijndael.c rijndael.h
	$(CC) $(CFLAGS) -c rijndael.c


clear:
	rm -rf *.o *.gch

clean:
	rm -rf *.o *.gch $(FILES)