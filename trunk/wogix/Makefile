CC=gcc
CCFLAGS=-Wall -W
CPP=g++
CPPFLAGS=-Wall -W
LD=ld
AS=nasm

OBJECTS=src/main.o
BIN=src/wogix

all: $(OBJECTS) link

install:
	-echo "error: 'make install' not defined."

clean:
	-rm $(OBJECTS) $(BIN)

%.o: %.cpp Makefile
	$(CPP) $(CPPFLAGS) $< -o $@ -lX11

link:
	$(LD) -o $(BIN) $(OBJECTS)
