//Test the subtractor component
int subtractor_test()
{
  output_a(0); output_b(1); assert(input_a() == -1);
  output_a(0); output_b(2); assert(input_a() == -2);
  output_a(0); output_b(3); assert(input_a() == -3);
  output_a(0x8000); output_b(0); assert(input_a() == 0x8000);
  output_a(0x8000); output_b(1); assert(input_a() == 0x7fff);
  output_a(0x8000); output_b(2); assert(input_a() == 0x7ffe);
  output_a(0x0000); output_b(0); assert(input_a() == 0x0000);
  output_a(0x0000); output_b(1); assert(input_a() == 0xffff);
  output_a(0x0000); output_b(2); assert(input_a() == 0xfffe);
  output_a(1); output_b(1); assert(input_a() == 0);
  report(1);
  return 0;
}
