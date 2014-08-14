typedef struct{int a; int b; int c;} mytype;

void main(){
    mytype a[10][10];

    a[0][0].a = 10;
    a[0][0].b = 20;
    a[0][0].c = 30;
    a[0][1].a = 40;
    a[0][1].b = 50;
    a[0][1].c = 60;
    a[1][0].a = 70;
    a[1][0].b = 80;
    a[1][0].c = 90;

    report(a[0][0].a);
    report(a[0][0].b);
    report(a[0][0].c);
    report(a[0][1].a);
    report(a[0][1].b);
    report(a[0][1].c);
    report(a[1][0].a);
    report(a[1][0].b);
    report(a[1][0].c);
}

