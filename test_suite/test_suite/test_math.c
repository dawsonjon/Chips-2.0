#include <math.h>

void test_exceptions(){

    //acos(|x|>1)     EDOM        NaN
    errno = 0;
    assert(isnan(acos(1.1)));
    assert(errno == EDOM);
    errno = 0;
    assert(isnan(acos(-1.1)));
    assert(errno == EDOM);

    //acosh(x<1)      EDOM        NaN
    errno = 0;
    assert(isnan(acosh(0.9)));
    assert(errno == EDOM);
    
    //asin(|x|>1)     EDOM        NaN
    errno = 0;
    assert(isnan(asin(1.1)));
    assert(errno == EDOM);
    errno = 0;
    assert(isnan(asin(-1.1)));
    assert(errno == EDOM);

    //atan2
    assert(atan2(1.0, 0.0) == M_PI_2);
    assert(atan2(-1.0, 0.0) == -M_PI_2);
    assert(atan2(0.0, 0.0) == 0.0);

    //atanh(|x|>1)    EDOM        NaN
    errno = 0;
    assert(isnan(atanh(1.1)));
    assert(errno == EDOM);
    errno = 0;
    assert(isnan(atanh(-1.1)));
    assert(errno == EDOM);

    //atanh(+-1)      EDOM/ERANGE +-infinity
    errno = 0;
    assert(atanh(-1.0) == -INFINITY);
    assert(errno == ERANGE);
    errno = 0;
    assert(atanh(1.0) == INFINITY);
    assert(errno == ERANGE);

    //cosh overflow   ERANGE      infinity
    errno = 0;
    assert(cosh(-710.5) == INFINITY);
    assert(errno == ERANGE);
    errno = 0;
    assert(cosh(710.5) == INFINITY);
    assert(errno == ERANGE);
    //errno = 0;
    //report(acosh(1.7976931348623157e+308));
    //assert(cosh(-710.4758600739439) != INFINITY);
    //assert(errno == 0);
    //errno = 0;
    //assert(cosh(710.4758600739439) != INFINITY);
    //assert(errno == 0);

    //exp overflow    ERANGE      infinity
    errno = 0;
    assert(exp(710) == INFINITY);
    assert(errno == ERANGE);

    //exp underflow   ERANGE      0.0
    errno = 0;
    assert(exp(-800) == 0.0);
    assert(errno == ERANGE);
    

    //fmod(x,0)       EDOM        NaN
    errno = 0;
    assert(isnan(fmod(1.0, 0)));
    assert(errno == EDOM);

    //log(0)          EDOM/ERANGE -infinity
    errno = 0;
    assert(log(0.0) == -INFINITY);
    assert(errno == ERANGE);

    //log(x<0)        EDOM        NaN
    errno = 0;
    assert(isnan(log(-1.0)));
    //assert(errno == EDOM);

    //log10(0)        EDOM/ERANGE -infinity
    errno = 0;
    assert(log10(0.0) == -INFINITY);
    assert(errno == ERANGE);

    //log10(x<0)      EDOM        NaN
    errno = 0;
    assert(isnan(log10(-1.0)));
    assert(errno == EDOM);

    //log2(0)        EDOM/ERANGE -infinity
    errno = 0;
    assert(log2(0.0) == -INFINITY);
    assert(errno == ERANGE);

    //log2(x<0)      EDOM        NaN
    errno = 0;
    assert(isnan(log2(-1.0)));
    assert(errno == EDOM);

    //pow(0,0)        EDOM        1.0 (no error)
    //errno = 0;
    //assert(pow(0.0, 0.0));
    //assert(errno == 0);

    //pow(NaN,0)      EDOM        1.0 (no error)
    //errno = 0;
    //assert(pow(NAN, 0.0)==1.0);
    //assert(errno == 0);

    //pow(0,neg)      EDOM        +-infinity
    //errno = 0;
    //assert(pow(0, -1)==INFINITY);
    //assert(errno == 0);

    //pow(neg, 
    //non-integer)    EDOM        NaN
    //errno = 0;
    //assert(isnan(pow(-1, 0.5)));
    //assert(errno == EDOM);
    //errno = 0;
    //assert(isnan(pow(-1, 1.5)));
    //assert(errno == EDOM);

//pow overflow    ERANGE      +-infinity
//pow underflow   ERANGE      +-0.0

    //sinh overflow   ERANGE      +-infinity
    errno = 0;
    assert(sinh(-710.5) == -INFINITY);
    assert(errno == ERANGE);
    errno = 0;
    assert(sinh(710.5) == INFINITY);
    assert(errno == ERANGE);

    //sqrt(x<0)       EDOM        NaN
    errno = 0;
    assert(isnan(sqrt(-1.0)));
    assert(errno == EDOM);

}

void test_ceil(){
    //Test Ceil Function
    assert(ceil(1.5)==2.0);
    assert(ceil(-1.5)==-1.0);
    assert(ceil(1.000001)==2.0);
    assert(ceil(-1.000001)==-1.0);
    assert(ceil(1.0)==1.0);
    assert(ceil(-1.0)==-1.0);
    assert(ceil(10000.000001)==10001.0);
    assert(ceil(-10000.000001)==-10000.0);
}

void test_floor(){
    //Test Ceil Function
    assert(floor(1.5)==1.0);
    assert(floor(-1.5)==-2.0);
    assert(floor(1.000001)==1.0);
    assert(floor(-1.000001)==-2.0);
    assert(floor(1.0)==1.0);
    assert(floor(-1.0)==-1.0);
    assert(floor(10000.000001)==10000.0);
    assert(floor(-10000.000001)==-10001.0);
}

void test_trig(){
    double x, step;
    step = M_PI/100.0;
    for(x=-2*M_PI; x <= 2*M_PI; x += step){
       report(x);
       file_write(x, "x");
       file_write(cos(x), "cos_x");
       file_write(sin(x), "sin_x");
       file_write(tan(x), "tan_x");
    }
}
void test_inverse_tan(){
    double x, step;
    step = 1.0/100.0;
    for(x=-10.0; x <= 10.0; x += step){
       report(x);
       file_write(x, "x_2");
       file_write(atan(x), "atan_x");
    }
}
void test_inverse_trig(){
    double x, step;
    step = 1.0/100.0;
    for(x=-1.0; x <= 1.0; x += step){
       report(x);
       file_write(x, "x_3");
       file_write(asin(x), "asin_x");
       file_write(acos(x), "acos_x");
    }
}
void test_htrig(){
    double x, step;
    step = 1.0/10.0;
    for(x=-15.0; x <= 15.0; x += step){
       report(x);
       file_write(x, "x_4");
       file_write(cosh(x), "cosh_x");
       file_write(sinh(x), "sinh_x");
       file_write(tanh(x), "tanh_x");
    }
}
void test_sqrt(){
    double x, step;
    for(x=0.0; x <= 10.0; x += 0.01){
       report(x);
       file_write(x, "x_5");
       file_write(sqrt(x), "sqrt_x");
    }
}

void test_exp(){
    double x, step;
    for(x=-10.0; x <= 10.0; x += 0.1){
       file_write(x, "x_6");
       file_write(exp(x), "exp_x");
    }
}

void test_log(){
    double x, step;
    for(x=0.1; x <= 10.0; x += 0.1){
       report(x);
       file_write(x, "x_7");
       file_write(log(x), "log_x");
    }
}

void main(){

    //Test Ceil Function
    test_exceptions();
    test_ceil();
    test_floor();
    test_trig();
    test_inverse_tan();
    test_inverse_trig();
    test_htrig();
    test_sqrt();
    test_exp();
    test_log();

}
