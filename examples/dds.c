#include <stdio.h>
#include <math.h>

unsigned frequency_in = input("frequency");
unsigned sin_out = output("sin");
unsigned cos_out = output("cos");

void main(){
    float sin_x, cos_x, new_sin, new_cos, si, sr, frequency;
    int i;

    cos_x = 1.0;
    sin_x = 0.0;
    sr = cos(2.0 * M_PI/N);
    si = sin(2.0 * M_PI/N);

    while(1){
        frequency = fget_float(frequency_in);
        for(i=0; i<frequency; i++){
            new_cos = cos_x*sr - sin_x*si;
            new_sin = cos_x*si + sin_x*sr;
            cos_x = new_cos;
            sin_x = new_sin;
        }
        fput_float(cos_x, sin_out);
        fput_float(sin_x, cos_out);
    }

}
