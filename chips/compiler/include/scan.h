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

