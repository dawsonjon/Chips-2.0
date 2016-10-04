#include <stdio.h>

//Print an unsigned int to stdout in hex format
void fprint_uhex(unsigned uhex, unsigned handle){
        char digits[] = "0123456789abcdef";
        unsigned i, value;
        for(i=0; i<8; i++){
            value = uhex >> 28;
            uhex <<= 4;
            fputc(digits[value], handle);
        }
}

//Print an unsigned int to stdout in decimal format
//leading 0s will be suppressed
void fprint_udecimal(unsigned udecimal, unsigned handle){
        unsigned digit;
        unsigned significant = 0;
        digit = 0;
        while(udecimal >= 1000000000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 100000000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 10000000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 1000000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 100000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 10000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 1000){
                udecimal -= 1000;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 100){
                udecimal -= 100;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 10){
                udecimal -= 10;
                digit += 1;
        }
        if(digit | significant){
              fputc(digit | 0x30, handle);
              significant = 1;
        }
        fputc(udecimal | 0x30, handle);
}

//Print a signed int to stdout in hex format
void fprint_hex(int hex, unsigned handle){
        if(hex >= 0){
                fprint_uhex(hex, handle);
        } else {
                fputc('-', handle);
                fprint_uhex(-hex, handle);
        }
}

//Print a signed int to stdout in decimal format
//leading 0s will be suppressed
void fprint_decimal(int decimal, unsigned handle){
        if(decimal >= 0){
                fprint_udecimal(decimal, handle);
        } else {
                fputc('-', handle);
                fprint_udecimal(-decimal, handle);
        }
}

void fprint_float(float f, handle){
    unsigned digit;
    unsigned print = 0;
    float significance = 100000000.0f;

    if( f < 0.0f) {
        fputc('-', handle);
        f = -f;
    }

    while(significance >= 1.0f){
        digit = f / significance; 
        if(significance < 10.0f){
            print = 1;
        } else {
            print |= digit;
        }
        if(print){
            fputc(digit + '0', handle);
        }
        f = f - (digit * significance);
        significance /= 10.0f;
    }

    fputc('.', handle);

    while(significance > 0.00000001f){
        digit = f / significance; 
        fputc(digit + '0', handle);
        f = f - (digit * significance);
        significance /= 10.0f;
        if(f == 0.0f) break;
    }
}

void fprint_double(double f, handle){
    unsigned digit;
    unsigned print = 0;
    double significance = 100000000000000.0;

    if( f < 0) {
        fputc('-', handle);
        f = -f;
    }

    while(significance >= 1.0){
        digit = f / significance; 
        if(significance < 10.0){
            print = 1;
        } else {
            print |= digit;
        }
        if(print){
            fputc(digit + '0', handle);
        }
        f = f - (digit * significance);
        significance /= 10.0;
    }

    fputc('.', handle);

    while(significance > 0.0000000001){
        digit = f / significance; 
        fputc(digit + '0', handle);
        f = f - (digit * significance);
        significance /= 10.0;
        if(f == 0.0) break;
    }
}

void print_uhex(int hex){
    fprint_uhex(hex, stdout);
}

void print_udecimal(int decimal){
    fprint_udecimal(decimal, stdout);
}

void print_hex(int hex){
    fprint_hex(hex, stdout);
}

void print_decimal(int decimal){
    fprint_decimal(decimal, stdout);
}

void print_float(float f){
    fprint_float(f, stdout);
}

void print_double(double f){
    fprint_double(f, stdout);
}
