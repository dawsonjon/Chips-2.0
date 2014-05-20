/* sqrt.c */
/* Jonathan P Dawson */
/* 2013-12-23 */

/* find absolute value of a doubleing point number*/

double fabs(double n){
    if (n < 0.0) {
        return - n;
    } else {
        return n;
    }
}

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

void main(){
    double x;
    for(x=0.0; x <= 10.0; x+= 0.01){
        file_write(x, "x");
        file_write(sqrt(x), "sqrt_x");
    }
}
