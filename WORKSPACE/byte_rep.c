#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


char* byte_rep(int);
char *init_string(char);
void reverse_string(char*, char*);
void show_usage_and_exit();

int BYTE_ARR_WIDTH = 0;
char *NAME;

void show_usage_and_exit()
{
	fprintf(stderr, "Usage: %s -i <integer in decimal> -b <byte size>\n", NAME);
	exit(1);
}


int main(int argc, char **argv)
{
	int inp_int = 0, byte_size = 0, opt;
	char int_inp_flag, byte_inp_flag;

	int_inp_flag = byte_inp_flag = 0;
	NAME = argv[0];

	while ((opt = getopt(argc, argv, "i:b:")) != -1) {
		switch(opt) {
			case 'i':
				inp_int = atoi(optarg);
				int_inp_flag = 1;
				break;
			case 'b':
				byte_size = atoi(optarg);
				byte_inp_flag = 1;
				break;
			default:
				show_usage_and_exit();
		}
	}
	
	if (int_inp_flag == 0 || byte_inp_flag == 0) {
		fprintf(stderr, "Input both parameters.");
		show_usage_and_exit();
	}
	BYTE_ARR_WIDTH = byte_size * 8;

	printf("integer [%d] in binary representation of [%d] bytes is [%s]\n", inp_int, BYTE_ARR_WIDTH/8,
		byte_rep(inp_int)
	      );
	return 0;
}

char* init_string(char init_char)
{
	char *byte_rep_out = (char *) malloc (sizeof(char) * BYTE_ARR_WIDTH+1);

	memset(byte_rep_out, init_char, BYTE_ARR_WIDTH);
	//printf("in init_string [%s]\n", byte_rep_out);
	byte_rep_out[BYTE_ARR_WIDTH] = '\0';
	return byte_rep_out;
}

void strrev(char *inp, char *out)
{
	int i, j, inp_len = strlen(inp);

	for(i = 0, j = BYTE_ARR_WIDTH; i < inp_len && j > 0; )
		out[--j] = inp[i++];
}


char* byte_rep(int n)
{
	unsigned int ONE = 1;
	char *byte_rep;
	char *byte_rep_out;
	int i = 0, b;
	
	byte_rep = (char *) malloc(sizeof(char) * BYTE_ARR_WIDTH + 1);
	byte_rep_out = init_string('0');
	while (n != 0 && i < BYTE_ARR_WIDTH) {
		b = n & ONE;
		byte_rep[i++] = b ? '1': '0';
		//printf("b [%d] i [%d] n [%d]\n", b, i, n);
		n >>= ONE;
	}
	byte_rep[i] = '\0';
	//printf("before rev byte_rep [%s]\n", byte_rep);

	strrev(byte_rep, byte_rep_out);
	
	//printf("byte_rep_out [%s]\n", byte_rep_out);
	return byte_rep_out;
}
