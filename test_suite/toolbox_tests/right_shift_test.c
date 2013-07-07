//Test the adder component
int right_shift_test()
{
  output_a(0xffff); output_b(0); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(1); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(2); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(3); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(4); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(5); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(6); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(7); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(8); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(9); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(10); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(11); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(12); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(13); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(14); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(15); assert(input_a() == 0xffff);
  output_a(0xffff); output_b(16); assert(input_a() == 0xffff);
  output_a(0x7fff); output_b(0); assert(input_a() == 0x7fff);
  output_a(0x7fff); output_b(1); assert(input_a() == 0x3fff);
  output_a(0x7fff); output_b(2); assert(input_a() == 0x1fff);
  output_a(0x7fff); output_b(3); assert(input_a() == 0x0fff);
  output_a(0x7fff); output_b(4); assert(input_a() == 0x07ff);
  output_a(0x7fff); output_b(5); assert(input_a() == 0x03ff);
  output_a(0x7fff); output_b(6); assert(input_a() == 0x01ff);
  output_a(0x7fff); output_b(7); assert(input_a() == 0x00ff);
  output_a(0x7fff); output_b(8); assert(input_a() == 0x007f);
  output_a(0x7fff); output_b(9); assert(input_a() == 0x003f);
  output_a(0x7fff); output_b(10); assert(input_a() == 0x001f);
  output_a(0x7fff); output_b(11); assert(input_a() == 0x000f);
  output_a(0x7fff); output_b(12); assert(input_a() == 0x7);
  output_a(0x7fff); output_b(13); assert(input_a() == 0x3);
  output_a(0x7fff); output_b(14); assert(input_a() == 0x1);
  output_a(0x7fff); output_b(15); assert(input_a() == 0x0);
  report(1);
  return 0;
}
