int print(int string[])
{
  int i;
  while( string[i] ) output_serial(string[i++]);
  return 0;
}


int board_test()
{
  int string[] = "blah";
  print(string);
  return 0;
}
