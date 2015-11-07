#define CLOCKS_PER_SEC 10
#include <time.h>
#include <stdio.h>
stdout = output(console);

void main(){
    time_t t1, t2;
    
    t1 = clock();
    t2 = clock();
    assert(t2 > t1);
    t1 = time((time_t*)NULL);
    t2 = time((time_t*)NULL);
    assert(t2 > t1);
    
    /* test gmtime */
    time_t t3, t4;
    tm *t;
    t3 = 0;
    t = gmtime(&t3);
    assert(t->tm_year == 70);
    assert(t->tm_mon == 0);
    assert(t->tm_mday == 1);
    assert(t->tm_hour == 0);
    assert(t->tm_min == 0);
    assert(t->tm_sec == 0);
    assert(t->tm_yday == 0);
    assert(t->tm_wday == 4);

    t3 = mktime(t);
    assert(t3 == 0);

    t4 = 1445539690;
    t = gmtime(&t4);
    assert(t->tm_year == 115);
    assert(t->tm_mon == 9);
    assert(t->tm_mday == 22);
    assert(t->tm_hour == 18);
    assert(t->tm_min == 48);
    assert(t->tm_sec == 10);
    assert(t->tm_yday == 294);
    assert(t->tm_wday == 4);

    t4 = mktime(t);
    assert(t4 == 1445539690);

    t4 = 1445888259;
    tz_offset = 3600; 
    t = localtime(&t4);
    assert(t->tm_year == 115);
    assert(t->tm_mon == 9);
    assert(t->tm_mday == 26);
    assert(t->tm_hour == 20);
    assert(t->tm_min == 37);
    assert(t->tm_sec == 39);
    assert(t->tm_yday == 298);
    assert(t->tm_wday == 1);

    t4 = mktime(t);
    assert(t4 == 1445888259);

    puts(asctime(t));

}
