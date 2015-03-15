#include <stdlib.h>


void test_division(unsigned a, unsigned b){
    unsigned int q, r;
    q = a / b;
    r = a % b;
    if(a != b*q+r){
        report(a);
        report(b);
        report(q);
        report(r);
        assert(0);
    }
}

void main(){
    unsigned int a, b;
    int i, j=0;

    srand(555555);
    
    for(i=0; i<100; i++){ 
        a = rand();
        test_division(a, 1);
        test_division(a, 0x10000000u);
        test_division(a, 0x20000000u);
        test_division(a, 0x40000000u);
        test_division(a, 0x7fffffffu);
        test_division(a, 0x80000000u);
        test_division(a, 0xffffffffu);
        test_division(0x00000000u, a);
        test_division(0x00000001u, a);
        test_division(0x10000000u, a);
        test_division(0x20000000u, a);
        test_division(0x40000000u, a);
        test_division(0x7fffffffu, a);
        test_division(0x80000000u, a);
        test_division(0xffffffffu, a);
        report(j++);
    }

}
