
int foo(void)	{
}

_start()
{
	foo();
	__asm__("leave");
}

