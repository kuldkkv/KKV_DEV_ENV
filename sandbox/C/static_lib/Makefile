LIB=./lib
TMP=./tmp
DIST=./dist
SRC=./src
RM=/bin/rm -f


all:	$(DIST)/main $(LIB)/lib_mylib.a

$(LIB)/lib_mylib.a:	$(TMP)/lib_mylib.o
	ar rcs $(LIB)/lib_mylib.a $(TMP)/lib_mylib.o

$(TMP)/lib_mylib.o:	$(SRC)/lib_mylib.c
	cc -c $(SRC)/lib_mylib.c -o $(TMP)/lib_mylib.o

$(DIST)/main:	$(SRC)/main.c $(LIB)/lib_mylib.a
	cc $(SRC)/main.c -L$(LIB) -l_mylib -o $(DIST)/main

clean:
	$(RM) $(TMP)/lib_mylib.o $(LIB)/lib_mylib.a $(DIST)/main
