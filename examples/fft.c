#include "math.h"

unsigned bit_reverse(unsigned forward, unsigned bits){
    unsigned reversed = 0;
    unsigned i;
    for(i=0; i<bits; i++){
        reversed <<= 1;
        if (forward & 1) reversed |= 1;	
        forward >>= 1;
    }
    return reversed;
}

unsigned stages(unsigned n){
    unsigned guess = 0;
    while((1 << guess) < n){
	    guess++;
    }
    return guess;
}

void main(){
    int n = 1024;
    int m = stages(n);
    int stage, subdft_size, span, i, ip, j;
    float imaginaries[1024];
    float reals[1024];
    float twiddle_step_real[10];
    float twiddle_step_imaginary[10];
    float sr, si, temp_real, temp_imaginary, imaginary_twiddle, real_twiddle;



    for(stage=1; i<=m; stage++){
	subdft_size = 1 << i;
	span = subdft_size >> 1;
	twiddle_step_real[stage] = cos(pi/span);
	twiddle_step_imaginary[stage] = -sin(pi/span);
    }

    while(1){

	//read data into array
	for(i=0; i<n; i++){
	    reals[bit_reverse(i, m)] = input_time();
	    imaginaries[bit_reverse(i, m)] = input_time();
	}

	//butterfly multiplies
	for(stage=1; stage<=m; stage++){
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

	//write out data from array
	for(i=0; i<n; i++){
	    output_frequency(reals[i]);
	    output_frequency(imaginaries[i]);
	}
    }
}
