/*
 * Jonathan P Dawson
 * Copyright (C) 2013-2015, Jonathan P Dawson"
 *
 * math.h
/*


    /* globals */
    const double M_LOG2E = 1.44269504089;
    const double M_LOG10E = 0.4342944819;
    const double M_LN2 = 0.69314718056;
    const double M_LN10 = 2.30258509299;
    const double M_PI = 3.14159265359;
    const double M_PI_2 = M_PI/2.0;
    const double M_PI_4 = M_PI/4.0;
    const double M_1_PI = 0.31830988618;
    const double M_2_PI = M_PI * 2.0;
    const double M_2_SQRTPI = 1.1283791671;
    const double M_SQRT2 = 1.41421356237;

    /* return absolute value of an int */

    int abs(int x){
        if (x < 0) {
            return - x;
        } else {
            return x;
        }
    }

    /* return absolute value of a long*/

    long labs(long x){
        if (x < 0) {
            return - x;
        } else {
            return x;
        }
    }

    /* return absolute value of a double n*/

    double fabs(double n){
        if (n < 0.0) {
            return - n;
        } else {
            return n;
        }
    }

    //Missing - div
    //Missing - ldiv

    double _truncate(double x){
	    unsigned long bits, exponent;

	    if( x < 1.0 && x > -1.0)
		   return 0.0;

	    bits = double_to_bits(x);
            exponent = (bits >> 52) & 0x7ff;
            exponent -= 1023;

	    if (exponent < 52)
		    bits &= ~(0xffffffffffffful >> exponent);

	    return bits_to_double(bits);
    }

    double modf(double x, double *int_part){
	    double ip;
	    ip = _truncate(x);
	    *int_part = ip;
	    return x - ip;
    }


    /* Computes the floating-point remainder of the division operation x/y */

    double fmod(double x, double y)
    {
	double n = _truncate(x/y);
	return x - (n * y);
    }

    /* return e ** x */

    double exp(double x){

        double result = 1.0;
        unsigned n = 1;
        double power = 1.0;
        double factorial = 1.0;
        double old = 0.0;

        while(fabs(old - result) > 0.00001){
            old = result;
            power *= x;
            factorial *= n;
            result += (power/factorial);
            n++;
        }

        return result;

    }

    /* Computes the largest integer value not greater than x */

    double floor( double x)
    {
        double f, y;

        if (x > -1.0 && x < 1.0){
		if(x >= 0) {
			return 0.0;
		} else {
			return -1.0;
		}
	}

        y = modf (x, &f);

        if (y == 0.0)
          return (x);

	if(x >= 0) {
		return f;
	} else {
		return f-1.0;
	}
    }

    /*Computes the smallest integer value not less than arg. */

    double ceil(double x)
    {
        double f, y;

        y = modf (x, &f);

        if (y == 0.0)
	    return (x);
	else if (x > -1.0 && x < 1.0)
	    if(x > 0)
		    return 1.0;
	    else
		    return 0.0;
	else
	    if(x > 0)
		    return f + 1.0;
	    else
		    return f;
    }

    /* return log_e(n) */

    double log(double n){
        double antilog, x, old;
        x = 10.0;
        old = 0.0;
        while(fabs(old - x) > 0.00001){
            old = x;
            antilog = exp(x);
            x -= (antilog - n)/antilog;
        }
        return x;
    }

    /* approximate sqrt using newton's method*/

    double sqrt(double n){

        double square, x, old;
        long val_int = double_to_bits(n);
        val_int -= 1 << 52; /* Subtract 2^m. */
        val_int >>= 1; /* Divide by 2. */
        val_int += 1 << 61; /* Add ((b + 1) / 2) * 2^m. */
        x = bits_to_double(val_int);
        do{
            old = x;
            x = (x + n/x)*0.5;
        } while (old != x);
        return x;
    }


    /*Polynomial Approximations*/

    double _cos_kernel(double x){
        const double c1 = 0.99999999999925182;
        const double c2 =-0.49999999997024012;
        const double c3 = 0.041666666473384543;
        const double c4 =-0.001388888418000423;
        const double c5 = 0.0000248010406484558;
        const double c6 =-0.0000002752469638432;
        const double c7 = 0.0000000019907856854;
	double x2;
	x2=x*x;
	return (c1 + x2*(c2 + x2*(c3 + x2*(c4 + x2*(c5 + x2*(c6 + c7*x2))))));
    }

    double _tan_kernel(double x){
        const double c1 = -34287.4662577359568109624;
        const double c2 = 2566.7175462315050423295;
        const double c3 = -26.5366371951731325438;
        const double c4 = -43656.1579281292375769579;
        const double c5 = 12244.4839556747426927793;
        const double c6 = -336.611376245464339493;
	double x2;
	x2=x*x;
	return (x * (c1 + x2*(c2 + x2*c3))/(c4 +x2 * (c5 + x2*(c6 + x2))));
    }

    double _atan_kernel(double x){
        const double c1 = 48.70107004404898384;
        const double c2 = 49.5326263772254345;
        const double c3 = 9.40604244231624;
        const double c4 = 48.70107004404996166;
        const double c5 = 65.7663163908956299;
        const double c6 = 21.587934067020262;
	double x2;
	x2=x*x;
	return (x * (c1 + x2*(c2 + x2*c3))/(c4 +x2 * (c5 + x2*(c6 + x2))));
    }


    /*return cos of angle in radians*/

    double cos(double x){
	int quadrant;
	x = fmod(x, M_2_PI);
	if(x<0.0) x = -x;	
	quadrant = x/(M_PI_2);
	switch(quadrant){
	    case 0: return _cos_kernel(x);
	    case 1: return -_cos_kernel(M_PI - x);
	    case 2: return -_cos_kernel(x - M_PI);
	    case 3: return _cos_kernel(M_2_PI - x);
	}
    }

    /*return sin of angle in radians*/

    double sin(double angle){
        return cos(angle-(M_PI_2));
    }

    double _tan_reduce(double x){
	const double four_over_pi = 4.0/M_PI;
	const double three_pi_over_two = (3.0*M_PI)/2;
        int octant;
	x = fmod(x, M_2_PI);
        octant=x/M_PI_4;	
	switch(octant){
	    case 0: return       _tan_kernel(x *              four_over_pi);
	    case 1: return 1.0/  _tan_kernel((M_PI_2-x) *     four_over_pi);
	    case 2: return -1.0/ _tan_kernel((x-M_PI_2) *     four_over_pi);
	    case 3: return -     _tan_kernel((M_PI-x) *       four_over_pi);
	    case 4: return       _tan_kernel((x-M_PI) *       four_over_pi);
	    case 5: return 1.0/  _tan_kernel((three_pi_over_two-x) * four_over_pi);
	    case 6: return -1.0/ _tan_kernel((x-three_pi_over_two) * four_over_pi);
	    case 7: return -     _tan_kernel((M_2_PI-x) *     four_over_pi);
        }
    }

    /*return tan of angle in radians*/

    double tan(double x){
	    if(x<0.0) return -_tan_reduce(-x);
	    else return _tan_reduce(x);
    }
 
    /*return the inverse tan of x*/

    double atan(double x){
	    const double tan_pi_over_twelve = 0.2679491924311227;
	    const double tan_pi_over_six = 0.5773502691896257;
	    const double pi_over_six = 0.5235987755982988;
	    double y;
	    int complement=0;
	    int region=0;
	    int sign=0;

	    if (x<0.0){
		    x=-x;
		    sign=1;
	    }
	    if (x>1.0){
		    x=1.0/x;
		    complement=1;
	    }
	    if (x>tan_pi_over_twelve){
		    x=(x-tan_pi_over_six)/(1+tan_pi_over_six*x);
		    region=1;
	    }
	    y = _atan_kernel(x);
	    if(region) y+=pi_over_six;
	    if(complement) y=M_PI_2-y;
	    if(sign) y=-y;
	    return y;
    }

    double asin(double x){
	    return atan(x/sqrt(1-(x*x)));
    }

    double acos(double x){
	    return M_PI_2 - asin(x);
    }

    /*return sinh of x in radians*/

    double sinh(double x){
        return (exp(x)-exp(-x))/2.0;
    }

    /*return cosh of x in radians*/

    double cosh(double x){
        return (exp(x)+exp(-x))/2.0;
    }

    /*return tanh of x in radians*/

    double tanh(double x){
        return sinh(x)/cosh(x);
    }

    /*return asinh of x in radians*/

    double asinh(double x){
        return log(x-sqrt((x * x) + 1.0));
    }

    /*return acosh of x in radians*/

    double acosh(double x){
        return log(x-sqrt((x * x) - 1.0));
    }

    /*return atanh of x in radians*/

    double atanh(double x){
        return 0.5 * log((1.0+x)/(1.0-x));
    }


    /* return log_10(n) */

    double log10(double n){
        return log(n)/log(10);
    }

    /* return log_2(n) */

    double log2(double n){
        return log(n)/log(2);
    }
