
int as_int32(unsigned a){
    return *((int*)&a);
}

long long as_int64(long long unsigned a){
    return *((long long *)&a);
}

unsigned as_uint32(int a){
    return *((unsigned*)&a);
}

long long unsigned as_uint64(long long a){
    return *((long long unsigned*)&a);
}

typedef struct {unsigned hi, lo;} pair;

extern pair add(unsigned a, unsigned b, unsigned c){
    unsigned long long result;
    pair retval;
    result = (unsigned long long)a + b + c;
    retval.hi = (result >> 32);
    retval.hi &= 1;
    retval.lo = result & 0xffffffff;
    return retval;
}

extern pair subtract(unsigned a, unsigned b, unsigned c){
    unsigned long long result;
    pair retval;
    result = (unsigned long long)a + ~(unsigned long long)b + c;
    retval.hi = (result >> 32);
    retval.hi &= 1;
    retval.hi ^= 1;
    retval.lo = result & 0xffffffff;
    return retval;
}

#include <stdio.h>
extern pair shift_left(unsigned a, unsigned b, unsigned c){
    pair retval;

    if(!b){
        retval.lo = a;
        retval.hi = 0;
        return retval;
    }

    if (b > 32) b = 32;
    retval.hi = a >> (32 - b);
    if(b == 32){
        retval.lo = 0 | c;
    } else {
        retval.lo = (a << b) | c;
    }

    return retval;
}

extern pair shift_right(unsigned a, unsigned b){
    pair retval;
    if (!b){
        retval.hi = 0;
        retval.lo = a;
    } else if (b >= 32) {
        if(a & 0x80000000){
            retval.hi = a;
            retval.lo = 0xffffffffu;
        } else {
            retval.hi = a;
            retval.lo = 0;
        }
    } else {
        retval.hi = a << (32 - b);
        retval.lo = as_uint32(as_int32(a) >> b);
    }
    return retval;
}

extern pair unsigned_shift_right(unsigned a, unsigned b, unsigned c){
    pair retval;

    if (!b){
        retval.hi = 0;
        retval.lo = a;
    } else if (b >= 32) {
        retval.hi = a;
        retval.lo = c;
    } else {
        retval.hi = a << (32 - b);
        retval.lo = (a >> b) | c;
    }
    return retval;
}

extern unsigned greater(unsigned a, unsigned b){
    return as_int32(a) > as_int32(b);
}

extern unsigned greater_equal(unsigned a, unsigned b){
    return as_int32(a) >= as_int32(b);
}

extern unsigned unsigned_greater(unsigned a, unsigned b){
    return a > b;
}

extern unsigned unsigned_greater_equal(unsigned a, unsigned b){
    return a >= b;
}

extern unsigned unsigned_divide(unsigned a, unsigned b){
    if (!b) return a;
    return a/b;
}

extern unsigned divide(unsigned a, unsigned b){
    if (!b) return a;
    return as_uint32(as_int32(a)/as_int32(b));
}

extern unsigned unsigned_modulo(unsigned a, unsigned b){
    if (!b) return a;
    return a%b;
}

extern unsigned modulo(unsigned a, unsigned b){
    if (!b) return a;
    return as_uint32(as_int32(a)%as_int32(b));
}

extern long long unsigned unsigned_long_divide(long long unsigned a, long long unsigned b){
    if (!b) return a;
    return a/b;
}

extern long long unsigned long_divide(long long unsigned a, long long unsigned b){
    if (!b) return a;
    if (a==0x8000000000000000 && b==0xffffffffffffffff) return a;
    return as_uint64(as_int64(a)/as_int64(b));
}

extern long long unsigned unsigned_long_modulo(long long unsigned a, long long unsigned b){
    if (!b) return a;
    return a%b;
}

extern long long unsigned long_modulo(long long unsigned a, long long unsigned b){
    if (!b) return a;
    if (a==0x8000000000000000 && b==0xffffffffffffffff) return 0;
    return as_uint64(as_int64(a)%as_int64(b));
}

extern unsigned long long join_words(unsigned a, unsigned b){
    return ((unsigned long long) a << 32) | b;
}

extern unsigned high_word(unsigned long long a){
    return a >> 32;
}

extern unsigned low_word(unsigned long long a){
    return a & 0xffffffffl;
}

extern unsigned float_to_bits(float a){
    return *((unsigned*)&a);
}

extern float bits_to_float(unsigned a){
    return *((float*)&a);
}

extern unsigned long long double_to_bits(double a){
    return *((unsigned long long*)&a);
}

extern double bits_to_double(unsigned long long a){
    return *((double*)&a);
}
