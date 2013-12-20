

Example 1 - Approximating trig functions using the Taylor Series
----------------------------------------------------------------

In this example, we calculate an approximation of the cosine functions using
the `Taylor series <http://en.wikipedia.org/wiki/Taylor_series>`_:

.. math::

    \cos (x) = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n)!} x^{2n}

A more versatile Cosine function exploit the symetry of the cosine function to
handle negative angles. Angles outside the calculable range are handled by
moving the function in to the range 0 to 2*pi. A Sine function is synthesised
from the cosine function by subtracting pi/2 from the angle. Other trig
functions could be synthesised using trig identities.

.. code-block:: c

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
    
    /*Redefine sine in terms of cosine*/
    float sin(float angle){
        return cos(angle-(pi/2));
    }
    
    void main(){
        float x;
        float step=pi/50;
    
        for(x=-pi; x <= pi; x += step){
           file_write(x, "x");
           file_write(cos(x), "cos_x");
           file_write(sin(x), "sin_x");
        }
    }

A simple test calulates Sine and Cosine for the range -2*pi to 2*pi.

.. image:: images/example_1.png

