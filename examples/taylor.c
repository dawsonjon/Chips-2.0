/* taylor.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

#include <stdio.h>

/* globals */
double pi=3.14159265359;

/* approximate the cosine function using Taylor series */

double taylor(double angle){

    double old, approximation, sign, power, fact;
    unsigned count, i;

    approximation = angle;
    old = 0.0;
    sign = -1.0;
    count = 1;
    power = 1.0;
    fact = 1.0;

    for(i=3; approximation!=old; i+=2){
        old = approximation;

        while(count<=i){
            power*=angle;
            fact*=count;
            count++;
        }

        approximation += sign*(power/fact);
        sign = -sign;

    }
    return approximation;
}


/* return the sine of angle in radians */

double sin(double angle){

    return taylor(angle);

}

/* return the cosine of angle in radians */

double cos(double angle){
    
    return sin(angle+(pi/2));

}


/* test routine */
const int x_in = input("x");
const int sin_x_out = output("sin_x");
const int cos_x_out = output("cos_x");

void main(){
    double x;

    while(1){
        x = fget_double(x_in);
        fput_double(sin(x), sin_x_out);
        fput_double(cos(x), cos_x_out);
    }

}
