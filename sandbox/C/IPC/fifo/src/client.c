#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include "fifo.h"

void client(int, int);

int main(int argc, char **argv)
{
	int readfd, writefd;

	if ((mkfifo(FIFO1, FILE_MODE) < 0) && (errno != EEXIST)) {
		perror("fifo1");
		exit(EXIT_FAILURE);
	}

	if ((mkfifo(FIFO2, FILE_MODE) < 0) && (errno != EEXIST)) {
		perror("fifo2");
		exit(EXIT_FAILURE);
	}

	writefd = open(FIFO1, O_WRONLY, 0);
	readfd = open(FIFO2, O_RDONLY, 0);

	client(readfd, writefd);

	exit(EXIT_SUCCESS);
}

void client(int readfd, int writefd)
{
	size_t len;
	ssize_t n;
	char buf[BUFSIZ];

	printf("client: enter pathname\n");
	fgets(buf, BUFSIZ, stdin);	// get pathname from stdin
	len = strlen(buf);
	if (buf[len] == '\n') {
		len--;
		printf("removed newline from buffer in client\n");
	}

	write(writefd, buf, len);	// pass pathname to server

	while ((n = read(readfd, buf, BUFSIZ)) > 0)	// read pathname/file contents from server
		write(STDOUT_FILENO, buf, n);
}
