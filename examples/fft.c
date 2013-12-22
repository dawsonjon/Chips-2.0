#include "math.h"

/*globals*/
const int n = 1024;
const int m = 10;
float twiddle_step_real[m];
float twiddle_step_imaginary[m];


/*calculate twiddle factors and store them*/
void calculate_twiddles(){
    unsigned stage, subdft_size, span;
    for(stage=1; stage<=m; stage++){
        subdft_size = 1 << stage;
        span = subdft_size >> 1;
        twiddle_step_real[stage] = cos(pi/span);
        twiddle_step_imaginary[stage] = -sin(pi/span);
    }
}

/*bit reverse*/
unsigned bit_reverse(unsigned forward){
    unsigned reversed=0;
    unsigned i;
    for(i=0; i<m; i++){
        reversed <<= 1;
        reversed |= forward & 1;
        reversed >>= 1;
    }
    return reversed;
}

/*calculate fft*/
void fft(float reals[], float imaginaries[]){

    int stage, subdft_size, span, i, ip, j;
    float sr, si, temp_real, temp_imaginary, imaginary_twiddle, real_twiddle;

    //read data into array
    for(i=0; i<n; i++){
        ip = bit_reverse(i);
        if(i < ip){
            temp_real = reals[i];
            temp_imaginary = imaginaries[i];
            reals[i] = reals[ip];
            imaginaries[i] = imaginaries[ip];
            reals[ip] = temp_real;
            imaginaries[ip] = temp_imaginary;
        }
    }

    //butterfly multiplies
    for(stage=1; stage<=m; stage++){
        report(stage);
        subdft_size = 1 << stage;
        span = subdft_size >> 1;

        //initialize trigonometric recurrence

        real_twiddle=1.0;
        imaginary_twiddle=0.0;

        sr = twiddle_step_real[stage];
        si = twiddle_step_imaginary[stage];

        for(j=0; j<span; j++){
            for(i=j; i<n; i+=subdft_size){
                ip=i+span;

                temp_real      = reals[ip]*real_twiddle      - imaginaries[ip]*imaginary_twiddle;
                temp_imaginary = reals[ip]*imaginary_twiddle + imaginaries[ip]*real_twiddle;

                reals[ip]       = reals[i]-temp_real;
                imaginaries[ip] = imaginaries[i]-temp_imaginary;

                reals[i]       = reals[i]+temp_real;
                imaginaries[i] = imaginaries[i]+temp_imaginary;
            }
            //trigonometric recreal_twiddlerence
            temp_real=real_twiddle;
            real_twiddle      = temp_real*sr - imaginary_twiddle*si;
            imaginary_twiddle = temp_real*si + imaginary_twiddle*sr;
        }
    }
}

void main(){
    float reals[n];
    float imaginaries[n];
    unsigned i;
    for(i=0; i<n; i++){
        reals[i] = 0.0;
        imaginaries[i] = 0.0;
    }
    reals[0] = 1.0;
    calculate_twiddles();
    fft(reals, imaginaries);
    for(i=0; i<n; i++){
        file_write(reals[i], "fft_x_re");
        file_write(imaginaries[i], "fft_x_im");
    }
}
