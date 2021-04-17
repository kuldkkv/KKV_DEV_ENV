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

void server(int, int);

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

	readfd = open(FIFO1, O_RDONLY, 0);
	writefd = open(FIFO2, O_WRONLY, 0);

	server(readfd, writefd);

	exit(EXIT_SUCCESS);
}

void server(int readfd, int writefd)
{
	int fd;
	ssize_t n;
	char buf[BUFSIZ];

	// read pathname from readfd
	if ((n = read(readfd, buf, BUFSIZ)) <= 0) {
		fprintf(stderr, "server: read error for pathname\n");
		exit(EXIT_FAILURE);
	}
	buf[n - 1] = '\0';
	printf("server: filename received is [%s] [%d] [%d]\n", buf,
	       strlen(buf), n);

	// read file pointed by pathname/buf
	if ((fd = open(buf, O_RDONLY)) < 0) {
		sprintf(buf, "server: unable to open file: %s\n",
			strerror(errno));
		fprintf(stderr, "%s\n", buf);
		write(writefd, buf, strlen(buf));
	} else {
		// read all file contents and write to client
		while ((n = read(fd, buf, BUFSIZ)) > 0)
			write(writefd, buf, n);
		close(fd);
	}
}
