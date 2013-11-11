#!/usr/bin/env python
"""Support Library for builtin Functionality"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2013, Jonathan P Dawson"
__version__ = "0.1"

builtins="""

unsigned unsigned_divide_xxxx(unsigned dividend, unsigned divisor){
    unsigned denom = divisor;
    unsigned bit = 1;
    unsigned quotient = 0;
    if( denom > dividend ) return 0;
    if( denom == dividend ) return 1;
    while(denom <= dividend){
        denom <<= 1;
        bit <<= 1;
    }
    denom >>= 1;
    bit >>= 1;
    while(bit){
        if(dividend >= denom){
            dividend -= denom;
            quotient |= bit;
        }
        bit >>= 1;
        denom >>= 1;
    }
    return quotient;
}

int divide_xxxx(int dividend, int divisor){
    unsigned udividend, udivisor, uquotient;
    unsigned dividend_sign, divisor_sign, quotient_sign;
    dividend_sign = dividend & 0x8000u;
    divisor_sign = divisor & 0x8000u;
    quotient_sign = dividend_sign ^ divisor_sign;
    udividend = dividend_sign ? -dividend : dividend;
    udivisor = divisor_sign ? -divisor : divisor;
    uquotient = unsigned_divide_xxxx(udividend, udivisor);
    return quotient_sign ? -uquotient : uquotient;
}

long unsigned long_unsigned_divide_xxxx(long unsigned dividend, long unsigned divisor){
    long unsigned denom = divisor;
    long unsigned bit = 1;
    long unsigned quotient = 0;
    if( denom > dividend ) return 0;
    if( denom == dividend ) return 1;
    while(denom <= dividend){
        denom <<= 1;
        bit <<= 1;
    }
    denom >>= 1;
    bit >>= 1;
    while(bit){
        if(dividend >= denom){
            dividend -= denom;
            quotient |= bit;
        }
        bit >>= 1;
        denom >>= 1;
    }
    return quotient;
}

long int long_divide_xxxx(long int dividend, long int divisor){
    long unsigned udividend, udivisor, uquotient;
    long unsigned dividend_sign, divisor_sign, quotient_sign;
    dividend_sign = dividend & 0x80000000ul;
    divisor_sign = divisor & 0x80000000ul;
    quotient_sign = dividend_sign ^ divisor_sign;
    udividend = dividend_sign ? -dividend : dividend;
    udivisor = divisor_sign ? -divisor : divisor;
    uquotient = long_unsigned_divide_xxxx(udividend, udivisor);
    return quotient_sign ? -uquotient : uquotient;
}

"""
