////////////////////////////////////////////////////////////////////////////////
// TCP-IP User Settings
//

unsigned local_mac_address_hi = 0x0001;
unsigned local_mac_address_med = 0x0203;
unsigned local_mac_address_lo = 0x0405;
unsigned local_ip_address_hi = 0xc0A8;//192/168
unsigned local_ip_address_lo = 0x0101;//1/1
unsigned local_port = 23;//telnet

////////////////////////////////////////////////////////////////////////////////
// TCP-IP GLOBALS
//

unsigned tx_packet[512];

////////////////////////////////////////////////////////////////////////////////
// Checksum calculation routines
//
 
//store checksum in a global variable
//unsigneds are 16 bits, so use an array of 2 to hold a 32 bit number
 
unsigned checksum;
 
//Reset checksum before calculation
//
 
unsigned reset_checksum(){
  checksum = 0;

  //success
  return 0;
}
 
//Add 16 bit data value to 32 bit checksum value
//
 
unsigned add_checksum(unsigned data){
  unsigned temp;
 
  //perform addition
  temp = checksum + data;
 
  //Check for carry
  if(temp < data) temp++;
  checksum = temp;
 
  //success
  return 0;
}
 
//Retrieve the calculated checksum
//
 
unsigned check_checksum(){
  return ~checksum;
}

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

////////////////////////////////////////////////////////////////////////////////
// UTILITY FUNCTIONS
//

unsigned calc_ack(unsigned ack[], unsigned seq[], unsigned length){
	//given a two word sequence number and a one word length
	//calculate a two word acknowledgement number
	//check whether we have new data or not
	unsigned new_ack_0;
	unsigned new_ack_1;
	unsigned return_value = 0;
	new_ack_0 = seq[0] + length;
	new_ack_1 = seq[1];
	if(new_ack_0 < length) new_ack_1 = new_ack_1 + 1;

	//Is this data we have allready acknowledged?
	if((new_ack_0 != ack[0]) || (new_ack_1 != ack[1])){
		ack[0] = new_ack_0;
		ack[1] = new_ack_1;
		return_value = 1;
	}
	return return_value;
}
			
////////////////////////////////////////////////////////////////////////////////
// Data Link Layer - Ethernet
//

unsigned put_ethernet_packet(
		unsigned packet[], 
		unsigned number_of_bytes,
		unsigned destination_mac_address_hi,
		unsigned destination_mac_address_med,
		unsigned destination_mac_address_lo,
		unsigned protocol){

        unsigned byte, index;

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

unsigned get_ethernet_packet(unsigned packet[]){

        unsigned number_of_bytes, index;
	unsigned byte;

	while(1){
		number_of_bytes = input_eth_rx();
		index = 0;
		for(byte=0; byte<number_of_bytes; byte+=2){
			packet[index] = input_eth_rx();
			index ++;
		}

                //Filter out packets not meant for us
		if(packet[0] != local_mac_address_hi && packet[0] != 0xffff) continue;
		if(packet[1] != local_mac_address_med && packet[1] != 0xffff) continue;
		if(packet[2] != local_mac_address_lo && packet[2] != 0xffff) continue;

                //Process ARP requests within the data link layer
	        if (packet[6] == 0x0806){ //ARP

			//respond to requests
			if (packet[10] == 0x0001){
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
			}
			continue;
		}
		break;
	}
	return number_of_bytes;
}

unsigned arp_ip_hi[16];
unsigned arp_ip_lo[16];
unsigned arp_mac_0[16];
unsigned arp_mac_1[16];
unsigned arp_mac_2[16];
unsigned arp_pounsigneder = 0;

//return the location of the ip address in the arp cache table
unsigned get_arp_cache(unsigned ip_hi, unsigned ip_lo){

        unsigned number_of_bytes;
	unsigned byte;
	unsigned packet[16];
	unsigned i;

	//Is the requested IP in the ARP cache?
	for(i=0; i<16; i++){
		if(arp_ip_hi[i] == ip_hi && arp_ip_lo[i] == ip_lo){
			return i;
		}
	}

        //It is not, so send an arp request
	tx_packet[7] = 0x0001; //HTYPE ethernet
	tx_packet[8] = 0x0800; //PTYPE IPV4
	tx_packet[9] = 0x0604; //HLEN, PLEN
	tx_packet[10] = 0x0001; //OPER=REQUEST
	tx_packet[11] = local_mac_address_hi; //SENDER_HARDWARE_ADDRESS
	tx_packet[12] = local_mac_address_med; //SENDER_HARDWARE_ADDRESS
	tx_packet[13] = local_mac_address_lo; //SENDER_HARDWARE_ADDRESS
	tx_packet[14] = local_ip_address_hi; //SENDER_PROTOCOL_ADDRESS
	tx_packet[15] = local_ip_address_lo; //SENDER_PROTOCOL_ADDRESS
	tx_packet[19] = ip_hi; //TARGET_PROTOCOL_ADDRESS
	tx_packet[20] = ip_lo; //
	put_ethernet_packet(
		tx_packet, 
		64,
		0xffff, //broadcast via ethernet
		0xffff,
		0xffff,
		0x0806);

        //wait for a response
	while(1){

		number_of_bytes = input_eth_rx();
		i = 0;
		for(byte=0; byte<number_of_bytes; byte+=2){
			//only keep the part of the packet we care about
			if(i < 16){
				packet[i] = input_eth_rx();
			} else {
				input_eth_rx();
			}
			i++;
		}

                //Process ARP requests within the data link layer
	        if (packet[6] == 0x0806 && packet[10] == 0x0002){
			if (packet[14] == ip_hi && packet[15] == ip_lo){
				arp_ip_hi[arp_pounsigneder] = ip_hi;
				arp_ip_lo[arp_pounsigneder] = ip_lo;
				arp_mac_0[arp_pounsigneder] = packet[11];
				arp_mac_1[arp_pounsigneder] = packet[12];
				arp_mac_2[arp_pounsigneder] = packet[13];
				i = arp_pounsigneder;
				arp_pounsigneder++;
				if(arp_pounsigneder == 16) arp_pounsigneder = 0;
				return i;
			}
		}
	}
}

////////////////////////////////////////////////////////////////////////////////
// Network Layer - Internet Protocol
//

unsigned put_ip_packet(unsigned packet[], unsigned total_length, unsigned protocol, unsigned ip_hi, unsigned ip_lo){
	unsigned number_of_bytes, i, arp_cache;

	//see if the requested IP address is in the arp cache
	arp_cache = get_arp_cache(ip_hi, ip_lo);

        //Form IP header
	packet[7] = 0x4500;              //Version 4 header length 5x32
	packet[8] = total_length;        //IP data + header
	packet[9] = 0x0000;              //Identification
	packet[10] = 0x4000;             //don't fragment
	packet[11] = 0xFF00 | protocol;  //ttl|protocol
	packet[12] = 0x0000;             //checksum
	packet[13] = local_ip_address_hi;//source_high
	packet[14] = local_ip_address_lo;//source_low
	packet[15] = ip_hi;              //dest_high
	packet[16] = ip_lo;              //dest_low
	number_of_bytes = total_length + 14;

	//calculate checksum
        reset_checksum();
	for(i=7; i<=16; i++){
		add_checksum(packet[i]);
	}
	packet[12] = check_checksum();

	//enforce minimum ethernet frame size
	if(number_of_bytes < 64){
		number_of_bytes = 64;
	}

	//send packet over ethernet
	put_ethernet_packet(
		packet,                  //packet
		number_of_bytes,         //number_of_bytes
	       	arp_mac_0[arp_cache],    //destination mac address
		arp_mac_1[arp_cache],    //
		arp_mac_2[arp_cache],    //
		0x0800);                 //protocol IPv4
	return 0;
}

unsigned get_ip_packet(unsigned packet[]){
	unsigned ip_payload;
	unsigned total_length;
	unsigned header_length;
	unsigned payload_start;
	unsigned payload_length;
	unsigned i, from, to;
	unsigned payload_end;

	while(1){
		number_of_bytes = get_ethernet_packet(packet);

		if (packet[6] == 0x0800){ //IPv4
			//check the destination address matches, and return
			if(packet[15] != local_ip_address_hi) continue;
			if(packet[16] != local_ip_address_lo) continue;
			if((packet[11] & 0xff) == 1){//ICMP

				header_length = ((packet[7] >> 8) & 0xf) << 1;                   //in words
				payload_start = header_length + 7;                               //in words
				total_length = packet[8];                                        //in bytes
				payload_length = ((total_length+1) >> 1) - header_length;        //in words
				payload_end = payload_start + payload_length - 1;                //in words

				if(packet[payload_start] == 0x0800){//ping request

					//copy icmp packet to response
					to = 19;//assume that 17 and 18 are 0
					reset_checksum();
					for(from=payload_start+2; from<=payload_end; from++){
						i = packet[from];
						add_checksum(i);
						tx_packet[to] = i;
						to++;
					}
					tx_packet[17] = 0;//ping response
					tx_packet[18] = check_checksum();

					//send ping response
					put_ip_packet(
						tx_packet,
						total_length,
						1,//icmp
						packet[13], //remote ip
						packet[14]  //remote ip
					);
				}
					        
			} else if((packet[11] & 0xff) == 6){//TCP
				return number_of_bytes;
			}
		}
	}
}

////////////////////////////////////////////////////////////////////////////////
// Transport Layer - TCP
//

unsigned remote_ip_hi, remote_ip_lo;

unsigned tx_source=0;
unsigned tx_dest=0;
unsigned tx_seq[2];
unsigned next_tx_seq[2];
unsigned tx_ack[2];
unsigned tx_window=1460; //ethernet MTU - 40 bytes for TCP/IP header

unsigned tx_fin_flag=0;
unsigned tx_syn_flag=0;
unsigned tx_rst_flag=0;
unsigned tx_psh_flag=0;
unsigned tx_ack_flag=0;
unsigned tx_urg_flag=0;

unsigned rx_source=0;
unsigned rx_dest=0;
unsigned rx_seq[2];
unsigned rx_ack[2];
unsigned rx_window=0;

unsigned rx_fin_flag=0;
unsigned rx_syn_flag=0;
unsigned rx_rst_flag=0;
unsigned rx_psh_flag=0;
unsigned rx_ack_flag=0;
unsigned rx_urg_flag=0;

unsigned put_tcp_packet(unsigned tx_packet [], unsigned tx_length){

        unsigned payload_start = 17;
	unsigned packet_length;
	unsigned index;

	//encode TCP header
	tx_packet[payload_start + 0] = tx_source;
	tx_packet[payload_start + 1] = tx_dest;
	tx_packet[payload_start + 2] = tx_seq[1];
	tx_packet[payload_start + 3] = tx_seq[0];
	tx_packet[payload_start + 4] = tx_ack[1];
	tx_packet[payload_start + 5] = tx_ack[0];
	tx_packet[payload_start + 6] = 0x5000; //5 long words
	tx_packet[payload_start + 7] = tx_window;
	tx_packet[payload_start + 8] = 0;
	tx_packet[payload_start + 9] = 0;


	//encode flags
	
	if(tx_fin_flag) tx_packet[payload_start + 6] |= 0x01;
	if(tx_syn_flag) tx_packet[payload_start + 6] |= 0x02;
	if(tx_rst_flag) tx_packet[payload_start + 6] |= 0x04;
	if(tx_psh_flag) tx_packet[payload_start + 6] |= 0x08;
	if(tx_ack_flag) tx_packet[payload_start + 6] |= 0x10;
	if(tx_urg_flag) tx_packet[payload_start + 6] |= 0x20;

	//calculate checksum
	//length of payload + header + pseudo_header in words
        reset_checksum();
        add_checksum(local_ip_address_hi);
        add_checksum(local_ip_address_lo);
        add_checksum(remote_ip_hi);
        add_checksum(remote_ip_lo);
        add_checksum(0x0006);
        add_checksum(tx_length+20);//tcp_header + tcp_payload in bytes

	packet_length = (tx_length + 20 + 1) >> 1; 
	index = payload_start;
	for(i=0; i<packet_length; i++){
		add_checksum(tx_packet[index]);
		index++;
	}
	tx_packet[payload_start + 8] = check_checksum();

	put_ip_packet(
		tx_packet,
		tx_length + 40,
		6,//tcp
		remote_ip_hi, //remote ip
		remote_ip_lo  //remote ip
	);
	return 0;
}

unsigned rx_length, rx_start;

unsigned get_tcp_packet(unsigned rx_packet []){

        unsigned number_of_bytes, header_length, payload_start, total_length, payload_length, payload_end, tcp_header_length;

	number_of_bytes = get_ip_packet(rx_packet);

	//decode lengths from the IP header
	header_length = ((rx_packet[7] >> 8) & 0xf) << 1;                  //in words
	payload_start = header_length + 7;                                 //in words

	total_length = rx_packet[8];                                       //in bytes
	payload_length = total_length - (header_length << 1);              //in bytes
	tcp_header_length = ((rx_packet[payload_start + 6] & 0xf000)>>10); //in bytes
	rx_length = payload_length - tcp_header_length;                    //in bytes
	rx_start = payload_start + (tcp_header_length >> 1);               //in words

	//decode TCP header
	rx_source = rx_packet[payload_start + 0];
	rx_dest   = rx_packet[payload_start + 1];
	rx_seq[1] = rx_packet[payload_start + 2];
	rx_seq[0] = rx_packet[payload_start + 3];
	rx_ack[1] = rx_packet[payload_start + 4];
	rx_ack[0] = rx_packet[payload_start + 5];
	rx_window = rx_packet[payload_start + 7];

	//decode flags
	rx_fin_flag = rx_packet[payload_start + 6] & 0x01;
	rx_syn_flag = rx_packet[payload_start + 6] & 0x02;
	rx_rst_flag = rx_packet[payload_start + 6] & 0x04;
	rx_psh_flag = rx_packet[payload_start + 6] & 0x08;
	rx_ack_flag = rx_packet[payload_start + 6] & 0x10;
	rx_urg_flag = rx_packet[payload_start + 6] & 0x20;

	return 0;


}

unsigned application_put_data(unsigned packet[], unsigned start, unsigned length){
	unsigned i, index, data;

	index = start;
	for(i=0; i<length; i+=2){
		data = packet[index];
		if (i > 1) {
			output_rs232_tx(data >> 8);	
		}
		output_rs232_tx(data & 0xff);	
		index++;
	}
	return 0;
}

unsigned application_get_data(unsigned packet[], unsigned start){
	unsigned data[] = "Message to outside world\n";
	unsigned i, word, index;
	index = start;

	i = 0;
	while(1){
		if(data[i]){
			word = data[i] << 8;
		} else {
			break;
		}
		i++;
		if(data[i]){
			word |= data[i];
		} else {
			packet[index] = word;
			break;
		}
		packet[index] = word;
		i++;
		index++;
	}
	return i;
}

unsigned user_design()
{

	unsigned rx_packet[1024];
	unsigned tx_packet[1024];
	unsigned tx_start = 27;

	unsigned listen = 1;
	unsigned syn_rxd = 2;
	unsigned established = 3;
	unsigned wait_close = 4;

	unsigned state = listen;
	unsigned new_rx_data = 0;
	unsigned new_tx_data = 0;
	unsigned tx_length;
	unsigned timer;
	tx_seq[0] = 0;
	tx_seq[1] = 0;

        while(1){ 

		if(state == listen){

			while(1){
				get_tcp_packet(rx_packet);
				if(rx_dest == local_port) break;
			}
			if(rx_syn_flag){

				remote_ip_hi = rx_packet[13];
				remote_ip_lo = rx_packet[14];
				tx_dest = rx_source;
				tx_source = local_port;

				calc_ack(tx_ack, rx_seq, 1);

				tx_syn_flag = 1;
				tx_ack_flag = 1;
				state = syn_rxd;
				put_tcp_packet(tx_packet, 0);
			}

		} else if(state == syn_rxd){

			while(1){
				get_tcp_packet(rx_packet);
				if(rx_dest == local_port) break;
			}
			if(rx_ack_flag){
				state = established;
				tx_seq[1] = rx_ack[1];
				tx_seq[0] = rx_ack[0];
				next_tx_seq[1] = rx_ack[1];
				next_tx_seq[0] = rx_ack[0];
				tx_syn_flag = 0;
				tx_ack_flag = 0;
			}
			//TODO, retry if no acknowledgement

		} else if(state == established) {

			while(1){
				get_tcp_packet(rx_packet);
				if(rx_dest == local_port) break;
			}

			tx_ack_flag = 1;
			if(rx_fin_flag){

				//client disconnect
				tx_ack_flag = 1;
				tx_fin_flag = 1;
				calc_ack(tx_ack, rx_seq, 1);
				state = wait_close;
				put_tcp_packet(tx_packet, 0);

			} else {

				//tcp -> application
				new_rx_data = calc_ack(tx_ack, rx_seq, rx_length);
				if(new_rx_data){
					application_put_data(rx_packet, rx_start, rx_length);
				}

				//application -> tcp
				if(rx_ack_flag && (next_tx_seq[1] == rx_ack[1]) && (next_tx_seq[0] == rx_ack[0])){
					tx_length = application_get_data(tx_packet, tx_start);
					tx_seq[0] = next_tx_seq[0];
					tx_seq[1] = next_tx_seq[1];
					calc_ack(next_tx_seq, tx_seq, tx_length);
					//TODO check tx_length < rx_window
				}

				put_tcp_packet(tx_packet, tx_length);

			}

		} else if(state == wait_close) {

			while(1){
				get_tcp_packet(rx_packet);
				if(rx_dest == local_port) break;
			}
			if(rx_ack_flag){
				state = listen;
				tx_syn_flag = 0;
				tx_fin_flag = 0;
				tx_ack_flag = 0;
			}

			//TODO, retry if no acknowledgement
		}

		if(rx_rst_flag){
			//client reset
		       	state = listen;
		}


	}

        //dummy access to peripherals
	output_leds(0x5);
	input_rs232_rx();
	output_rs232_tx(1);
	return 0;
}
