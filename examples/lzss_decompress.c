/*LZSS Decmpression Component*/
/*Jonathan P Dawson 2014-07-10*/

unsigned raw_out = output("raw_out");
unsigned compressed_in = input("compressed_in");

/*A function to get data of an arbitrary bit length*/

unsigned stored = 0;
unsigned packed;
unsigned get_bits(unsigned bits){
    unsigned i, value = 0;
    for(i=0; i<bits; i++){
        if(!stored){
            stored = 32;
            packed = fgetc(compressed_in);
        }
        value >>= 1;
        value |= (packed & 1) << 31;
        packed >>= 1;
        stored--;
    }
    return value >> (32 - bits);
}


/*Decompress a stream of lzss compressed data, 
and generate a stream of raw data*/

void decompress(){
    unsigned i, pointer, distance, length, data;
    unsigned buffer[N];

    while(1){

        /*get distance length*/
        if(get_bits(1)){
            data = get_bits(8);
            buffer[pointer] = data;
            pointer++;
            fputc(data, raw_out);
        }
        else{
            length = get_bits(LOG2N);
            distance = get_bits(LOG2N);
            for(i=0; i<length; i++){
                data = buffer[pointer-distance];
                buffer[pointer] = data;
                pointer++;
                fputc(data, raw_out);
            }
        }
    }
}

            
