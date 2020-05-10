#include <stdio.h>
#include "/home/kkv/DEV/C/static_lib/src/lib_mylib.h"

int main()
{
    printf("before dynamic call\n");
    fun_mylib();
    printf("after dynamic main\n");

    return 0;
}

