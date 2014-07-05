/* Chips-2.0 FIR Filter Example */
/* Jonathan P Dawson 2014-07-05 */

#include <stdio.h>

unsigned in = input("a");
unsigned out = output("z");
unsigned kernel_in = input("k");

void fir_filter(){
    unsigned i = 0;
    unsigned inp = 0;
    float delay[N];
    float kernel[N];
    float data_out;

    /* read in filter kernel */
    for(i=0; i<N; i++){
       kernel[i] = fget_float(kernel_in);
    }


    /* execute filter on input stream */
    while(1){
        delay[inp] = fget_float(in);
        data_out=0.0; i=0;
        while(1){
            data_out += delay[inp] * kernel[i];
            if(i == N-1) break;
            i++;
            if(inp == N-1){
                inp=0;
            }else{
                inp++;
            }
        }
        fput_float(data_out, out);
    }
}
