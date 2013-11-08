////////////////////////////////////////////////////////////////////////////////
// DEBUG FUNCTIONS
//

unsigned print_string(char value[]){
	unsigned i = 0;
	while( value[i] != 0 ){
		output_rs232_tx(value[i]);
		i++;
	}

	return 0;
}

unsigned nibble_to_hex(unsigned nibble){
	if( nibble > 9 ) return nibble + ('a' - 10);
	return nibble + '0';
}

unsigned print_hex(unsigned value){

	output_rs232_tx(nibble_to_hex((value >> 12) & 0xf));
	output_rs232_tx(nibble_to_hex((value >> 8)  & 0xf));
	output_rs232_tx(' ');
	output_rs232_tx(nibble_to_hex((value >> 4)  & 0xf));
	output_rs232_tx(nibble_to_hex((value     )  & 0xf));
	output_rs232_tx(' ');
	return 0;
}

unsigned high = 1;
unsigned data;

unsigned put_char(char x){
	if(high){
		high = 0;
		data = x << 8;
	} else {
		high = 1;
		data |= x & 0xff;
		output_socket(data);
	}
	return 0;
}

unsigned flush(){
	if(!high) output_socket(data);
	return 0;
}

unsigned put_string(unsigned string[]){
	unsigned i;
	while(string[i]){
		put_char(string[i]);
		i++;
	}
	return 0;
}

unsigned put_decimal(unsigned value){
	int digit_0 = '0';
	int digit_1 = '0';
	int digit_2 = '0';
	int digit_3 = '0';
	int digit_4 = '0';

	while(value >= 10000){
		digit_4++;
		value -= 10000;
	}
	put_char(digit_4);
	while(value >= 1000){
		digit_3++;
		value -= 1000;
	}
	put_char(digit_3);
	while(value >= 100){
		digit_2++;
		value -= 100;
	}
	put_char(digit_2);
	while(value >= 10){
		digit_1++;
		value -= 10;
	}
	put_char(digit_1);
	while(value >= 1){
		digit_0++;
		value -= 1;
	}
	put_char(digit_0);
	return 0;
}


unsigned HTTP_GET_response(int body[]){
	unsigned header_length;
	unsigned body_length;
	unsigned header[] = 
"HTTP/1.1 200 OK\r\n\
Date: Thu Oct 31 19:16:00 2013\r\n\
Server: chips-web/0.0\r\n\
Content-Type: text/html\r\n\
Content-Length: ";

	//calculate length of header
	header_length = 0;
	while(header[header_length]){
		header_length ++;
	}

	//calculate length of body
	body_length = 0;
	while(body[body_length]){
		body_length ++;
	}
	print_string("Sending Response: "); print_hex(header_length + body_length + 9); print_string("bytes\n");

	//send via socket interface
	output_socket(header_length + body_length + 9);
	put_string(header);
	put_decimal(body_length);
	put_string("\r\n\r\n");
	put_string(body);
	flush();
	return 0;
}

unsigned user_design()
{
	//simple echo application
	unsigned length;
	unsigned i, index;
	unsigned data[1460];
	unsigned word;
	while(1){

		length = input_socket();
		index = 0;
		for(i=0;i<length;i+=2){
			data[index] = input_socket();
			index++;
		}
		print_string("Incoming Packet, size: "); print_hex(length); print_string("bytes\n");

		HTTP_GET_response("<html><head><title>An Example Page</title></head><body>Hello World, this is a very simple HTML document.</body> </html>");

	}

        //dummy access to peripherals
	output_leds(0x5);
	input_rs232_rx();
	output_rs232_tx(1);
	return 0;
}
