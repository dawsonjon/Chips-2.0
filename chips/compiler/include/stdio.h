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
    unsigned long l;
    unsigned low, high;
    l = double_to_bits(d);
    low = l & 0xffffffffu;
    high = l >> 32;
    fputc(low, handle);
    fputc(high, handle);
}

double fget_double(unsigned handle){
    int low, high;
    unsigned long l;
    double d;
    low = fgetc(handle);
    high = fgetc(handle);
    l = ((long) high) << 32;
    l |= low;
    d =  bits_to_double(l);
    return d;
}

void fput_float(float d, unsigned handle){
    fputc(float_to_bits(d), handle);
}

float fget_float(unsigned handle){
    return bits_to_float(fgetc(handle));
}

void fput_long(long d, unsigned handle){
    int low, high;
    long l = d;
    low = l & 0xffffffffu;
    high = l >> 32;
    fputc(low, handle);
    fputc(high, handle);
}

long fget_long(unsigned handle){
    int low, high;
    long l;
    low = fgetc(handle);
    high = fgetc(handle);
    l = ((long) high) << 32;
    l |= low;
    return l;
}

