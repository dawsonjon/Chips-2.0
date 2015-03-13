  void myprint(char x) {
      report(x); 
  }

  int main() {
     void (*test)(char);
     void (*test2)(char);

     test = myprint;
     //test2 = &myprint;

     test(123);
     (*test)(456);
     //test2(789);
     //(*test2)(012);

  }
