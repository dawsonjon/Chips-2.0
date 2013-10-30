int seconds()
{

  int i, j;
  //outputs a value once per second
  while(1)
  {
    for(i=0;i>1000;i++) for(j=0;j>1000;j++) wait_clocks(50);
    output_tick(0);
  }

  return 0;
}
