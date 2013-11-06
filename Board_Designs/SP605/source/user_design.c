////////////////////////////////////////////////////////////////////////////////
// DEBUG FUNCTIONS
//

//unsigned prunsigned_string(char value[]){
//	unsigned i = 0;
//	while( value[i] != 0 ){
//		output_rs232_tx(value[i]);
//		i++;
//	}
//
//	return 0;
//}

//unsigned nibble_to_hex(unsigned nibble){
//	if( nibble > 9 ) return nibble + ('a' - 10);
//	return nibble + '0';
//}

//unsigned prunsigned_hex(unsigned value){
//
//	output_rs232_tx(nibble_to_hex((value >> 12) & 0xf));
//	output_rs232_tx(nibble_to_hex((value >> 8)  & 0xf));
//	output_rs232_tx(' ');
//	output_rs232_tx(nibble_to_hex((value >> 4)  & 0xf));
//	output_rs232_tx(nibble_to_hex((value     )  & 0xf));
//	output_rs232_tx(' ');
//	return 0;
//}

unsigned user_design()
{
	//simple echo application
	unsigned length;
	unsigned i, index;
	unsigned data[1460];
	unsigned response[] = "HTTP/1.1 200 OK\r\nDate: Thu Oct 31 19:16:00 2013\r\nServer: blah\r\nContent-Type: text/html\r\nContent-Length: 118\r\n\r\n<html><head><title>An Example Page</title></head><body>Hello World, this is a very simple HTML document.</body> </html>";
	unsigned word;
	while(1){

		length = input_socket();
		index = 0;
		for(i=0;i<length;i+=2){
			data[index] = input_socket();
			index++;
		}

		output_socket(231);
		index = 0;
		for(i=0;i<231;i+=2){
			word = response[index] << 8;
			index++;
			word |= response[index] & 0xff;
			index++;
			output_socket(word);
		}

	}

        //dummy access to peripherals
	output_leds(0x5);
	input_rs232_rx();
	output_rs232_tx(1);
	return 0;
}
