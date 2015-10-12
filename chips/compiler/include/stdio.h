#ifndef __STDIO_H
#define __STDIO_H

unsigned stdin = 0;
unsigned stdout = 0;

///stdio.h
///-------
///
///In contrast to the C standard, `fputc` and `fgetc` are built-in functions, you
///do not need to include `stdio.h` to use them.
///
///The globals `stdin` and `stdout` should be set to an input or output by the user.
///


///The `fputs` function prints `string` to the output `handle`.
///
///.. code-block:: c
///
///        void fputs(unsigned string[], unsigned handle);
///
void fputs(unsigned string[], unsigned handle){
        unsigned i=0;
        while(string[i]){
                fputc(string[i], handle);
                i++;
        }
}

///The `fgets` function reads a line, up to `maxlength` characters, or a line end
///from the input `handle`. The string will be null terminated. `maxlength`
///includes the null character.
///
///.. code-block:: c
///
///        void fgets(unsigned string[], unsigned maxlength, unsigned handle);
///

void fgets(unsigned string[], unsigned maxlength, unsigned handle){
        unsigned c;
        unsigned i=0;
        while(1){
                c = fgetc(handle);
                string[i] = c;
                i++;
                if(c == '\n') break;
                if(i == maxlength-1) break;
        }
        string[i] = 0;
}

///The `puts` function prints `string` to stdout.
///
///.. code-block:: c
///
///        void puts(unsigned string[]);
///

void gets(unsigned string[], unsigned maxlength){
        fgets(string, maxlength, stdin);
}

///The `gets` function reads a line, up to `maxlength` characters, or a line end
///from stdin. The string will be null terminated. `maxlength`
///includes the null character.
///
///.. code-block:: c
///
///        void gets(unsigned string[], unsigned maxlength);
///

void puts(unsigned string[]){
        fputs(string, stdout);
}

///The `getc` returns a single character from stdin.
///
///.. code-block:: c
///
///        unsigned long getc();
///

unsigned getc(){
        return fgetc(stdout);
}

///The `putc` writes a single character to stdout.
///
///.. code-block:: c
///
///        void putc(unsigned c);
///

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
    unsigned low, high;
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

void fput_int(int d, unsigned handle){
    fputc(d, handle);
}

int fget_int(unsigned handle){
    return fgetc(handle);
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

#endif

