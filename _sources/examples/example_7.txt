

FM Modulation
=============

It is often useful in digital hardware to simulate a sin wave numerically. It
is possible to implements a sinusoidal oscillator, without having to calculate
the value of the sinusoid for each sample. A typical approach to this in
hardware is to store within a lookup table a series of values, and to sweep
through those values at a programmable rate. This method relies on a large
amount of memory, and the memory requirements increase rapidly for high
resolutions. It is possible to improve the resolution using techniques such as
interpolation.  

In this example however, an alternative method is employed,
trigonometric recurrence allows us to calculate the sin and cosine of a small
angle just once. From there, subsequent samples can be found using multipliers.


.. code-block:: c

    #include <stdio.h>
    #include <math.h>
    
    unsigned frequency_in = input("frequency");
    unsigned sin_out = output("sin");
    unsigned cos_out = output("cos");
    
    void dds(){
        float sin_x, cos_x, new_sin, new_cos, si, sr, frequency;
        int i;
    
        cos_x = 1.0;
        sin_x = 0.0;
        sr = cos(2.0 * M_PI/N);
        si = sin(2.0 * M_PI/N);
    
        while(1){
            frequency = fget_float(frequency_in);
            for(i=0; i<frequency; i++){
                new_cos = cos_x*sr - sin_x*si;
                new_sin = cos_x*si + sin_x*sr;
                cos_x = new_cos;
                sin_x = new_sin;
            }
            fput_float(cos_x, sin_out);
            fput_float(sin_x, cos_out);
        }
    
    }

Conveniently, using this method, both a sin and cosine wave are generated. This
is useful in complex mixers which require a coherent sin and cosine wave. We
can control the frequency of the generated wave by stepping through the
waveform more quickly. If the step rate is received from an input, this can be
used to achieve frequency modulation.

.. image:: images/example_7.png

