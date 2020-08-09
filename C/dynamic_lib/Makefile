LIB=./lib
TMP=./tmp
DIST=./dist
SRC=./src
RM=/bin/rm -f

all:	$(DIST)/main $(LIB)/lib_mylib.so
lib:    $(LIB)/lib_mylib.so

$(LIB)/lib_mylib.so:	$(TMP)/lib_mylib.o
	cc -shared -o $(LIB)/lib_mylib.so $(TMP)/lib_mylib.o

$(TMP)/lib_mylib.o:	$(SRC)/lib_mylib.c
	cc -c -Wall -Werror -fpic $(SRC)/lib_mylib.c -o $(TMP)/lib_mylib.o

$(DIST)/main:	$(SRC)/main.c	$(LIB)/lib_mylib.so
	cc -Wall $(SRC)/main.c -L$(LIB) -l_mylib -o $(DIST)/main

clean:
	$(RM) $(TMP)/lib_mylib.o $(LIB)/lib_mylib.so $(DIST)/main
