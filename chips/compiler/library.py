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

}"""
}
