#include <stdio.h>
void main(){
    unsigned a = input("a");
	report(fget_long(a));
	assert(fget_long(a)==2);
	assert(fget_long(a)==3);
	assert(fget_long(a)==4);
	assert(fget_long(a)==5);
	assert(fget_long(a)==6);
	assert(fget_long(a)==7);
	assert(fget_long(a)==8);
	assert(fget_long(a)==9);
	assert(fget_long(a)==10);
	report(1);
}
