#!/usr/bin/env python
"""Support Library for builtin Functionality"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

libs={"print.h":"""

//Print a string *string* to stdout
void print_string(unsigned string[]){
        unsigned i=0;
        while(string[i]){
                       stdout_put_char(string[i]);
                i++;
        }
}

//Print an unsigned int to stdout in hex format
void print_uhex(unsigned uhex){
        unsigned digit_3 = (uhex >> 12) & 0xf;
        unsigned digit_2 = (uhex >> 8) & 0xf;
        unsigned digit_1 = (uhex >> 4) & 0xf;
        unsigned digit_0 = uhex & 0xf;
        if(digit_3 < 9) stdout_put_char(digit_3 | 0x30);
        else stdout_put_char(digit_3 + 87);
        if(digit_2 < 9) stdout_put_char(digit_2 | 0x30);
        else stdout_put_char(digit_2 + 87);
        if(digit_1 < 9) stdout_put_char(digit_1 | 0x30);
        else stdout_put_char(digit_1 + 87);
        if(digit_0 < 9) stdout_put_char(digit_0 | 0x30);
        else stdout_put_char(digit_0 + 87);
}

//Print an unsigned int to stdout in decimal format
//leading 0s will be suppressed
void print_udecimal(unsigned udecimal){
        unsigned digit;
        unsigned significant = 0;
        digit = 0;
        while(udecimal >= 10000){
                udecimal -= 10000;
                digit += 1;
        }
        if(digit | significant){
              stdout_put_char(digit | 0x30);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 1000){
                udecimal -= 1000;
                digit += 1;
        }
        if(digit | significant){
              stdout_put_char(digit | 0x30);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 100){
                udecimal -= 100;
                digit += 1;
        }
        if(digit | significant){
              stdout_put_char(digit | 0x30);
              significant = 1;
        }
        digit = 0;
        while(udecimal >= 10){
                udecimal -= 10;
                digit += 1;
        }
        if(digit | significant){
              stdout_put_char(digit | 0x30);
              significant = 1;
        }
        stdout_put_char(udecimal | 0x30);
}

//Print a signed int to stdout in hex format
void print_hex(int hex){
        if(hex >= 0){
                print_uhex(hex);
        } else {
                stdout_put_char('-');
                print_uhex(-hex);
        }
}

//Print a signed int to stdout in decimal format
//leading 0s will be suppressed
void print_decimal(int decimal){
        if(decimal >= 0){
                print_udecimal(decimal);
        } else {
                stdout_put_char('-');
                print_udecimal(-decimal);
        }
}

void print_float(float f){
    unsigned digit;
    unsigned print = 0;
    float significance = 100000000.0;

    if( f < 0) {
        stdout_put_char('-');
        f = -f;
    }

    while(significance >= 1.0){
        digit = f / significance; 
        print |= digit;
        if(print){
            stdout_put_char(digit + '0');
        }
        f = f - (digit * significance);
        significance /= 10.0;
    }

    stdout_put_char('.');

    while(significance > 0.00000001){
        digit = f / significance; 
        stdout_put_char(digit + '0');
        f = f - (digit * significance);
        significance /= 10.0;
        if(f == 0.0) break;
    }
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

}""",

"math.h" : """

    /* This is a very incomplete version of libc math.h 
     * Not all the funtions and Macros are implemented.
     * It has not been tested.
     * Special cases have not been catered for*/


    /* globals */
    const float M_LOG2E = 1.44269504089;
    const float M_LOG10E = 0.4342944819;
    const float M_LN2 = 0.69314718056;
    const float M_LN10 = 2.30258509299;
    const float M_PI = 3.14159265359;
    const float M_PI_2 = 1.57079632679;
    const float M_PI_4 = 0.78539816339;
    const float M_1_PI = 0.31830988618;
    const float M_2_PI = 0.63661977236;
    const float M_2_SQRTPI = 1.1283791671;
    const float M_SQRT2 = 1.41421356237;

    /*Taylor series approximation of Cosine function*/

    float _taylor(float angle){

        float old, approximation, sign, power, fact;
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

    float cos(float angle){
        return _taylor(angle);
    }

    /*return sin of angle in radians*/

    float sin(float angle){
        return cos(angle-(M_PI/2));
    }

    /*return tan of angle in radians*/

    float tan(float n){
        return sin(n) / cos(n);
    }

    /* return e ** x */

    float exp(float x){

        float result = 1.0;
        unsigned n = 1;
        float power = 1.0;
        float factorial = 1.0;
        float old = 0.0;

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

    float sinh(float x){
        return (exp(x)-exp(-x))/2.0;
    }

    /*return cosh of x in radians*/

    float cosh(float x){
        return (exp(x)+exp(-x))/2.0;
    }

    /*return tanh of x in radians*/

    float tanh(float x){
        return sinh(x)/cosh(x);
    }

    /*return asinh of x in radians*/

    float asinh(float x){
        return log(x-sqrt((x * x) + 1.0));
    }

    /*return acosh of x in radians*/

    float acosh(float x){
        return log(x-sqrt((x * x) - 1.0));
    }

    /*return atanh of x in radians*/

    float atanh(float x){
        return 0.5 * log((1.0+x)/(1.0-x));
    }

    /* Return absolute value of a float n*/

    float fabs(float n){
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

    float log(float n){
        float antilog, x, old;
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

    float log10(float n){
        return log(n)/log(10);
    }

    /* return log_2(n) */

    float log2(float n){
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
