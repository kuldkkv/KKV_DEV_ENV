LIB=./lib
TMP=./tmp
DIST=./dist
SRC=./src
RM=/bin/rm -f


all:	$(DIST)/server $(DIST)/client $(LIB)/lib_myserverlib.a

$(LIB)/lib_myserverlib.a:	$(TMP)/lib_myserverlib.o
	ar rcs $(LIB)/lib_myserverlib.a $(TMP)/lib_myserverlib.o

$(TMP)/lib_myserverlib.o:	$(SRC)/lib_myserverlib.c
	cc -c $(SRC)/lib_myserverlib.c -o $(TMP)/lib_myserverlib.o

$(DIST)/server:	$(SRC)/server_main.c $(LIB)/lib_myserverlib.a
	cc $(SRC)/server_main.c -L$(LIB) -l_myserverlib -o $(DIST)/server

$(DIST)/client:	$(SRC)/client.c
	cc $(SRC)/client.c -L$(LIB) -o $(DIST)/client

clean:
	$(RM) $(TMP)/lib_myserverlib.o $(LIB)/lib_myserverlib.a $(DIST)/server $(DIST)/client
