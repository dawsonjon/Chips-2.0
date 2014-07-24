/* fft.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

#include "math.h"

/*globals*/
const int n = 1024;
const int m = 10;
double twiddle_step_real[m];
double twiddle_step_imaginary[m];


/*calculate twiddle factors and store them*/
void calculate_twiddles(){
    unsigned stage, span;
    for(stage=0; stage<m; stage++){
        span = 1 << stage;
        twiddle_step_real[stage] = cos(M_PI/span);
        twiddle_step_imaginary[stage] = -sin(M_PI/span);
    }
}

/*bit reverse*/
unsigned bit_reverse(unsigned forward){
    unsigned reversed=0;
    unsigned i;
    for(i=0; i<m; i++){
        reversed <<= 1;
        reversed |= forward & 1;
        forward >>= 1;
    }
    return reversed;
}

/*calculate fft*/
void fft(double reals[], double imaginaries[]){

    int stage, subdft_size, span, i, ip, j;
    double sr, si, temp_real, temp_imaginary, imaginary_twiddle, real_twiddle;


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
    for(stage=0; stage<m; stage++){
        subdft_size = 2 << stage;
        span = subdft_size >> 1;

        //initialize trigonometric recurrence

        real_twiddle=1.0;
        imaginary_twiddle=0.0;

        sr = twiddle_step_real[stage];
        si = twiddle_step_imaginary[stage];

        report(stage);
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
            //trigonometric recurrence
            temp_real=real_twiddle;
            real_twiddle      = temp_real*sr - imaginary_twiddle*si;
            imaginary_twiddle = temp_real*si + imaginary_twiddle*sr;
        }

    }

}

void main(){
    unsigned i;
    double reals[n];
    double imaginaries[n];

    /* pre-calculate sine and cosine*/
    calculate_twiddles();

    /* generate a 64 sample sin wave */
    for(i=0; i<n; i++){
        reals[i] = 0.0;
        imaginaries[i] = 0.0;
    }
    for(i=0; i<=64; i++){
       reals[i] = sin(2.0 * M_PI * (i/64.0));
    }

    /* output time domain signal to a file */
    for(i=0; i<n; i++){
        file_write(reals[i], "x_re");
        file_write(imaginaries[i], "x_im");
    }

    /* transform into frequency domain */
    fft(reals, imaginaries);

    /* output frequency domain signal to a file */
    for(i=0; i<n; i++){
        file_write(reals[i], "fft_x_re");
        file_write(imaginaries[i], "fft_x_im");
    }
}
