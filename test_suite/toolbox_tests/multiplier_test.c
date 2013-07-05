//Test the adder component
int multiplier_test()
{
  output_a(0); output_b(0); assert(input_a() == 0);
  output_a(0); output_b(1); assert(input_a() == 0);
  output_a(0); output_b(2); assert(input_a() == 0);
  output_a(0); output_b(0x7fff); assert(input_a() == 0);
  output_a(2); output_b(0x3fff); assert(input_a() == 0x7ffe);
  output_a(1); output_b(0x7fff); assert(input_a() == 0x7fff);
  output_a(1); output_b(0xffff); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(0xffff); assert(input_a() == 0x0001);
  output_a(1); output_b(-1); assert(input_a() == -1);
  report(1);
  return 0;
}
