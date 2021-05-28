#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <string.h>
#include <time.h>


char           *
getcurrtime()
{
	time_t 		current_time;
	char           *current_time_str;

	current_time = time(NULL);
	current_time_str = ctime(&current_time);
    current_time_str[strlen(current_time_str)-1] = '\0';
	return current_time_str;
}


void 
client_handler(int client_socket_fd)
{
	char 		buffer   [BUFSIZ];
	char 		server_hello[BUFSIZ];
	char 		client_handler_id[100];
	int 		valread;

	sprintf(client_handler_id, "server thread [%d]", getpid());
	printf("%s started at [%s]\n", client_handler_id, getcurrtime());

	for (;;) {
		valread = read(client_socket_fd, buffer, BUFSIZ);
		if (valread <= 0) {
			printf("%s, %s: client ended\n", client_handler_id, getcurrtime());
			break;
		}
		buffer[valread] = '\0';
		printf("%s, %s: from client: [%s]\n", client_handler_id, getcurrtime(), buffer);
		sprintf(server_hello, "%s, %s: hello", client_handler_id, getcurrtime());
		send(client_socket_fd, server_hello, strlen(server_hello), 0);
	}
}
