/*LZSS Compression Component*/
/*Jonathan P Dawson 2014-07.10*/

unsigned raw_in = input("raw_in");
unsigned compressed_out = output("compressed_out");

/*Send data of an arbitrary bit length*/
unsigned packed, stored = 0;
void send_bits(unsigned data, unsigned bits){
    unsigned i;
    for(i=0; i<bits; i++){
        packed >>= 1;
        packed |= (data & 1) << 31;
        data >>= 1;
        stored++;
        if(stored == 32){
            fputc(packed, compressed_out);
            stored = 0;
        }
    }
}

/*A function that reads a stream of uncompressed data, 
and creates a stream of compressed data*/

void compress(){

    unsigned pointer, match, match_length, longest_match, longest_match_length;
    unsigned buffer[N];

    unsigned new_size;

    while(1){
        for(pointer=0; pointer<N; pointer++){
            buffer[pointer] = fgetc(raw_in);
        }

        pointer=0;
        new_size = 0;
        while(pointer<N){

            /*Find the longest matching string already sent*/
            longest_match = 0;
            longest_match_length = 0;
            for(match=0; match<pointer; match++){

                /*match length of 0 indicates no match*/
                match_length = 0;

                /*search through buffer to find a match*/
                while(buffer[match+match_length] == buffer[pointer+match_length]){
                    match_length++;
                }

                /*If this is the longest match, remember it*/
                if(match_length > longest_match_length){
                    longest_match = match;
                    longest_match_length = match_length;
                }

            }

            /*send data*/
            if(longest_match_length >= 3){
                send_bits(0, 1);
                send_bits(longest_match_length, LOG2N);
                send_bits(pointer - longest_match, LOG2N);
                pointer += longest_match_length;
                new_size += LOG2N + LOG2N + 1;
            }
            else{
                send_bits(1, 1);
                send_bits(buffer[pointer], 8);
                pointer++;
                new_size += 9;
            }

            report(pointer);
        }
        /*report the compression ratio of this block in simulation*/
        report(new_size / (8.0*N));
    }
}
