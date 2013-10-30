int count_revs()
{
  int count;
  while(1)
  {
    for(count = 0; !ready_seconds(); count++)
    {
        while(input_sensor()) count;
        while(!input_sensor()) count;
    }
    input_seconds();
    //speed in 0.5 mph steps
    output_speed(count * 1112 / 500);
  }
  return 0;
}
