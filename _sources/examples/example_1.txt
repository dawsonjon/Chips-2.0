

Calculate Square Root using Newton's Method
===========================================

In this example, we calculate the sqrt of a number using `Newton's method
<http://en.wikipedia.org/wiki/Newton's_method#Square_root_of_a_number>`_.
The problem of finding the square root can be expressed as:

.. math::

     n = x^2

Which can be rearranged as:

.. math::

     f(x) = x^2 - n

Using Newton's method, we can find numerically the approximate point at which
:math:`f(x) = 0`. Repeated applications of the following expression yield
increasingly accurate approximations of the Square root:

.. math::

    f(x_k) = x_{k-1} - \frac{{x_{k-1}}^2 - n}{2x_{k-1}}

Turning this into a practical solution, the following code calculates the square
root of a floating point number. An initial approximation is refined using
Newton's method until further refinements agree to within a small degree.

.. code-block:: c

    /* sqrt.c */
    /* Jonathan P Dawson */
    /* 2013-12-23 */
    
    #include <stdio.h>
    
    /* approximate sqrt using newton's method*/
    double sqrt(double n){
        double square, x, old;
        x = n;
        old = 0.0;
        while(old != x){
            old = x;
            x = (x + n/x)*0.5;
        }
        return x;
    }
    
    /* test sqrt function*/
    const int x_in = input("x");
    const int sqrt_x_out = output("sqrt_x");
    void main(){
        double x;
        while(1){
            x = fget_float(x_in);
            fput_float(sqrt(x), sqrt_x_out);
        }
    }

Note that the code isn't entirely robust, and cannot handle special cases such
as Nans, infinities or negative numbers.  A simple test calculates
:math:`\sqrt{x}` where :math:`-10 < x < 10`.

.. image:: images/example_1.png

