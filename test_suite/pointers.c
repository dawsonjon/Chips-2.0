void main(){
    long a[5];
    long* pa;

    pa = a;

    a[0] = 0;
    a[1] = 1;
    a[2] = 2;
    a[3] = 3;
    a[4] = 4;

    assert(*pa == 0);
    assert(*pa+1 == 1);
    assert(*pa+2 == 2);
    assert(*pa+3 == 3);
    assert(*pa+4 == 4);

    report(&a[4] - &a[0]);

}
