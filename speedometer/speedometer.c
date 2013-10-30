int calculate_speed()
{
	while(1)
	{
		count = 0;
		while(!ready_seconds())
		{
			while (input_sensor());
			count ++;
			while (!input_sensor());
		}
		speed = (count * 1112)/500 //0.5 mph steps
		output_speed();
	}
}
