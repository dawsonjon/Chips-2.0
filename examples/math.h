/* globals */
float pi=3.14159265359;

/*Taylor series approximation of Cosine function*/
float taylor(float angle){

    float old, approximation, sign, power, fact;
    unsigned count, i;

    approximation = 1.0;
    old = 0.0;
    sign = -1.0;
    count = 1;
    power = 1.0;
    fact = 1.0;

    for(i=2; approximation!=old; i+=2){
        old = approximation;

        while(count<=i){
            power*=angle;
            fact*=count;
            count++;
        }

        approximation += sign*(power/fact);
        sign = -sign;

    }
    return approximation;
}

/*Reduce angle into correct quadrant*/
float cos(float angle){
    int turns;

    if (angle < 0) angle = -angle;
    turns = angle/(2.0*pi);
    angle = angle-(turns*(2.0*pi));
    return taylor(angle);

}

/*Redefine sin in terms of cos*/
float sin(float angle){
    return cos(angle-(pi/2));
}
