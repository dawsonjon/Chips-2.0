////////////////////////////////////////////////////////////////////////////////
// TCP-IP User Settings
//

int local_mac_address_hi = 0x0001;
int local_mac_address_med = 0x0203;
int local_mac_address_lo = 0x0405;
int local_ip_address_hi = 0xc0A8;//192/168
int local_ip_address_lo = 0x0101;//1/1
int local_port = 23;//telnet

////////////////////////////////////////////////////////////////////////////////
// TCP-IP GLOBALS
//

int tx_packet[512];

////////////////////////////////////////////////////////////////////////////////
// DEBUG FUNCTIONS
//

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
// UTILITY FUNCTIONS
//

int calc_ack(int ack[], int seq[], int length){
	//given a two word sequence number and a one word length
	//calculate a two word acknowledgement number
	//check whether we have new data or not
	int new_ack_0;
	int new_ack_1;
	int return_value = 0;
	new_ack_0 = seq[0] + length;
	new_ack_1 = seq[1];
	if((seq[0] | length) & 0x8000){
		if(!(new_ack_0 & 0x8000)){
			new_ack_1 = new_ack_1 + 1;
		}
	}
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

int put_ethernet_packet(
		int packet[], 
		int number_of_bytes,
		int destination_mac_address_hi,
		int destination_mac_address_med,
		int destination_mac_address_lo,
		int protocol){

        int byte, index;
	print_string("put_eth\n");

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

int get_ethernet_packet(int packet[]){
	print_string("get_eth\n");
        int number_of_bytes, index;
	int byte;

	while(1){
		number_of_bytes = input_eth_rx();
		//print_string("reading bytes: "); print_hex(number_of_bytes); print_string("\n");
		index = 0;
		for(byte=0; byte<number_of_bytes; byte+=2){
			packet[index] = input_eth_rx();
			index ++;
		}
		//print_string("done\n");

                //Filter out packets not meant for us
		//print_hex(packet[0]); print_string("\n");
		if(packet[0] != local_mac_address_hi && packet[0] != 0xffff) continue;
		//print_hex(packet[1]); print_string("\n");
		if(packet[1] != local_mac_address_med && packet[1] != 0xffff) continue;
		//print_hex(packet[2]); print_string("\n");
		if(packet[2] != local_mac_address_lo && packet[2] != 0xffff) continue;
		//print_string("mac good\n");

                //Process ARP requests within the data link layer
	        if (packet[6] == 0x0806){ //ARP
			//print_string("arp\n");

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

int arp_ip_hi[16];
int arp_ip_lo[16];
int arp_mac_0[16];
int arp_mac_1[16];
int arp_mac_2[16];
int arp_pointer = 0;

//return the location of the ip address in the arp cache table
int get_arp_cache(int ip_hi, int ip_lo){

        int number_of_bytes;
	int byte;
	int packet[16];
	int i;

	//Is the requested IP in the ARP cache?
	for(i=0; i<16; i++){
		if(arp_ip_hi[i] == ip_hi && arp_ip_lo[i] == ip_lo){
			//print_string("cache hit\n");
			return i;
		}
	}

	//print_string("cache miss\n");
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

	//print_string("arp request\n");

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
		//print_string("got_packet\n");

                //Process ARP requests within the data link layer
	        if (packet[6] == 0x0806 && packet[10] == 0x0002){
			//print_string("arp response\n");
			if (packet[14] == ip_hi && packet[15] == ip_lo){
				//print_string("updating cache\n");
				arp_ip_hi[arp_pointer] = ip_hi;
				arp_ip_lo[arp_pointer] = ip_lo;
				arp_mac_0[arp_pointer] = packet[11];
				arp_mac_1[arp_pointer] = packet[12];
				arp_mac_2[arp_pointer] = packet[13];
				i = arp_pointer;
				arp_pointer++;
				if(arp_pointer == 16) arp_pointer = 0;
				return i;
			}
		}
	}
}

////////////////////////////////////////////////////////////////////////////////
// Network Layer - Internet Protocol
//

int put_ip_packet(int packet[], int total_length, int protocol, int ip_hi, int ip_lo){
	print_string("put_ip\n");
	int number_of_bytes, i, arp_cache;

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
        output_checksum(10);
	for(i=7; i<=16; i++){
		output_checksum(packet[i]);
	}
	packet[12] = input_checksum();

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

int get_ip_packet(int packet[]){
	int ip_payload;
	int total_length;
	int header_length;
	int payload_start;
	int payload_length;
	int i, from, to;
	int payload_end;

	print_string("get_ip\n");
	while(1){
		number_of_bytes = get_ethernet_packet(packet);

		if (packet[6] == 0x0800){ //IPv4
			//print_string("ip\n");
			//check the destination address matches, and return
			if(packet[15] != local_ip_address_hi) continue;
			if(packet[16] != local_ip_address_lo) continue;
			//print_string("ip address good\n");
			if((packet[11] & 0xff) == 1){//ICMP

				header_length = ((packet[7] >> 8) & 0xf) << 1;                   //in words
				payload_start = header_length + 7;                               //in words
				total_length = packet[8];                                        //in bytes
				payload_length = ((total_length+1) >> 1) - header_length;        //in words
				payload_end = payload_start + payload_length - 1;                //in words

				//print_string("icmp\n");
				if(packet[payload_start] == 0x0800){//ping request
					//print_string("ping_request\n");

					//copy icmp packet to response
					to = 19;//assume that 17 and 18 are 0
					output_checksum(payload_length);
					output_checksum(0);
					output_checksum(0);
					for(from=payload_start+2; from<=payload_end; from++){
						i = packet[from];
						output_checksum(i);
						tx_packet[to] = i;
						to++;
					}
					tx_packet[17] = 0;//ping response
					tx_packet[18] = input_checksum();

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
		} else {
			//print_string("other");
		}
	}
}

////////////////////////////////////////////////////////////////////////////////
// Transport Layer - TCP
//

int remote_ip_hi, remote_ip_lo;

int tx_source=0;
int tx_dest=0;
int tx_seq[2];
int next_tx_seq[2];
int tx_ack[2];
int tx_window=1460; //ethernet MTU - 40 bytes for TCP/IP header

int tx_fin_flag=0;
int tx_syn_flag=0;
int tx_rst_flag=0;
int tx_psh_flag=0;
int tx_ack_flag=0;
int tx_urg_flag=0;

int rx_source=0;
int rx_dest=0;
int rx_seq[2];
int rx_ack[2];
int rx_window=0;

int rx_fin_flag=0;
int rx_syn_flag=0;
int rx_rst_flag=0;
int rx_psh_flag=0;
int rx_ack_flag=0;
int rx_urg_flag=0;

int put_tcp_packet(int tx_packet [], int tx_length){

	print_string("put tcp\n");

        int payload_start = 17;
	int checksum_length;
	int packet_length;
	int index;

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
	checksum_length = (tx_length + 20 + 12 + 1) >> 1; 
        output_checksum(checksum_length);
        output_checksum(local_ip_address_hi);
        output_checksum(local_ip_address_lo);
        output_checksum(remote_ip_hi);
        output_checksum(remote_ip_lo);
        output_checksum(0x0006);
        output_checksum(tx_length+20);//tcp_header + tcp_payload in bytes

	packet_length = (tx_length + 20 + 1) >> 1; 
	index = payload_start;
	for(i=0; i<packet_length; i++){
		output_checksum(tx_packet[index]);
		index++;
	}
	tx_packet[payload_start + 8] = input_checksum();

	put_ip_packet(
		tx_packet,
		tx_length + 40,
		6,//tcp
		remote_ip_hi, //remote ip
		remote_ip_lo  //remote ip
	);
	return 0;
}

int rx_length, rx_start;

int get_tcp_packet(int rx_packet []){

	print_string("get tcp\n");

        int number_of_bytes, header_length, payload_start, total_length, payload_length, payload_end, tcp_header_length;

	number_of_bytes = get_ip_packet(rx_packet);

	//decode lengths from the IP header
	header_length = ((rx_packet[7] >> 8) & 0xf) << 1;                  //in words
	payload_start = header_length + 7;                                 //in words

	total_length = rx_packet[8];                                       //in bytes
	payload_length = total_length - (header_length << 1);              //in bytes
	tcp_header_length = ((rx_packet[payload_start + 6] & 0xf000)>>10); //in bytes
	print_string("tcp_header_length ");print_hex(tcp_header_length); print_string("\n");
	rx_length = payload_length - tcp_header_length;                    //in bytes
	rx_start = payload_start + (tcp_header_length >> 1);               //in words
	print_string("rx_length ");print_hex(rx_length); print_string("\n");

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

	//print_string("flags: "); print_hex(rx_packet[payload_start + 6]); print_string("\n");
	return 0;


}

int application_put_data(int packet[], int start, int length){
	int i, index, data;
	print_string("echo data:\n");

	index = start;
	for(i=length; i>0; i-=2){
		data = packet[index];
		if (i > 1) {
			output_rs232_tx(data >> 8);	
		}
		output_rs232_tx(data & 0xff);	
		index++;
	}
	print_string("\n");
	return 0;
}

int application_get_data(int packet[], int start){
	int data[] = "Message to outside world\n";
	int i, word, index;
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

int user_design()
{

	int rx_packet[1024];
	int tx_packet[1024];
	int tx_start = 27;

	int listen = 1;
	int syn_rxd = 2;
	int established = 3;
	int wait_close = 4;

	int state = listen;
	int new_rx_data = 0;
	int new_tx_data = 0;
	int tx_length;
	int timer;
	tx_seq[0] = 0;
	tx_seq[1] = 0;

	print_string("\nEthernet Monitor\n");


        while(1){ 

		if(state == listen){

			get_tcp_packet(rx_packet);
			if(rx_syn_flag){
				print_string("incomming connection from: ");
				print_hex(rx_packet[13]);
				print_hex(rx_packet[14]);
				print_string("\n");

				remote_ip_hi = rx_packet[13];
				remote_ip_lo = rx_packet[14];
				tx_dest = rx_source;
				tx_source = local_port;

				calc_ack(tx_ack, rx_seq, 1);

				tx_syn_flag = 1;
				tx_ack_flag = 1;
				state = syn_rxd;
				put_tcp_packet(tx_packet, 0);
				print_string("waiting for acknowledgement\n");
			}

		} else if(state == syn_rxd){

		 	get_tcp_packet(rx_packet);
			if(rx_ack_flag){
				print_string("connection established\n");
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

			//transfer client data to the application
			get_tcp_packet(rx_packet);
			tx_ack_flag = 1;

			if(rx_fin_flag){

				//disconnect
				tx_ack_flag = 1;
				tx_fin_flag = 1;
				calc_ack(tx_ack, rx_seq, 1);
				state = wait_close;
				put_tcp_packet(tx_packet, 0);
				print_string("waiting for close ack\n");

			} else {

				//tcp -> application
				new_rx_data = calc_ack(tx_ack, rx_seq, rx_length);
				if(new_rx_data){
					print_string("incoming data:\n");
					application_put_data(rx_packet, rx_start, rx_length);
				}

				//application -> tcp
				if(rx_ack_flag && (next_tx_seq[1] == rx_ack[1]) && (next_tx_seq[0] == rx_ack[0])){
					tx_length = application_get_data(tx_packet, tx_start);
					tx_seq[0] = next_tx_seq[0];
					tx_seq[1] = next_tx_seq[1];
					calc_ack(next_tx_seq, tx_seq, tx_length);
					print_string("sending data\n");
					print_hex(tx_seq[0]);
					print_hex(tx_seq[1]);
					//TODO check tx_length < rx_window
				}

				put_tcp_packet(tx_packet, tx_length);

			}

		} else if(state == wait_close) {

			get_tcp_packet(rx_packet);
			if(rx_ack_flag){
				print_string("connection closed\n");
				state = listen;
				tx_syn_flag = 0;
				tx_fin_flag = 0;
				tx_ack_flag = 0;
			}

			//TODO, retry if no acknowledgement
		}

		if(rx_rst_flag){
			print_string("connection reset by client\n");
		       	state = listen;
		}


	}


        //dummy access to peripherals
	output_leds(0x5);
	output_checksum(0x5);
	input_rs232_rx();
	input_checksum();
	return 0;
}
