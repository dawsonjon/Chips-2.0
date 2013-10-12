int print_string(char value[]){
	int i = 0;
	while( value[i] != 0 ){
		output_rs232_tx(value[i]);
		i++;
	}

	return 0;
}

int nibble_to_hex(int nibble){
	if( nibble > 9 ) return nibble + ('a' - 10);
	return nibble + '0';
}

int print_hex(int value){
	output_rs232_tx(nibble_to_hex((value >> 12) & 0xf));
	output_rs232_tx(nibble_to_hex((value >> 8)  & 0xf));
	output_rs232_tx(' ');
	output_rs232_tx(nibble_to_hex((value >> 4)  & 0xf));
	output_rs232_tx(nibble_to_hex((value     )  & 0xf));
	output_rs232_tx(' ');
	return 0;
}

////////////////////////////////////////////////////////////////////////////////
// Data Link Layer - Ethernet
//

int local_mac_address_hi = 0x0001;
int local_mac_address_med = 0x0203;
int local_mac_address_lo = 0x0405;

int get_ethernet_packet(int packet[]){
	print_string("get_eth");
        int number_of_bytes, index;
	int byte;

	number_of_bytes = input_eth_rx();
	index = 0;
	for(byte=0; byte<number_of_bytes; byte+=2){
		packet[index] = input_eth_rx();
		index ++;
	}
	return number_of_bytes;
}

int put_ethernet_packet(
		int packet[], 
		int number_of_bytes,
		int destination_mac_address_hi,
		int destination_mac_address_med,
		int destination_mac_address_lo,
		int protocol){

        int byte, index;
	print_string("put_eth");

        //set up ethernet header
	packet[0] = destination_mac_address_hi;
	packet[1] = destination_mac_address_med;
	packet[2] = destination_mac_address_lo;
	packet[3] = local_mac_address_hi;
	packet[4] = local_mac_address_med;
	packet[5] = local_mac_address_lo;
	packet[6] = protocol;

	output_eth_tx(number_of_bytes);
	index = 0;
	for(byte=0; byte<number_of_bytes; byte+=2){
		output_eth_tx(packet[index]);
		index ++;
	}
	return 0;
}

////////////////////////////////////////////////////////////////////////////////
// Network Layer - Internet Protocol
//
int local_ip_address_hi = 0xc0A8;//192/168
int local_ip_address_lo = 0x0101;//1/1

int get_ip_packet(int packet[]){
	int tx_packet[64];
	print_string("get_ip");
	while(1){
		number_of_bytes = get_ethernet_packet(packet);
		if (packet[6] == 0x0800){ //IPv4
			print_string("ip");
		} 
		else if (packet[6] == 0x0806){ //ARP
			print_string("arp");

			//construct and send an ARP response
			tx_packet[7] = 0x0001; //HTYPE ethernet
			tx_packet[8] = 0x0800; //PTYPE IPV4
			tx_packet[9] = 0x0604; //HLEN, PLEN
			tx_packet[10] = 0x0002; //OPER=REPLY
			tx_packet[11] = local_mac_address_hi; //SENDER_HARDWARE_ADDRESS
			tx_packet[12] = local_mac_address_med; //SENDER_HARDWARE_ADDRESS
			tx_packet[13] = local_mac_address_lo; //SENDER_HARDWARE_ADDRESS
			tx_packet[14] = local_ip_address_hi; //SENDER_PROTOCOL_ADDRESS
			tx_packet[15] = local_ip_address_lo; //SENDER_PROTOCOL_ADDRESS
			tx_packet[16] = packet[11]; //TARGET_HARDWARE_ADDRESS
			tx_packet[17] = packet[12]; //
			tx_packet[18] = packet[13]; //
			tx_packet[19] = packet[14]; //TARGET_PROTOCOL_ADDRESS
			tx_packet[20] = packet[15]; //
			put_ethernet_packet(
				tx_packet, 
				64,
				packet[11],
		                packet[12],
		                packet[13],
				0x0806);
		} else {
			print_string("other");
		}
	}
	return number_of_bytes;
}

int user_design()
{

	int i = 0;
	int rx_packet[1024];

	output_rs232_tx(13);
	output_rs232_tx(10);
	print_string("Ethernet Monitor");
	output_rs232_tx(13);
	output_rs232_tx(10);


        get_ip_packet(rx_packet);




        //dummy access to peripherals
	output_leds(0x5);
	output_eth_tx(0);
	input_eth_rx();
	output_rs232_tx(1);
	input_rs232_rx();
	return 0;
}
