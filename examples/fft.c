#define a fft component
################################################################################
def fft(input_stream, n):

    rex=VariableArray(n)
    imx=VariableArray(n)
    nm1=n-1
    nd2=n>>1
    m=int(log(n,2))

    #set up initial values for trig recurrence
    thetas = []
    for l in range(1, m+1):
        le=1<<l
        le2=le>>1
        thetas.append(pi/le2)

    sr_lut = Sequence(*[to_fixed(cos(i)) for i in thetas])
    si_lut = Sequence(*[to_fixed(-sin(i)) for i in thetas])

    i = Variable(0)
    ip = Variable(0)
    j = Variable(0)
    jm1 = Variable(0)
    l = Variable(0)
    k = Variable(0)
    le = Variable(0)
    le2 = Variable(0)
    tr = Variable(0)
    ti = Variable(0)
    xr = Variable(0)
    xi = Variable(0)
    ur = Variable(0)
    ui = Variable(0)
    sr = Variable(0)
    si = Variable(0)
    real = Output()
    imaginary = Output()

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

void main(){
    float[n] imaginaries;
    float[n] reals;

    while(1){

	//read data into array
	for(i=0; i<n; i++){
            i_reversed
	    reals[reversed(i, m)] = input_time();
	    imaginaries[reversed(i, m)] = input_time();
	}

	//butterfly multiplies
	for(stage=1; stage<=m; stage++){
	    subdft_size = 1 << stage;
	    span = subdft_size >> 1;

	    //initialize trigonometric recurrence

	    real_twiddle=1.0;
	    imaginary_twiddle=0.0;

	    sr = input_sr();
	    si = input_si();

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
		tr=real_twiddle;
		real_twiddle      = tr*sr - imaginary_twiddle*si;
		imaginary_twiddle = tr*si + imaginary_twiddle*sr;
	    }
	}

	//write out data from array
	for(i=0; i<n; i++){
	    output_frequency(reals[i]);
	    output_frequency(imaginaries[i]);
	}
    }
}
