LIB=./lib
TMP=./tmp
DIST=./dist
SRC=./src
RM=/bin/rm -f


all:	$(DIST)/server $(DIST)/client

$(DIST)/server:	$(TMP)/server.o
	cc $(TMP)/server.o -o $(DIST)/server

$(TMP)/server.o:	$(SRC)/server.c
	cc -c $(SRC)/server.c -o  $(TMP)/server.o

$(DIST)/client:	$(TMP)/client.o
	cc $(TMP)/client.o -o $(DIST)/client

$(TMP)/client.o:	$(SRC)/client.c
	cc -c $(SRC)/client.c -o  $(TMP)/client.o

clean:
	$(RM) $(TMP)/server.o $(TMP)/client.o

cleanall:
	$(RM) $(TMP)/server.o $(TMP)/client.o $(DIST)/server $(DIST)/client
