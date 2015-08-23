examples = {
"Edge Detection" : """
/*Edge Detection*/
/*Jonathan P Dawson 2014-07-06*/

const int HEIGHT = 64;
const int WIDTH = 64;
const int SIZE = 4096;

void set_xy(int image[], int x, int y, int pixel){
    if(x<0) return;
    if(x>=WIDTH) return;
    image[x+y*WIDTH] = pixel;
}

int get_xy(int image[], int x, int y){
    if(x<0) return 0;
    if(x>=WIDTH) return 0;
    return image[x+y*WIDTH];
}

void main()
{

    unsigned image_in = input("image_in");
    unsigned image_out = output("image_out");

    unsigned image[SIZE];
    unsigned new_image[SIZE];

    int x, y, pixel;

    while(1){

        /* read in image */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){
                set_xy(image, x, y, fgetc(image_in));
            }
        }

        /* apply edge detect */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){

                pixel =  get_xy(image, x,   y  ) << 2;
                pixel -= get_xy(image, x-1, y+1);
                pixel -= get_xy(image, x+1, y-1);
                pixel -= get_xy(image, x-1, y-1);
                pixel -= get_xy(image, x+1, y+1);
                set_xy(new_image, x, y, pixel);
            }
        }

        /* write out image */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){
                fputc(get_xy(new_image, x, y), image_out);
            }
        }

    }
}
""",

"FIR Filter":"""
/* Chips-2.0 FIR Filter Example */
/* Jonathan P Dawson 2014-07-05 */

#include <stdio.h>

unsigned in = input("a");
unsigned out = output("z");
unsigned kernel_in = input("k");

const int N = 10;

void fir_filter(){
    unsigned i = 0;
    unsigned inp = 0;
    float delay[N];
    float kernel[N];
    float data_out;

    /* read in filter kernel */
    for(i=0; i<N; i++){
       kernel[i] = fget_float(kernel_in);
    }


    /* execute filter on input stream */
    while(1){
        delay[inp] = fget_float(in);
        data_out=0.0; i=0;
        while(1){
            data_out += delay[inp] * kernel[i];
            if(i == N-1) break;
            i++;
            if(inp == N-1){
                inp=0;
            }else{
                inp++;
            }
        }
        fput_float(data_out, out);
    }
}
""",

"Knight Rider":"""
/* Knight Rider Style LEDs */

int leds = output("leds");
void main()
{
    int shifter = 1;
    while(1){
        while(shifter < 0x80){
            shifter <<= 1;
            fputc(leds, shifter);
            wait_clocks(10000000); /*0.1 seconds @ 100MHz*/
        }
        while(shifter > 1){
            shifter >>= 1;
            fputc(leds, shifter);
            wait_clocks(10000000); /*0.1 seconds @ 100MHz*/
        }
    }
}
""",

"Seven Segment":"""
/* Seven Segment Display Driver */

int nibble = input("nibble");
int leds = output("leds");

int digits[] = {
    0x7E, 0x30, 0x6D, 0x79, 
    0x33, 0x5B, 0x5F, 0x70, 
    0x7F, 0x7B, 0x77, 0x1F, 
    0x4E, 0x3D, 0x4F, 0x47};

void main()
{
    while(1) fputc(leds, digits[fgetc(nibble)]);
}
""",

"LZSS Compress" : """
/*LZSS Compression Component*/
/*Jonathan P Dawson 2014-07.10*/

const int N = 1024;
const int LOG2N = 10;

unsigned raw_in = input("raw_in");
unsigned compressed_out = output("compressed_out");

/*Create a to send data of an arbitrary bit length*/
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

        }
    }
}
""",

"LZSS Decompress" : """
/*LZSS Decompression Component*/
/* Jonathan P Dawson 2014-07-10*/

const int N = 1024;
const int LOG2N = 10;

unsigned raw_out = output("raw_out");
unsigned compressed_in = input("compressed_in");

/* A function to get data of an arbitrary bit length data */

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


/* Decompress a stream of lzss compressed data, 
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
}"""

            

}

