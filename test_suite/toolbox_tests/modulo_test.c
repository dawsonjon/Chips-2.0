//Test the adder component
int modulo_test()
{
  output_a(7); output_b(8); assert(input_a()==7);
  output_a(15); output_b(8); assert(input_a()==7);
  output_a(16); output_b(8); assert(input_a()==0);
  output_a(-7); output_b(8); assert(input_a()==-7);
  output_a(-15); output_b(8); assert(input_a()==-7);
  output_a(-16); output_b(8); assert(input_a()==-0);
  output_a(7); output_b(-8); assert(input_a()==7);
  output_a(15); output_b(-8); assert(input_a()==7);
  output_a(16); output_b(-8); assert(input_a()==0);
  report(1);
  return 0;
}
