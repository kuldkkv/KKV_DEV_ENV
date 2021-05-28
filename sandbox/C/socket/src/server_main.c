#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include "server.h"

#define PORT 8080


int
main(int argc, char **argv)
{
	int 		server_fd, client_socket_fd;
	struct sockaddr_in address;
	int 		addrlen = sizeof(address);

	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
		perror("socket failed");
		exit(EXIT_FAILURE);
	}
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(PORT);

	if (bind(server_fd, (struct sockaddr *) & address, sizeof(address)) < 0) {
		perror("bind");
		exit(EXIT_FAILURE);
	}
	if (listen(server_fd, 3) < 0) {
		perror("listen");
		exit(EXIT_FAILURE);
	}
	printf("server up and running ... press control+c to end\n");
	for (;;) {
		printf("waiting for client\n");
		client_socket_fd = accept(server_fd, (struct sockaddr *) & address, (socklen_t *) & addrlen);
		if (fork() == 0) {
			close(server_fd);
			client_handler(client_socket_fd);
			close(client_socket_fd);
			exit(0);
		}
	}
}
