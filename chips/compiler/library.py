#!/usr/bin/env python
"""Support Library for builtin Functionality"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

libs={

"stdio.h" :


"""
unsigned stdin = 0;
unsigned stdout = 0;


void fputs(unsigned string[], unsigned handle){
        unsigned i=0;
        while(string[i]){
                fputc(string[i], handle);
                i++;
        }
}

void fgets(unsigned string[], unsigned maxlength, unsigned handle){
        unsigned c;
        unsigned i=0;
        while(1){
                c = fgetc(handle);
                string[i] = c;
                i++;
                if(c == '\\n') break;
                if(i == maxlength-1) break;
        }
        string[i] = 0;
}

void gets(unsigned string[], unsigned maxlength){
        fgets(string, maxlength, stdin);
}

void puts(unsigned string[]){
        fputs(string, stdout);
}

unsigned getc(){
        return fgetc(stdout);
}

void putc(unsigned c){
        fputc(c, stdout);
}

/*Non-Standard Extensions*/

void fput_double(double d, unsigned handle){
    long l;
    l = double_to_bits(d);
    /*send low word*/
    fputc(l & 0xffffffffu, handle);
    /*send high word*/
    fputc((l >> 32) & 0xffffffffu, handle);
}

double fget_double(unsigned handle){
    long low, high;
    double d;
    /*get low word*/
    low = fgetc(handle);
    report(low);
    /*get high word*/
    high = fgetc(handle);
    high <<= 32;
    high |= low;
    report(high);
    d =  bits_to_double(high);
    report(d);
    return d;
}

void fput_float(float d, unsigned handle){
    fputc(float_to_bits(d), handle);
}

float fget_float(unsigned handle){
    return bits_to_float(fgetc(handle));
}

""",


"print.h":"""

#include <stdio.h>

//Print an unsigned int to stdout in hex format
void fprint_uhex(unsigned uhex, unsigned handle){
        unsigned digit_3 = (uhex >> 12) & 0xf;
        unsigned digit_2 = (uhex >> 8) & 0xf;
        unsigned digit_1 = (uhex >> 4) & 0xf;
        unsigned digit_0 = uhex & 0xf;
        if(digit_3 < 9) fputc(digit_3 | 0x30, handle);
        else fputc(digit_3 + 87, handle);
        if(digit_2 < 9) fputc(digit_2 | 0x30, handle);
        else fputc(digit_2 + 87, handle);
        if(digit_1 < 9) fputc(digit_1 | 0x30, handle);
        else fputc(digit_1 + 87, handle);
        if(digit_0 < 9) fputc(digit_0 | 0x30, handle);
        else fputc(digit_0 + 87, handle);
}

//Print an unsigned int to stdout in decimal format
//leading 0s will be suppressed
void fprint_udecimal(unsigned udecimal, unsigned handle){
        unsigned digit;
        unsigned significant = 0;
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
    float significance = 100000000.0;

    if( f < 0) {
        fputc('-', handle);
        f = -f;
    }

    while(significance >= 1.0){
        digit = f / significance; 
        print |= digit;
        if(print){
            fputc(digit + '0', handle);
        }
        f = f - (digit * significance);
        significance /= 10.0;
    }

    fputc('.', handle);

    while(significance > 0.00000001){
        digit = f / significance; 
        fputc(digit + '0', handle);
        f = f - (digit * significance);
        significance /= 10.0;
        if(f == 0.0) break;
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
        print |= digit;
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

""",

"ctypes.h" : """
unsigned isalnum(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z') || (c >= '0' && c <= '9');
}

unsigned isalpha(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z');
}

unsigned islower(char c){
	return (c >='a' && c <= 'z');
}

unsigned isupper(char c){
	return (c >='A' && c <= 'Z');
}

unsigned isdigit(char c){
	return (c >='0' && c <= '9');
}

unsigned isxdigit(char c){
	return (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f') || (c >= '0' && c <= '9');
}

unsigned isgraph(char c){
	return (c >= 0x21  && c <= 0x7e);
}

unsigned isspace(char c){
	return (c == ' ' || c == '\\t' || c == '\\v' || c == '\\n' || c == '\\r' || c == '\\f');
}

unsigned isprint(char c){
	return (c >= 0x20  && c <= 0x7e);
}

unsigned ispunct(char c){
	return isgraph(c) && !isalnum(c);
}

unsigned toupper(char c){
	if(islower(c)){
	      return c - 'a' + 'A';	
	} else {
	      return c;
	}
}

unsigned tolower(char c){
	if(isupper(c)){
	      return c - 'A' + 'a';	
	} else {
	      return c;
	}
}""",

"scan.h":"""
unsigned scan_uhex(){
    unsigned value;
    value = 0;
    while(1){
        c = stdin_get_char();
        if(!isxdigit(c)) break;
        value <<= 4;
        value += _hex2nibble(c);
    }
    return sign * value;
}

unsigned scan_udecimal(){
    unsigned value;
    value = 0;
    while(1){
        c = stdin_get_char();
        if(!isdigit(c)) break;
        value *= 10;
        value += c - '0';
    }
    return value;
}

int scan_hex(){
    unsigned value;
    int sign;
    value = 0;
    if(c == '-'){
        sign = -1;
    } else if (c == '+'){
        sign = 1;
    } else {
        sign = 1;
        value = hextonibble(c);
    }
    while(1){
        c = stdin_getchar();
        if(!isxdigit(c)) break;
        value <<= 4;
        value += _hex2nibble(c);
    }
    return sign * value;
}

int scan_decimal(){
    unsigned value;
    int sign;
    value = 0;
    if(c == '-'){
        sign = -1;
    } else if (c == '+'){
        sign = 1;
    } else {
        sign = 1;
        value = c - 10;
    }
    while(1){
        c = stdin_get_char();
        if(!isdigit(c)) break;
        value *= 10;
        value += c - '0';
    }
    return sign * value;
}

float scan_float(){

    float value, significance, sign;

    value = 0;
    significance = 0.1

    /*evaluate sign*/
    if(c == '-'){
        sign = -1;
    } else if (c == '+'){
        sign = 1;
    } else {
        sign = 1;
        value = c - '0';
    }

    /*evaluate integer part*/
    while(1){
        c = stdin_get_char();
        if(!isdigit(c)) break;
        value *= 10;
        value += c - '0';
    }

    /*evaluate fractional part*/
    if(c == '.'){
        while(1){
            c = stdin_get_char();
            if(!isdigit(c)) break;
            value += significance * (c-'0');
            significance /= 10.0;
        }
    }

    return sign * value;

}

double scan_double(){

    double value, significance, sign;

    value = 0;
    significance = 0.1

    /*evaluate sign*/
    if(c == '-'){
        sign = -1;
    } else if (c == '+'){
        sign = 1;
    } else {
        sign = 1;
        value = c - '0';
    }

    /*evaluate integer part*/
    while(1){
        c = stdin_get_char();
        if(!isdigit(c)) break;
        value *= 10;
        value += c - '0';
    }

    /*evaluate fractional part*/
    if(c == '.'){
        while(1){
            c = stdin_get_char();
            if(!isdigit(c)) break;
            value += significance * (c-'0');
            significance /= 10.0;
        }
    }

    return sign * value;

}

""",

"math.h" : """

    /* This is a very incomplete version of libc math.h 
     * Not all the funtions and Macros are implemented.
     * It has not been tested.
     * Special cases have not been catered for*/


    /* globals */
    const double M_LOG2E = 1.44269504089;
    const double M_LOG10E = 0.4342944819;
    const double M_LN2 = 0.69314718056;
    const double M_LN10 = 2.30258509299;
    const double M_PI = 3.14159265359;
    const double M_PI_2 = 1.57079632679;
    const double M_PI_4 = 0.78539816339;
    const double M_1_PI = 0.31830988618;
    const double M_2_PI = 0.63661977236;
    const double M_2_SQRTPI = 1.1283791671;
    const double M_SQRT2 = 1.41421356237;

    /*Taylor series approximation of Cosine function*/

    double _taylor(double angle){

        double old, approximation, sign, power, fact;
        unsigned count, i;

        approximation = 1.0;
        old = 0.0;
        sign = -1.0;
        count = 1;
        power = 1.0;
        fact = 1.0;

        for(i=2; approximation!=old; i+=2){
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

    /*return cos of angle in radians*/

    double cos(double angle){
        return _taylor(angle);
    }

    /*return sin of angle in radians*/

    double sin(double angle){
        return cos(angle-(M_PI/2));
    }

    /*return tan of angle in radians*/

    double tan(double n){
        return sin(n) / cos(n);
    }

    /* return e ** x */

    double exp(double x){

        double result = 1.0;
        unsigned n = 1;
        double power = 1.0;
        double factorial = 1.0;
        double old = 0.0;

        while(fabs(old - result) > 0.00001){
            old = result;
            power *= x;
            factorial *= n;
            result += (power/factorial);
            n++;
        }

        return result;

    }

    /*return sinh of x in radians*/

    double sinh(double x){
        return (exp(x)-exp(-x))/2.0;
    }

    /*return cosh of x in radians*/

    double cosh(double x){
        return (exp(x)+exp(-x))/2.0;
    }

    /*return tanh of x in radians*/

    double tanh(double x){
        return sinh(x)/cosh(x);
    }

    /*return asinh of x in radians*/

    double asinh(double x){
        return log(x-sqrt((x * x) + 1.0));
    }

    /*return acosh of x in radians*/

    double acosh(double x){
        return log(x-sqrt((x * x) - 1.0));
    }

    /*return atanh of x in radians*/

    double atanh(double x){
        return 0.5 * log((1.0+x)/(1.0-x));
    }

    /* Return absolute value of a double n*/

    double fabs(double n){
        if (n < 0.0) {
            return - n;
        } else {
            return n;
        }
    }

    /* Return absolute value of integer n*/

    int abs(int n){
        if (n < 0) {
            return - n;
        } else {
            return n;
        }
    }


    /* return log_e(n) */

    double log(double n){
        double antilog, x, old;
        x = 10.0;
        old = 0.0;
        while(fabs(old - x) > 0.00001){
            old = x;
            antilog = exp(x);
            x -= (antilog - n)/antilog;
        }
        return x;
    }

    /* return log_10(n) */

    double log10(double n){
        return log(n)/log(10);
    }

    /* return log_2(n) */

    double log2(double n){
        return log(n)/log(2);
    }""",

"stdlib.h":"""

    const unsigned long RAND_MAX = 0xfffffffful;

    unsigned long int seed;

    void srand(unsigned long int s){
        seed = s;
    }

    unsigned long rand(){
        const unsigned long a = 1103515245ul;
        const unsigned long c = 12345ul;
        seed = (a*seed+c);
        return seed;
    }"""
}
