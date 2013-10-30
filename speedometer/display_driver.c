int update_digit(int value)
{
  if      ( value == 0 ) output_digit(0x7E);
  else if ( value == 1 ) output_digit(0x30);
  else if ( value == 2 ) output_digit(0x6d);
  else if ( value == 3 ) output_digit(0x79);
  else if ( value == 4 ) output_digit(0x33);
  else if ( value == 5 ) output_digit(0x5b);
  else if ( value == 6 ) output_digit(0x5f);
  else if ( value == 7 ) output_digit(0x70);
  else if ( value == 8 ) output_digit(0x7f);
  else if ( value == 9 ) output_digit(0x7b);
  return 0;
}

int display_driver()
{
  int i, speed, hundreds, tens, ones, halves;

  while(1)
  {

    if( ready_speed() )
    {
      speed = input_speed();
      for(hundreds = 0; speed > 200; speed -= 200) hundreds++;
      for(tens = 0; speed > 20; speed -= 20) tens++;
      for(ones = 0; speed > 2; speed -= 2) ones++;
      halves = speed?5:0;
    }

    output_digit_select(1);
    update_digit(hundreds);
    for(i=0; i<50; i++)
      wait_clocks(10000);//100 times/second

    output_digit_select(2);
    update_digit(tens);
    for(i=0; i<50; i++)
      wait_clocks(10000);//100 times/second

    output_digit_select(4);
    update_digit(ones);
    for(i=0; i<50; i++)
      wait_clocks(10000);//100 times/second

    output_digit_select(8);
    update_digit(halves);
    for(i=0; i<50; i++)
      wait_clocks(10000);//100 times/second
 
  } 
  
  return 0;
}
