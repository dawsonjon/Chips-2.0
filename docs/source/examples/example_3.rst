

Example 3 - Calculate Sqrt using Newton's Method
------------------------------------------------

In this example, we calculate the sqrt of a number using `Newton's method
<http://en.wikipedia.org/wiki/Newton's_method#Square_root_of_a_number>`_:

Starting with an initial estimate of the sqrt, successively better approximations can be found thus:

.. math::

    f(x_1) = x_0 - \frac{{x_0}^2 - n}{2x_0}

The function terminates when further iterations do not change the approximation.

.. code-block:: c

    /* Find absolute value iof a floating point number*/
    
    float fabs(float n){
        if (n < 0.0) {
            return - n;
        } else {
            return n;
        }
    }
    
    /* Approximate sqrt using newton's method*/
    
    float sqrt(float n){
        float square, x, old;
        x = 10.0;
        old = 0.0;
        while(fabs(old - x) > 0.000001){
            old = x;
            x -= (x*x-n)/(2*x);
        }
        return x;
    }
    
    /* Test Sqrt Function*/
    
    void main(){
        float x;
        for(x=0.0; x <= 10.0; x+= 0.1){
            file_write(x, "x");
            file_write(sqrt(x), "sqrt_x");
        }
    }

A simple test calulates sqrt(x) where -10 < x < 10.

.. image:: images/example_3.png

