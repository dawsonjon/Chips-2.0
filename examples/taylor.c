float sinf(float angle){

    float approximation, sign, power, fact;
    unsigned count, i;
    unsigned iterations=10;

    approximation = angle;
    sign = -1.0;

    for(i=3; i<=iterations; i+=2){

	power = 1.0;
	fact = 1;
	for(count=0; count<i; count++){
	    //calculate x**i
	    power*=angle;

	    //calculate x!
	    fact = fact*count;
	    count++;
	}

	//calculate x**i/i!
	approximation += sign*(power/fact);
	sign = -sign;

    }
    return approximation;

}

void main(){
    float x;
    float pi=3.14159265359;
    float step=pi/100;

    for(x=0.0; x <= pi; x += step){
        file_write(x, "sin_x");
    }
}
