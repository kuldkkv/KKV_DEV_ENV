#include <stdio.h>
#include <stdlib.h>

long fact(long inp)
{
	if (inp <= 1)
		return 1;

	return inp * fact(inp-1);
}


int main(int argc, char **argv)
{
	if (argc <= 1)	{
		printf("usage: fact.c <number");
		exit(1);
	}

	printf("%d\n", fact(atoi(argv[1])));
	return 0;
}

