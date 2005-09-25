CC=gcc
CCFLAGS=-Wall -W
CPP=g++
CPPFLAGS=-Wall -W
LD=ld
AS=nasm

OBJECTS=src/main.o

all: $(OBJECTS)

install:
	-echo "error: 'make install' not defined."

clean:
	-rm $(OBJECTS)

$(KERNEL): $(OBJECTS) Makefile linker.ld
	$(LD) $(LDFLAGS) $(OBJECTS) -o $@ -T linker.ld

%.o: %.cpp Makefile
	$(CPP) $(CPPFLAGS) -c $< -o $@
