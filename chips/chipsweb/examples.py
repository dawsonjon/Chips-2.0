examples = {
"Fast Fourier Transform" : """
/* fft.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

#include <math.h>
#include <stdio.h>

/*globals*/
const int n = 1024;
const int m = 10;
double twiddle_step_real[m];
double twiddle_step_imaginary[m];


/*calculate twiddle factors and store them*/
void calculate_twiddles(){
    unsigned stage, span;
    for(stage=0; stage<m; stage++){
        span = 1 << stage;
        twiddle_step_real[stage] = cos(M_PI/span);
        twiddle_step_imaginary[stage] = -sin(M_PI/span);
    }
}

/*bit reverse*/
unsigned bit_reverse(unsigned forward){
    unsigned reversed=0;
    unsigned i;
    for(i=0; i<m; i++){
        reversed <<= 1;
        reversed |= forward & 1;
        forward >>= 1;
    }
    return reversed;
}

/*calculate fft*/
void fft(double reals[], double imaginaries[]){

    int stage, subdft_size, span, i, ip, j;
    double sr, si, temp_real, temp_imaginary, imaginary_twiddle, real_twiddle;


    //read data into array
    for(i=0; i<n; i++){
        ip = bit_reverse(i);
        if(i < ip){
            temp_real = reals[i];
            temp_imaginary = imaginaries[i];
            reals[i] = reals[ip];
            imaginaries[i] = imaginaries[ip];
            reals[ip] = temp_real;
            imaginaries[ip] = temp_imaginary;
        }
    }

    //butterfly multiplies
    for(stage=0; stage<m; stage++){
        subdft_size = 2 << stage;
        span = subdft_size >> 1;

        //initialize trigonometric recurrence

        real_twiddle=1.0;
        imaginary_twiddle=0.0;

        sr = twiddle_step_real[stage];
        si = twiddle_step_imaginary[stage];

        report(stage);

        for(j=0; j<span; j++){
            for(i=j; i<n; i+=subdft_size){
                ip=i+span;

                temp_real      = reals[ip]*real_twiddle      - imaginaries[ip]*imaginary_twiddle;
                temp_imaginary = reals[ip]*imaginary_twiddle + imaginaries[ip]*real_twiddle;

                reals[ip]       = reals[i]-temp_real;
                imaginaries[ip] = imaginaries[i]-temp_imaginary;

                reals[i]       = reals[i]+temp_real;
                imaginaries[i] = imaginaries[i]+temp_imaginary;

            }
            //trigonometric recurrence
            temp_real=real_twiddle;
            real_twiddle      = temp_real*sr - imaginary_twiddle*si;
            imaginary_twiddle = temp_real*si + imaginary_twiddle*sr;
        }

    }

}

const int x_re_in = input("x_re");
const int x_im_in = input("x_im");
const int fft_x_re_out = output("fft_x_re");
const int fft_x_im_out = output("fft_x_im");

void main(){
    unsigned i;
    double reals[n];
    double imaginaries[n];

    /* pre-calculate sine and cosine*/
    calculate_twiddles();

    while(1){
        /* read time domain signal */
        for(i=0; i<n; i++){
            reals[i] = fget_double(x_re_in);
            imaginaries[i] = fget_double(x_im_in);
        }

        /* transform into frequency domain */
        fft(reals, imaginaries);

        /* output frequency domain signal*/
        for(i=0; i<n; i++){
            fput_double(reals[i], fft_x_re_out);
            fput_double(imaginaries[i], fft_x_im_out);
        }
    }
}
""",

"Taylor Series" : """
/* taylor.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

/* Note that the math.h implementations of trig functions are synthesisable and
 * more efficient than those shown here. */

#include <stdio.h>

/* globals */
double pi=3.14159265359;

/* approximate the cosine function using Taylor series */

double taylor(double angle){

    double old, approximation, sign, power, fact;
    unsigned count, i;

    approximation = angle;
    old = 0.0;
    sign = -1.0;
    count = 1;
    power = 1.0;
    fact = 1.0;

    for(i=3; approximation!=old; i+=2){
        old = approximation;

        while(count<=i){
            power*=angle;
            fact*=count;
            count++;
        }

        approximation += sign*(power/fact);
        sign = -sign;

    }
    return approximation;
}


/* return the sine of angle in radians */

double sin(double angle){

    return taylor(angle);

}

/* return the cosine of angle in radians */

double cos(double angle){
    
    return sin(angle+(pi/2));

}


/* test routine */
const int x_in = input("x");
const int sin_x_out = output("sin_x");
const int cos_x_out = output("cos_x");

void main(){
    double x;

    while(1){
        x = fget_double(x_in);
        fput_double(sin(x), sin_x_out);
        fput_double(cos(x), cos_x_out);
    }

}
""",

"Square Root" : """
/* sqrt.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

#include <stdio.h>

/* approximate sqrt using newton's method*/
double sqrt(double n){
    double square, x, old;
    x = n;
    old = 0.0;
    while(old != x){
        old = x;
        x = (x + n/x)*0.5;
    }
    return x;
}

/* test sqrt function*/
const int x_in = input("x");
const int sqrt_x_out = output("sqrt_x");
void main(){
    double x;
    while(1){
        x = fget_float(x_in);
        fput_float(sqrt(x), sqrt_x_out);
    }
}""",

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

void main(){
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
            fputc(shifter, leds);
            wait_clocks(10000000); /*0.1 seconds @ 100MHz*/
        }
        while(shifter > 1){
            shifter >>= 1;
            fputc(shifter, leds);
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
    while(1) fputc(digits[fgetc(nibble)], leds);
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

void main(){

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

void main(){
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

