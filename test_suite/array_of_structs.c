typedef struct{int a; int b; int c;} mytype;

void main(){
    mytype a[10][10];
    mytype b[10][10];

    a[0][0].a = 10;
    a[0][0].b = 20;
    a[0][0].c = 30;
    a[0][1].a = 40;
    a[0][1].b = 50;
    a[0][1].c = 60;
    a[1][0].a = 70;
    a[1][0].b = 80;
    a[1][0].c = 90;
    b[0][0].a = 110;
    b[0][0].b = 120;
    b[0][0].c = 130;
    b[0][1].a = 140;
    b[0][1].b = 150;
    b[0][1].c = 160;
    b[1][0].a = 170;
    b[1][0].b = 180;
    b[1][0].c = 190;

    assert(a[0][0].a == 10);
    assert(a[0][0].b == 20);
    assert(a[0][0].c == 30);
    assert(a[0][1].a == 40);
    assert(a[0][1].b == 50);
    assert(a[0][1].c == 60);
    assert(a[1][0].a == 70);
    assert(a[1][0].b == 80);
    assert(a[1][0].c == 90);
    assert(b[0][0].a == 110);
    assert(b[0][0].b == 120);
    assert(b[0][0].c == 130);
    assert(b[0][1].a == 140);
    assert(b[0][1].b == 150);
    assert(b[0][1].c == 160);
    assert(b[1][0].a == 170);
    assert(b[1][0].b == 180);
    assert(b[1][0].c == 190);
}

