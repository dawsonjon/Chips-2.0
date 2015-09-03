void consumer(){
    unsigned a = input("a");
	assert(fgetc(a)==1);
	assert(fgetc(a)==2);
	assert(fgetc(a)==3);
	assert(fgetc(a)==4);
	assert(fgetc(a)==5);
	assert(fgetc(a)==6);
	assert(fgetc(a)==7);
	assert(fgetc(a)==8);
	assert(fgetc(a)==9);
	assert(fgetc(a)==10);
}
