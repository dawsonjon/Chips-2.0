int print(int value[]){
	int i;
	for(i=0; i<5; i++){
		report(value[i]);
	}
	return 0;
}
int user_design()
{
	int data[] = "blah";
	report(data[0]);
	print(data);
	return 0;
}
