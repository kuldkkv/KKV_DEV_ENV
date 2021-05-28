LIB=./lib
TMP=./tmp
DIST=./dist
SRC=./src
RM=/bin/rm -f


all:	$(DIST)/main $(TMP)/main.o

$(DIST)/main:	$(TMP)/main.o
	cc $(TMP)/main.o -o $(DIST)/main

$(TMP)/main.o:	$(SRC)/main.c
	cc -c $(SRC)/main.c -o  $(TMP)/main.o

clean:
	$(RM) $(TMP)/main.o

cleanall:
	$(RM) $(TMP)/main.o $(DIST)/main
