/* sqrt.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

#include <stdio.h>

/* approximate sqrt using newton's method*/
double sqrt(double n){
    double square, x, old;
    x = n;
    old = 0.0;
    while(old != x){
        old = x;
        x = (x + n/x)*0.5;
    }
    return x;
}

/* test sqrt function*/
const int x_in = input("x");
const int sqrt_x_out = output("sqrt_x");
void main(){
    double x;
    while(1){
        x = fget_float(x_in);
        fput_float(sqrt(x), sqrt_x_out);
    }
}
