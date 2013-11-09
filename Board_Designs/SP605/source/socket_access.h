int put_char(int i){
	report(i);
	return 0;
}

unsigned socket_put_decimal(unsigned value){
	int digit_0 = '0';
	int digit_1 = '0';
	int digit_2 = '0';
	int digit_3 = '0';
	int digit_4 = '0';

	while(value >= 10000){
		digit_4++;
		value -= 10000;
	}
	put_char(digit_4);
	while(value >= 1000){
		digit_3++;
		value -= 1000;
	}
	put_char(digit_3);
	while(value >= 100){
		digit_2++;
		value -= 100;
	}
	put_char(digit_2);
	while(value >= 10){
		digit_1++;
		value -= 10;
	}
	put_char(digit_1);
	while(value >= 1){
		digit_0++;
		value -= 1;
	}
	put_char(digit_0);
	return 0;
}
