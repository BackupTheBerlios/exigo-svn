CC=gcc
CCFLAGS=-Wall -W
CPP=g++
CPPFLAGS=-Wall -W
AS=nasm

OBJECTS=src/main.o
WOGIX=wogix

all: $(WOGIX)

install:
	-echo "error: 'make install' not defined."

clean:
	-rm $(OBJECTS)
	-rm $(WOGIX)

$(WOGIX): $(OBJECTS) Makefile
	$(CPP) $(OBJECTS) -o $@ -lX11

%.o: %.cpp Makefile
	$(CPP) $(CPPFLAGS) $< -o $@ -c

