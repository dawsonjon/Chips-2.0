int float_equal_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a == b;
}

int float_ne_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a != b;
}

int float_lt_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a < b;
}

int float_gt_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a > b;
}

int float_le_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a <= b;
}

int float_ge_xxxx(int a, int b){
    if (a < 0) {
        a = 0x80000000u - a;
    }
    if (b < 0) {
        b = 0x80000000u - b;
    }
    return  a >= b;
}

int long_float_equal_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a == b;
}

int long_float_ne_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a != b;
}

int long_float_lt_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a < b;
}

int long_float_gt_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a > b;
}

int long_float_le_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a <= b;
}

int long_float_ge_xxxx(long a, long b){
    if (a < 0) {
        a = 0x8000000000000000lu - a;
    }
    if (b < 0) {
        b = 0x8000000000000000lu - b;
    }
    return  a >= b;
}
