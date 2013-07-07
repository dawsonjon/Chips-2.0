//Test the adder component
int left_shift_test()
{
  output_a(0xffff); output_b(0); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(1); assert(input_a() == 0xfffe);
  output_a(0xffff); output_b(2); assert(input_a() == 0xfffc);
  output_a(0xffff); output_b(3); assert(input_a() == 0xfff8);
  output_a(0xffff); output_b(4); assert(input_a() == 0xfff0);
  output_a(0xffff); output_b(5); assert(input_a() == 0xffe0);
  output_a(0xffff); output_b(6); assert(input_a() == 0xffc0);
  output_a(0xffff); output_b(7); assert(input_a() == 0xff80);
  output_a(0xffff); output_b(8); assert(input_a() == 0xff00);
  output_a(0xffff); output_b(9); assert(input_a() == 0xfe00);
  output_a(0xffff); output_b(10); assert(input_a() == 0xfc00);
  output_a(0xffff); output_b(11); assert(input_a() == 0xf800);
  output_a(0xffff); output_b(12); assert(input_a() == 0xf000);
  output_a(0xffff); output_b(13); assert(input_a() == 0xe000);
  output_a(0xffff); output_b(14); assert(input_a() == 0xc000);
  output_a(0xffff); output_b(15); assert(input_a() == 0x8000);
  output_a(0xffff); output_b(16); assert(input_a() == 0x0000);
  report(1);
  return 0;
}
