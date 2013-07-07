//Test the adder component
int divider_test()
{
  output_a(15); output_b(3); assert(input_a()==5);
  output_a(15); output_b(5); assert(input_a()==3);
  output_a(10); output_b(5); assert(input_a()==2);
  output_a(15); output_b(-3); assert(input_a()==-5);
  output_a(15); output_b(-5); assert(input_a()==-3);
  output_a(10); output_b(-5); assert(input_a()==-2);
  output_a(-15); output_b(3); assert(input_a()==-5);
  output_a(-15); output_b(5); assert(input_a()==-3);
  output_a(-10); output_b(5); assert(input_a()==-2);
  output_a(-15); output_b(-3); assert(input_a()==5);
  output_a(-15); output_b(-5); assert(input_a()==3);
  output_a(-10); output_b(-5); assert(input_a()==2);
  report(1);
  return 0;
}
