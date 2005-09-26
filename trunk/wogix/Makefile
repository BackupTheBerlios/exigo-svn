CC=gcc
CCFLAGS=-Wall -W
CPP=g++
CPPFLAGS=-Wall -W
LD=ld
AS=nasm

OBJECTS=src/main.o
WOGIX=wogix

all: $(WOGIX)

install:
	-echo "error: 'make install' not defined."

clean:
	-rm $(OBJECTS)

$(WOGIX): $(OBJECTS) Makefile
	$(LD) $(OBJECTS) -o $@

%.o: %.cpp Makefile
	$(CPP) $(CPPFLAGS) $< -o $@ -lX11

