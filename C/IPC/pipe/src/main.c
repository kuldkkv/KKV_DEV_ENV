#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>

void client(int, int);
void server(int, int);

int main(int argc, char **argv)
{
	int pipe1[2], pipe2[2];
	pid_t childpid;

	if (pipe(pipe1) == -1) {
		perror("pipe1");
		exit(EXIT_FAILURE);
	}

	if (pipe(pipe2) == -1) {
		perror("pipe2");
		exit(EXIT_FAILURE);
	}

	childpid = fork();
	if (childpid == -1) {
		perror("fork");
		exit(EXIT_FAILURE);
	}
	if (childpid == 0) {
		close(pipe1[1]);	// close write end of pipe1
		close(pipe2[0]);	// close read end of pipe2
		server(pipe1[0], pipe2[1]);
		exit(EXIT_SUCCESS);
	}
	// parent
	close(pipe1[0]);	// close read end of pipe1
	close(pipe2[1]);	// close write end of pipe2
	client(pipe2[0], pipe1[1]);
	wait(NULL);
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
