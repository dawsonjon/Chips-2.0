#include <math.h>

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
    //test_ceil();
    //test_floor();
    //test_trig();
    //test_inverse_tan();
    //test_inverse_trig();
    //test_htrig();
    //test_sqrt();
    //test_exp();
    test_log();

}
