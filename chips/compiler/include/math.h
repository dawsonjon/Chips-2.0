/*
 * Jonathan P Dawson
 * Copyright (C) 2013-2015, Jonathan P Dawson"
 *
 * math.h
 */


#ifndef __math_h_
#define __math_h_

#include <errno.h>

/* globals */
const double M_E        = 2.7182818284590451;
const double M_LOG2E    = 1.4426950408889634;
const double M_LOG10E   = 0.43429448190325182;
const double M_LN2      = 0.69314718055994529;
const double M_LN10     = 2.3025850929940459;
const double M_PI       = 3.141592653589793;
const double M_PI_2     = 1.5707963267948966;
const double M_PI_4     = 0.7853981633974483;
const double M_1_PI     = 0.3183098861837907;
const double M_2_PI     = 0.6366197723675814;
const double M_TWICE_PI = 6.283185307179586;
const double M_2_SQRTPI = 0.56418958354775628;
const double M_SQRT2    = 1.4142135623730951;

const double HUGE_VAL   = bits_to_double(0x7ff0000000000000ul);
const double INFINITY   = bits_to_double(0x7ff0000000000000ul);
const double NAN        = bits_to_double(0x7ff8000000000000ul);

double log(double n);

///math.h
///------
///
///
///The isfinite macro
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///        #include <math.h>
///        int isfinite(real-floating x);
///
///Description:
///
///    The isfinite macro determines whether its argument has a finite value (zero,
///    subnormal, or normal, and not infinite or NaN). First, an argument represented in a
///    format wider than its semantic type is converted to its semantic type. Then determination
///    is based on the type of the argument.
///    Since an expression can be evaluated with more range and precision than its type has, it is important to
///    know the type that classification is based on. For example, a normal long double value might
///    become subnormal when converted to double, and zero when converted to float.
///
///Returns:
///
///The isfinite macro returns a nonzero value if and only if its argument has a finite
///value.
///

int isfinite(double x){
    unsigned long exponent = (double_to_bits(x) >> 52) & 0x7ff;
    unsigned long mantissa = double_to_bits(x) & 0xffffffffffffful;
    return exponent < 2047; //nan and inf have 2047
}


///The isinf macro
///***************
///
///Synopsis:
///
///.. code-block:: c
///
///    #include <math.h>
///    int isinf(real-floating x);
///
///Description:
///
///    The isinf macro determines whether its argument value is an infinity (positive or
///    negative). First, an argument represented in a format wider than its semantic type is
///    converted to its semantic type. Then determination is based on the type of the argument.
///
///Returns:
///
///    The isinf macro returns a nonzero value if and only if its argument has an infinite
///    value.
///
///

int isinf(double x){
    unsigned long exponent = (double_to_bits(x) >> 52) & 0x7ff;
    unsigned long mantissa = double_to_bits(x) & 0xffffffffffffful;
    return exponent == 2047 &&  mantissa == 0;
}

///The isnan macro
///***************
///
///Synopsis:
///
///.. code-block:: c
///
///        #include <math.h>
///        int isnan(real-floating x);
///
///Description:
///
///    The isnan macro determines whether its argument value is a NaN. First, an argument
///    represented in a format wider than its semantic type is converted to its semantic type.
///    Then determination is based on the type of the argument.
///
///Returns:
///
///    The isnan macro returns a nonzero value if and only if its argument has a NaN value.
///
///

int isnan(double x){
    unsigned long exponent = (double_to_bits(x) >> 52) & 0x7ff;
    unsigned long mantissa = double_to_bits(x) & 0xffffffffffffful;
    return exponent == 2047 &&  mantissa != 0;
}

///The isnormal macro
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///        #include <math.h>
///        int isnormal(real-floating x);
///
///    For the isnan macro, the type for determination does not matter unless the implementation supports
///    NaNs in the evaluation type but not in the semantic type.
///
///Description:
///
///    The isnormal macro determines whether its argument value is normal (neither
///    zero, subnormal, infinite, nor NaN). First, an argument
///    represented in a format wider than its semantic type is converted to its
///    semantic type. Then determination is based on the type of the argument.
///
///Returns:
///
///    The isnormal macro returns a nonzero value if and only if its argument has a
///    normal value.
///
///


int isnormal(double x){
    unsigned long exponent = (double_to_bits(x) >> 52) & 0x7ff;
    return exponent > 0 && exponent < 2047;
}

///The signbit macro (not in C89)
///******************************
///
///Synopsis:
///
///.. code-block:: c
///
///    #include <math.h>
///    int signbit(real-floating x);
///
///Description:
///
///    The signbit macro determines whether the sign of its argument value is negative.
///
///Returns:
///
///    The signbit macro returns a nonzero value if and only if the sign of its argument value
///    is negative.
///

int signbit(double x){
   return double_to_bits(x) >> 63;
}


///The fabs function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double fabs(double x);
///
///Description:
///
///   The fabs function computes the absolute value of a floating-point
///   number x.
///
///Returns:
///
///   The fabs function returns the absolute value of x.  
///
///

double fabs(double n){
    return bits_to_double(double_to_bits(n) & 0x7ffffffffffffffful);
}


///The modf function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double modf(double value, double *iptr);
///
///Description:
///
///   The modf function breaks the argument value into integral and
///   fractional parts, each of which has the same sign as the argument.  It
///   stores the integral part as a double in the object pointed to by iptr.
///
///Returns:
///
///   The modf function returns the signed fractional part of value.  
///
///

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
    if(isnan(x)){
        *int_part = NAN;
        return NAN;
    } else if (isinf(x)) {
	if(signbit(x)){
            *int_part = -INFINITY;
            return -0.0;
	} else {
            *int_part = INFINITY;
            return 0.0;
	}
    } else {
        ip = _truncate(x);
        *int_part = ip;
        return x - ip;
    }
}


///The fmod function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double fmod(double x, double y);
///
///Description:
///
///   The fmod function computes the floating-point remainder of x/y.  
///
///Returns:
///
///   The fmod function returns the value x i y , for some integer i such
///   that, if y is nonzero, the result has the same sign as x and magnitude
///   less than the magnitude of y.  If y is zero, whether a domain error
///   occurs or the fmod function returns zero is implementation-defined.
///
///

double fmod(double x, double y)
{
    if(isnan(x) || isnan(y)){
         errno = EDOM;
	 return NAN;
    }
    if(y==0.0 || y==-0.0){
         errno = EDOM;
	 return NAN;
    }
    double n = _truncate(x/y);
    return x - (n * y);
}

///The exp function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double exp(double x);
///
///Description:
///
///   The exp function computes the exponential function of x.  A range
///   error occurs if the magnitude of x is too large.
///
///Returns:
///
///   The exp function returns the exponential value.  
///
///

double exp(double x){
    double f, i;

    /*underflow*/
    if(x < -708.3964185322641){errno=ERANGE; return 0.0;}

    /*overflow*/
    if(x > 709.782712893384){errno=ERANGE; return INFINITY;}

    /* Handle negative values */
    if(x < 0.0) return 1.0/exp(-x);

    /* 2^x can be calculated more quickly than e^x */
    /* e^x = 2^(1.4426950408889634*x) */

    f = modf(x * 1.4426950408889634, &i);

    /* n^x = n^fraction(x) * n^integer(x) */
    /* calculate the integer part by bit manipulation of exponent */
    return bits_to_double((((long)i + 1023) & 0x7ff) << 52) * 

    /* calculate fraction part using polynomial */
    (f *(f *(f *(f *(f *(f *(f *(f *(f *(f *1.00021469355055e-8 +
	 9.43619480925929e-8) +
	 1.33179289464105e-6) +
	 1.52440534441702e-5) +
	 0.000154040000640711) +
	 0.00133335418836421) +
	 0.00961812945787236) +
	 0.0555041086208906) +
	 0.240226506961923) +
	 0.693147180559875) +
	 1.0);

}

///The sqrt function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double sqrt(double x);
///
///Description:
///
///   The sqrt function computes the nonnegative square root of x.  A
///   domain error occurs if the argument is negative.
///
///Returns:
///
///   The sqrt function returns the value of the square root.  
///
///

double sqrt(double n){

    double square, x, old;
    long val_int = double_to_bits(n);
    if(n<0){errno=EDOM; return NAN;}
    /*approximate square root by manipulating bits*/
    val_int -= 1 << 52; /* Subtract 2^m. */
    val_int >>= 1; /* Divide by 2. */
    val_int += 1 << 61; /* Add ((b + 1) / 2) * 2^m. */
    /*refine approximation using newtons method*/
    x = bits_to_double(val_int);
    do{
        old = x;
        x = (x + n/x)*0.5;
    } while (old != x);
    return x;

}

///The pow function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double pow(double x, double y);
///
///Description:
///
///   The pow function computes x raised to the power y.  A domain error
///   occurs if x is negative and y is not an integer.  A domain error
///   occurs if the result cannot be represented when x is zero and y is
///   less than or equal to zero.  A range error may occur.
///
///Returns:
///
///   The pow function returns the value of x raised to the power y.  
///
///

double pow(double x, double y){
	return exp(log(x)*y);
}

///The ldexp function
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double ldexp(double x, int exp);
///
///Description:
///
///   The ldexp function multiplies a floating-point number by an
///   integral power of 2.  A range error may occur.
///
///Returns:
///
///   The ldexp function returns the value of x times 2 raised to the
///   power exp.
///
///

double ldexp(double x, int exp){

    unsigned long bits, exponent;

    //IEEE 754-1985 double precision float
    //
    //|63 60|59 56|55 52|51 48|47 44|43 40|39 36|35 32|31 28|27 24|23 20|19 16|15 12|11  8|7   4|3   0|
    //
    // ^ sign bit
    //  | 62 <-----> 52 | exponent
    //
    //  mantissa        | 51 <------------------------------------------------------------------> 0 |
      

    bits = double_to_bits(x * 2.0);
    bits &= 0x800FFFFFFFFFUL; /* clear exponent bits */

    exponent = exp + 1023;
    exponent &= 0x7f;
    exponent <<= 52;
    bits |= exponent;

    return bits_to_double(bits);

}

///The frexp function
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double frexp(double value, int *exp);
///
///Description:
///
///   The frexp function breaks a floating-point number into a normalized
///   fraction and an integral power of 2.  It stores the integer in the int
///   object pointed to by exp.
///
///Returns:
///
///   The frexp function returns the value x , such that x is a double
///   with magnitude in the interval [1/2, 1) or zero, and value equals x
///   times 2 raised to the power *exp.  If value is zero, both parts of
///   the result are zero.
///
///

double frexp(double value, int *exp){
    unsigned long bits, significand;

    //IEEE 754-1985 double precision float
    //
    //|63 60|59 56|55 52|51 48|47 44|43 40|39 36|35 32|31 28|27 24|23 20|19 16|15 12|11  8|7   4|3   0|
    //
    // ^ sign bit
    //  | 62 <-----> 52 | exponent
    //
    //  mantissa        | 51 <------------------------------------------------------------------> 0 |
      
    bits = double_to_bits(value);

    //get exponent part
    *exp  = bits >> 52;
    *exp &= 0x7ff;
    *exp -= 1023;

    //get significand part
    significand = bits;
    significand &= 0x800FFFFFFFFFFFFFUL; //clear exponent bits
    significand |= 0x7FF0000000000000UL; //set exponent to 0 (+1023 bias)
    return bits_to_double(significand)/2.0; //move from interval [1, 2) to [0.5, 1)

}

///The floor function
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double floor(double x);
///
///Description:
///
///   The floor function computes the largest integral value not greater
///than x.
///
///Returns:
///
///   The floor function returns the largest integral value not greater
///   than x , expressed as a double.
///
///

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

///The ceil function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double ceil(double x);
///
///Description:
///
///   The ceil function computes the smallest integral value not less than x.  
///
///Returns:
///
///   The ceil function returns the smallest integral value not less than
///   x , expressed as a double.
///
///

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

///The cos function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double cos(double x);
///
///Description:
///
///   The cos function computes the cosine of x (measured in radians).  A
///   large magnitude argument may yield a result with little or no
///   significance.
///
///Returns:
///
///   The cos function returns the cosine value.  
///
///

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

double cos(double x){
    int quadrant;
    x = fmod(x, M_TWICE_PI);
    if(x<0.0) x = -x;	
        quadrant = x/(M_PI_2);
    switch(quadrant){
        case 0: return _cos_kernel(x);
        case 1: return -_cos_kernel(M_PI - x);
        case 2: return -_cos_kernel(x - M_PI);
        case 3: return _cos_kernel(M_TWICE_PI - x);
    }
}

///The sin function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double sin(double x);
///
///Description:
///
///   The sin function computes the sine of x (measured in radians).  A
///   large magnitude argument may yield a result with little or no
///   significance.
///
///Returns:
///
///   The sin function returns the sine value.  
///
///

double sin(double angle){
    return cos(angle-(M_PI_2));
}

///The tan function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double tan(double x);
///
///Description:
///
///   The tan function returns the tangent of x (measured in radians).  A large magnitude argument may yield a result with little or no significance.  
///
///Returns:
///
///   The tan function returns the tangent value.  
///
///

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

double _tan_reduce(double x){
    const double four_over_pi = 4.0/M_PI;
    const double three_pi_over_two = (3.0*M_PI)/2;
    int octant;
    x = fmod(x, M_TWICE_PI);
    octant=x/M_PI_4;    
    switch(octant){
        case 0: return       _tan_kernel(x *              four_over_pi);
        case 1: return 1.0/  _tan_kernel((M_PI_2-x) *     four_over_pi);
        case 2: return -1.0/ _tan_kernel((x-M_PI_2) *     four_over_pi);
        case 3: return -     _tan_kernel((M_PI-x) *       four_over_pi);
        case 4: return       _tan_kernel((x-M_PI) *       four_over_pi);
        case 5: return 1.0/  _tan_kernel((three_pi_over_two-x) * four_over_pi);
        case 6: return -1.0/ _tan_kernel((x-three_pi_over_two) * four_over_pi);
        case 7: return -     _tan_kernel((M_TWICE_PI-x) *     four_over_pi);
    }
}

double tan(double x){
    if(x<0.0) return -_tan_reduce(-x);
    else return _tan_reduce(x);
}

 
///The atan function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double atan(double x);
///
///Description:
///
///   The atan function computes the principal value of the arc tangent of x.  
///
///Returns:
///
///   The atan function returns the arc tangent in the range [-PI/2, +PI/2]
///   radians.
///
///

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

///The atan2 function
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double atan2(double y, double x);
///
///Description:
///
///   The atan2 function computes the principal value of the arc tangent
///   of y/x , using the signs of both arguments to determine the quadrant
///   of the return value.  A domain error may occur if both arguments are
///   zero.
///
///Returns:
///
///   The atan2 function returns the arc tangent of y/x , in the range
///   [-PI, +PI] radians.
///
///

double atan2(double y, double x){
    if(x == 0.0){
        if(y > 0.0) return M_PI_2;
        else if(y < 0.0) return -M_PI_2;
	else return 0.0;
    }
    return atan(y/x);
}

///The asin function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double asin(double x);
///
///Description:
///
///   The asin function computes the principal value of the arc sine of x.
///   A domain error occurs for arguments not in the range [-1, +1].
///
///Returns:
///
///   The asin function returns the arc sine in the range [-PI/2, +PI/2]
///   radians.
///
///

double asin(double x){
    if(x > 1.0 || x < -1.0){ errno=EDOM; return NAN;}
    return atan(x/sqrt(1-(x*x)));
}

///The acos function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///  #include <math.h>
///  double acos(double x);
///
///Description:
///
///  The acos function computes the principal value of the arc cosine of x.
///  A domain error occurs for arguments not in the range [-1, +1].
///
///Returns:
///
///  The acos function returns the arc cosine in the range [0, PI] radians.  
///
///


double acos(double x){
    if(x > 1.0 || x < -1.0){ errno=EDOM; return NAN;}
    return M_PI_2 - asin(x);
}

///The sinh function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double sinh(double x);
///
///Description:
///
///   The sinh function computes the hyperbolic sine of x.  A range error occurs if the magnitude of x is too large.  
///
///Returns:
///
///   The sinh function returns the hyperbolic sine value.  
///
///

double sinh(double x){
    if(x > 710.4758600739439){errno=ERANGE; return INFINITY;}
    if(x < -710.4758600739439){errno=ERANGE; return -INFINITY;}
   return (exp(x)-exp(-x))/2.0;
}

///The cosh function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double cosh(double x);
///
///Description:
///
///   The cosh function computes the hyperbolic cosine of x.  A range
///   error occurs if the magnitude of x is too large.
///
///Returns:
///
///   The cosh function returns the hyperbolic cosine value.  
///
///

double cosh(double x){
    if(x > 710.4758600739439){errno=ERANGE; return INFINITY;}
    if(x < -710.4758600739439){errno=ERANGE; return INFINITY;}
    return (exp(x)+exp(-x))/2.0;
}

///The tanh function
///*****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double tanh(double x);
///
///Description:
///
///   The tanh function computes the hyperbolic tangent of x.  
///
///Returns:
///
///   The tanh function returns the hyperbolic tangent value.  
///
///

double tanh(double x){
    return sinh(x)/cosh(x);
}

/*return asinh of x in radians*/

double asinh(double x){
    return log(x-sqrt((x * x) + 1.0));
}

/*return acosh of x in radians*/

double acosh(double x){
    if(x < 1.0 ){ errno=EDOM; return NAN;}
    return log(x-sqrt((x * x) - 1.0));
}

/*return atanh of x in radians*/

double atanh(double x){
    if(x < -1.0 || x > 1.0){ errno=EDOM; return NAN;}
    if(x == 1.0 || x == -1.0){ errno=ERANGE; return INFINITY * x;}
    return 0.5 * log((1.0+x)/(1.0-x));
}

///The log function
///****************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double log(double x);
///
///Description:
///
///   The log function computes the natural logarithm of x.  A domain
///   error occurs if the argument is negative.  A range error occurs if the
///   argument is zero and the logarithm of zero cannot be represented.
///
///Returns:
///
///   The log function returns the natural logarithm.  
/// 
/// 

double log(double n){
 
    long exponent;
    double x, antilog, old;

    if(n==0.0){errno=ERANGE; return -INFINITY;}
    if(n<0.0){errno=EDOM; return NAN;}


    /* start by approximating log2(n) by using exponent */
    /* exponent == floor(log2(n)) */
    exponent = double_to_bits(n) >> 52;
    exponent &= 0x7ff;
    exponent -= 1023;

    x = exponent/1.4426950408889634;

    do {
       old = x;
       antilog = exp(x);
       x -= (antilog - n)/antilog;
    } while(fabs(old - x) > 0.000000000000001);

    /* convert base to log(n) == log2(n)/log2(e) */
    return x;
}

///The log10 function
///******************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double log10(double x);
///
///Description:
///
///   The log10 function computes the base-ten logarithm of x.  A domain
///   error occurs if the argument is negative.  A range error occurs if the
///   argument is zero and the logarithm of zero cannot be represented.
///
///Returns:
///
///   The log10 function returns the base-ten logarithm.  
///
///

double log10(double n){
    return log(n)/2.302585092994046;
}

///The log2 function (Not in C89 standard)
///***************************************
///
///Synopsis:
///
///.. code-block:: c
///
///         #include <math.h>
///         double log2(double x);
///
///Description:
///
///   The log2 function computes the base-two logarithm of x.  A domain
///   error occurs if the argument is negative.  A range error occurs if the
///   argument is zero and the logarithm of zero cannot be represented.
///
///Returns:
///
///   The log2 function returns the base-two logarithm.  
///
///

double log2(double n){
    return log(n)/0.6931471805599453;
}

#endif

