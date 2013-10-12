int print(int value[]){
	int i = 0;
	while( value[i] != 0 ){
		output_rs232_tx(value[i]);
		i++;
	}

	return 0;
}
int user_design()
{
	int leds = 0x5;
	int data[] = "blah\n";
	print(data);
	output_leds(leds);
	output_eth_tx(0);
	input_eth_rx();
	output_rs232_tx(1);
	input_rs232_rx();
	return 0;
}
