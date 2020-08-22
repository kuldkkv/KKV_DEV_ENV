#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <stdlib.h>
#define PORT 8080

int 
main(int argc, char const * argv[])
{
	int 		sock = 0, valread;
	struct sockaddr_in serv_addr;
	char           *hello = "Hello from client";
	char 		mesg     [1024];
	char 		buffer   [1024] = {0};
	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("\n Socket creation error \n");
		return -1;
	}
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);

	//Convert IPv4 and IPv6 addresses from text to binary form
		if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}
	if (connect(sock, (struct sockaddr *) & serv_addr, sizeof(serv_addr)) < 0) {
		printf("\nConnection Failed \n");
		return -1;
	}
	for (;;) {
		printf("enter message: ");
		//scanf("%s", mesg);
        if (fgets(mesg, sizeof(mesg), stdin) == NULL)   {
            printf("client ended\n");
            break;
        }
        mesg[strlen(mesg)-1] = '\0';
        if (strlen(mesg) <= 0)
            break;
		if (write(sock, mesg, strlen(mesg)) < 0) {
			perror("write");
			exit(EXIT_FAILURE);
		}
		printf("\nmessage sent\n");
		if ((valread = read(sock, buffer, 1024)) < 0) {
			perror("read");
			exit(EXIT_FAILURE);
		}
		buffer[valread] = 0;
		printf("from server: [%s]\n", buffer);
	}
	return 0;
}
