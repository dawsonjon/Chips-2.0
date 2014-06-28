#include <stdio.h>
void consumer(){
    unsigned a = input("a");
	assert(fget_float(a)==1);
	assert(fget_float(a)==2);
	assert(fget_float(a)==3);
	assert(fget_float(a)==4);
	assert(fget_float(a)==5);
	assert(fget_float(a)==6);
	assert(fget_float(a)==7);
	assert(fget_float(a)==8);
	assert(fget_float(a)==9);
	assert(fget_float(a)==10);
	report(1);
}
