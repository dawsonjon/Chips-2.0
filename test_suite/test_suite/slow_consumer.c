void consumer(){
    unsigned a = input("a");
	wait_clocks(1000);
	assert(fgetc(a)==1);
	wait_clocks(1000);
	assert(fgetc(a)==2);
	wait_clocks(1000);
	assert(fgetc(a)==3);
	wait_clocks(1000);
	assert(fgetc(a)==4);
	wait_clocks(1000);
	assert(fgetc(a)==5);
	wait_clocks(1000);
	assert(fgetc(a)==6);
	wait_clocks(1000);
	assert(fgetc(a)==7);
	wait_clocks(1000);
	assert(fgetc(a)==8);
	wait_clocks(1000);
	assert(fgetc(a)==9);
	wait_clocks(1000);
	assert(fgetc(a)==10);
	report(1);
}
