void producer(){
    unsigned z = output("z");
	wait_clocks(1000);
	fputc(1, z);
	wait_clocks(1000);
	fputc(2, z);
	wait_clocks(1000);
	fputc(3, z);
	wait_clocks(1000);
	fputc(4, z);
	wait_clocks(1000);
	fputc(5, z);
	wait_clocks(1000);
	fputc(6, z);
	wait_clocks(1000);
	fputc(7, z);
	wait_clocks(1000);
	fputc(8, z);
	wait_clocks(1000);
	fputc(9, z);
	wait_clocks(1000);
	fputc(10, z);
}
