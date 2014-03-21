C Libraries
===========

Not all of the libC is supported. The library is under development, and the intention is to make the library as complete as possible.
There will be occasions, where the libc functions can't be implemented, or have to differ from the standard.

print.h
-------

The `print_string` function prints a null terminated string to standard output.

.. code-block:: c

    void print_string(char string[]);

The `print_decimal` function prints a number in decimal to standard output.

.. code-block:: c

    void print_decimal(int value);

The `print_hex` function prints a number in hexadecimal format to standard output.

.. code-block:: c

    void print_hex(int value);

The `print_float` function prints a floatin point number to standard output.

.. code-block:: c

    void print_float(float value);

To provide flexibility, the definition of standard output is left to the
user, it could be a serial port, an LCD display, or perhaps a telnet session.
To define standard output, a function `stdout_put_char` function must be
defined before including print.h.

.. code-block:: c

    void stdout_put_char(char value){
        output_rs232_tx(value);
    }

    #include <print.h>

    print_string("Hello World!\n"); //Hello World!
    print_decimal(12345); //12345
    print_hex(127); //7f
    print_float(1.0); //1.0

scan.h
------

The `scan_hex` function reads a hex value from standard input.

.. code-block:: c

    int scan_hex();

The `scan_decimal` function reads an integer from standard input.

.. code-block:: c

    int scan_decimal();

The `scan_decimal` function reads an float from standard input.

.. code-block:: c

    float scan_float();

To provide flexibility, the definition of standard input is left to the user.
To define standard output, a function `stdin_get_char` function must be defined
before including print.h.

ctypes.h
--------

The `isalnum` function returns 1 if c is an aphanumeric character otherwise 0.

.. code-block:: c

    unsigned isalnum(char c);

The `isalpha` function returns 1 if c is a letter otherwise 0.

.. code-block:: c

    unsigned isalpha(char c);

The `islower` function returns 1 if c is a lower case letter otherwise 0.

.. code-block:: c

    unsigned islower(char c);

The `isupper` function returns 1 if c is an upper case letter otherwise 0.

.. code-block:: c

    unsigned isupper(char c);

The `isdigit` function returns 1 if c is a digit otherwise 0.

.. code-block:: c

    unsigned isdigit(char c);

The `isxdigit` function returns 1 if c is a hexadecimal digit otherwise 0.

.. code-block:: c

    unsigned isxdigit(char c);

The `isgraph` function returns 1 if c is a printing character not including space otherwise 0.

.. code-block:: c

    unsigned isgraph(char c);

The `isspace` function returns 1 if c is white space character otherwise 0.

.. code-block:: c

    unsigned isspace(char c);

The `isprint` function returns 1 if c is a printing character otherwise 0.

.. code-block:: c

    unsigned isprint(char c);

The `ispunct` function returns 1 if c is punctuation otherwise 0.

.. code-block:: c

    unsigned ispunct(char c);

The `toupper` function returns the upper case equivilent of c if any otherwise c.

.. code-block:: c

    unsigned toupper(char c);

The `tolower` function returns the lower case equivilent of c if any otherwise c.

.. code-block:: c

    unsigned tolower(char c);

math.h
------

All angles are expressed in radians.

The `M_LOG2E` constant respresents an approximation of :math:`log_{2} e`.

.. code-block:: c

    const float M_LOG2E

The `M_LOG10E` constant respresents an approximation of :math:`log_{10} e`.

.. code-block:: c

    const float M_LOG10E

The `M_LN2` constant respresents an approximation of :math:`log_{e} 2`.

.. code-block:: c

    const float M_LN2

The `M_LN10` constant respresents an approximation of :math:`log_{e} 10`.

.. code-block:: c

    const float M_LN10

The `M_PI` constant respresents an approximation of :math:`\pi`.

.. code-block:: c

    const float M_PI

The `M_PI_2` constant respresents an approximation of :math:`\pi/2`.

.. code-block:: c

    const float M_PI_2

The `M_PI_4` constant respresents an approximation of :math:`\pi/4`.

.. code-block:: c

    const float M_PI_4

The `M_1_PI` constant respresents an approximation of :math:`1/\pi`.

.. code-block:: c

    const float M_1_PI

The `M_2_PI` constant respresents an approximation of :math:`2/\pi`.

.. code-block:: c

    const float M_2_PI

The `M_2_SQRTPI` constant respresents an approximation of :math:`2/\sqrt{\pi}`.

.. code-block:: c

    const float M_2_SQRTPI

The `M_SQRT2` constant respresents an approximation of :math:`\sqrt{2}`.

.. code-block:: c

    const float M_SQRT2

Return the :math:`cos x`.

.. code-block:: c

    float cos(float x);

Return the :math:`sin x`.

.. code-block:: c

    float sin(float x);

Return the :math:`tan x`.

.. code-block:: c

    float tan(float x);

Return the :math:`sinh x`.

.. code-block:: c

    float sinh(float x);

Return the :math:`cosh x`.

.. code-block:: c

    float cosh(float x);

Return the :math:`tanh x`.

.. code-block:: c

    float tanh(float x);

Return the :math:`asinh x`.

.. code-block:: c

    float asinh(float x);

Return the :math:`acosh x`.

.. code-block:: c

    float acosh(float x);

Return the :math:`atanh x`.

.. code-block:: c

    float atanh(float x);

Return the absolute value of float n.

.. code-block:: c

    float fabs(float n);

Return the absolute value of int n.

.. code-block:: c

    int abs(int n);

Return the :math:`e^x`. 

.. code-block:: c

    float exp(float x);

Return the :math:`log_{e} n`. 

.. code-block:: c

    float log(float n);

Return the :math:`log_{10} n`. 

.. code-block:: c

    float log10(float n);

Return the :math:`log_{2} n`. 

.. code-block:: c

    float log2(float n);

stdlib.h
--------

Return the maximum value returned by the rand function. 

.. code-block:: c

    const unsigned long RAND_MAX

Set the random seed to s. 

.. code-block:: c

    void srand(unsigned long int s);

Return a random integer in the range :math:`0 \le x \le RAND\_MAX`. 

.. code-block:: c

    unsigned long rand();
