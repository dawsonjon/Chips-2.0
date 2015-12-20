
C Libraries
===========


ctype.h
-------


The isalnum function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isalnum(int c);

Description:

   The isalnum function tests for any character for which isalpha or
   isdigit is true.


The isalpha function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isalpha(int c);

Description:

   The isalpha function tests for any character for which isupper or
   islower is true, or any of an implementation-defined set of characters
   for which none of iscntrl, isdigit, ispunct, or isspace is true.
   In the C locale, isalpha returns true only for the characters for
   which isupper or islower is true.


The iscntrl function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int iscntrl(int c);

Description:

   The iscntrl function tests for any control character.


The isdigit function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isdigit(int c);

Description:

   The isdigit function tests for any decimal-digit character.


The isgraph function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isgraph(int c);

Description:

   The isgraph function tests for any printing character except space (' ').


The islower function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int islower(int c);

Description:

   The islower function tests for any lower-case letter or any of an
   implementation-defined set of characters for which none of iscntrl,
   isdigit, ispunct, or isspace is true.  In the C locale, islower
   returns true only for the characters defined as lower-case letters.


The isprint function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isprint(int c);

Description:

   The isprint function tests for any printing character including
   space (' ').


The ispunct function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int ispunct(int c);

Description:

   The ispunct function tests for any printing character except space
   (' ') or a character for which isalnum is true.


The isspace function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isspace(int c);

Description:

   The isspace function tests for the standard white-space characters
   or for any of an implementation-defined set of characters for which
   isalnum is false.  The standard white-space characters are the
   following: space (' '), form feed ('\f'), new-line ('\n'), carriage
   return ('\r'), horizontal tab ('\t'), and vertical tab ('\v').  In the
   C locale, isspace returns true only for the standard white-space
   characters.


The isupper function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isupper(int c);

Description:

   The isupper function tests for any upper-case letter or any of an
   implementation-defined set of characters for which none of iscntrl,
   isdigit, ispunct, or isspace is true.  In the C locale, isupper
   returns true only for the characters defined as upper-case letters.


The isxdigit function
*********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int isxdigit(int c);

Description:

   The isxdigit function tests for any hexadecimal-digit character.


The tolower function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int tolower(int c);

Description:

   The tolower function converts an upper-case letter to the
   corresponding lower-case letter.

Returns:

   If the argument is an upper-case letter, the tolower function
   returns the corresponding lower-case letter if there is one; otherwise
   the argument is returned unchanged.  In the C locale, tolower maps
   only the characters for which isupper is true to the corresponding
   characters for which islower is true.


The toupper function
********************

Synopsis:

    .. code-block:: c

         #include <ctype.h>
         int toupper(int c);

Description:

   The toupper function converts a lower-case letter to the corresponding upper-case letter.

Returns:

   If the argument is a lower-case letter, the toupper function
   returns the corresponding upper-case letter if there is one; otherwise
   the argument is returned unchanged.  In the C locale, toupper maps
   only the characters for which islower is true to the corresponding
   characters for which isupper is true.

math.h
------


The isfinite macro
******************

Synopsis:

.. code-block:: c

        #include <math.h>
        int isfinite(real-floating x);

Description:

    The isfinite macro determines whether its argument has a finite value (zero,
    subnormal, or normal, and not infinite or NaN). First, an argument represented in a
    format wider than its semantic type is converted to its semantic type. Then determination
    is based on the type of the argument.
    Since an expression can be evaluated with more range and precision than its type has, it is important to
    know the type that classification is based on. For example, a normal long double value might
    become subnormal when converted to double, and zero when converted to float.

Returns:

The isfinite macro returns a nonzero value if and only if its argument has a finite
value.

The isinf macro
***************

Synopsis:

.. code-block:: c

    #include <math.h>
    int isinf(real-floating x);

Description:

    The isinf macro determines whether its argument value is an infinity (positive or
    negative). First, an argument represented in a format wider than its semantic type is
    converted to its semantic type. Then determination is based on the type of the argument.

Returns:

    The isinf macro returns a nonzero value if and only if its argument has an infinite
    value.


The isnan macro
***************

Synopsis:

.. code-block:: c

        #include <math.h>
        int isnan(real-floating x);

Description:

    The isnan macro determines whether its argument value is a NaN. First, an argument
    represented in a format wider than its semantic type is converted to its semantic type.
    Then determination is based on the type of the argument.

Returns:

    The isnan macro returns a nonzero value if and only if its argument has a NaN value.


The isnormal macro
******************

Synopsis:

.. code-block:: c

        #include <math.h>
        int isnormal(real-floating x);

..

    For the isnan macro, the type for determination does not matter unless the implementation supports
    NaNs in the evaluation type but not in the semantic type.

Description:

    The isnormal macro determines whether its argument value is normal (neither
    zero, subnormal, infinite, nor NaN). First, an argument
    represented in a format wider than its semantic type is converted to its
    semantic type. Then determination is based on the type of the argument.

Returns:

    The isnormal macro returns a nonzero value if and only if its argument has a
    normal value.


The signbit macro (not in C89)
******************************

Synopsis:

.. code-block:: c

    #include <math.h>
    int signbit(real-floating x);

Description:

    The signbit macro determines whether the sign of its argument value is negative.

Returns:

    The signbit macro returns a nonzero value if and only if the sign of its argument value
    is negative.

The fabs function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double fabs(double x);

Description:

   The fabs function computes the absolute value of a floating-point
   number x.

Returns:

   The fabs function returns the absolute value of x.


The modf function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double modf(double value, double *iptr);

Description:

   The modf function breaks the argument value into integral and
   fractional parts, each of which has the same sign as the argument.  It
   stores the integral part as a double in the object pointed to by iptr.

Returns:

   The modf function returns the signed fractional part of value.


The fmod function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double fmod(double x, double y);

Description:

   The fmod function computes the floating-point remainder of x/y.

Returns:

   The fmod function returns the value x i y , for some integer i such
   that, if y is nonzero, the result has the same sign as x and magnitude
   less than the magnitude of y.  If y is zero, whether a domain error
   occurs or the fmod function returns zero is implementation-defined.


The exp function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double exp(double x);

Description:

   The exp function computes the exponential function of x.  A range
   error occurs if the magnitude of x is too large.

Returns:

   The exp function returns the exponential value.


The sqrt function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double sqrt(double x);

Description:

   The sqrt function computes the nonnegative square root of x.  A
   domain error occurs if the argument is negative.

Returns:

   The sqrt function returns the value of the square root.


The pow function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double pow(double x, double y);

Description:

   The pow function computes x raised to the power y.  A domain error
   occurs if x is negative and y is not an integer.  A domain error
   occurs if the result cannot be represented when x is zero and y is
   less than or equal to zero.  A range error may occur.

Returns:

   The pow function returns the value of x raised to the power y.


The ldexp function
******************

Synopsis:

.. code-block:: c

         #include <math.h>
         double ldexp(double x, int exp);

Description:

   The ldexp function multiplies a floating-point number by an
   integral power of 2.  A range error may occur.

Returns:

   The ldexp function returns the value of x times 2 raised to the
   power exp.


The frexp function
******************

Synopsis:

.. code-block:: c

         #include <math.h>
         double frexp(double value, int *exp);

Description:

   The frexp function breaks a floating-point number into a normalized
   fraction and an integral power of 2.  It stores the integer in the int
   object pointed to by exp.

Returns:

   The frexp function returns the value x , such that x is a double
   with magnitude in the interval [1/2, 1) or zero, and value equals x
   times 2 raised to the power *exp.  If value is zero, both parts of
   the result are zero.


The floor function
******************

Synopsis:

.. code-block:: c

         #include <math.h>
         double floor(double x);

Description:

   The floor function computes the largest integral value not greater
than x.

Returns:

   The floor function returns the largest integral value not greater
   than x , expressed as a double.


The ceil function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double ceil(double x);

Description:

   The ceil function computes the smallest integral value not less than x.

Returns:

   The ceil function returns the smallest integral value not less than
   x , expressed as a double.


The cos function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double cos(double x);

Description:

   The cos function computes the cosine of x (measured in radians).  A
   large magnitude argument may yield a result with little or no
   significance.

Returns:

   The cos function returns the cosine value.


The sin function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double sin(double x);

Description:

   The sin function computes the sine of x (measured in radians).  A
   large magnitude argument may yield a result with little or no
   significance.

Returns:

   The sin function returns the sine value.


The tan function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double tan(double x);

Description:

   The tan function returns the tangent of x (measured in radians).  A large magnitude argument may yield a result with little or no significance.

Returns:

   The tan function returns the tangent value.


The atan function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double atan(double x);

Description:

   The atan function computes the principal value of the arc tangent of x.

Returns:

   The atan function returns the arc tangent in the range [-PI/2, +PI/2]
   radians.


The atan2 function
******************

Synopsis:

.. code-block:: c

         #include <math.h>
         double atan2(double y, double x);

Description:

   The atan2 function computes the principal value of the arc tangent
   of y/x , using the signs of both arguments to determine the quadrant
   of the return value.  A domain error may occur if both arguments are
   zero.

Returns:

   The atan2 function returns the arc tangent of y/x , in the range
   [-PI, +PI] radians.


The asin function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double asin(double x);

Description:

   The asin function computes the principal value of the arc sine of x.
   A domain error occurs for arguments not in the range [-1, +1].

Returns:

   The asin function returns the arc sine in the range [-PI/2, +PI/2]
   radians.


The acos function
*****************

Synopsis:

.. code-block:: c

  #include <math.h>
  double acos(double x);

Description:

  The acos function computes the principal value of the arc cosine of x.
  A domain error occurs for arguments not in the range [-1, +1].

Returns:

  The acos function returns the arc cosine in the range [0, PI] radians.


The sinh function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double sinh(double x);

Description:

   The sinh function computes the hyperbolic sine of x.  A range error occurs if the magnitude of x is too large.

Returns:

   The sinh function returns the hyperbolic sine value.


The cosh function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double cosh(double x);

Description:

   The cosh function computes the hyperbolic cosine of x.  A range
   error occurs if the magnitude of x is too large.

Returns:

   The cosh function returns the hyperbolic cosine value.


The tanh function
*****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double tanh(double x);

Description:

   The tanh function computes the hyperbolic tangent of x.

Returns:

   The tanh function returns the hyperbolic tangent value.


The log function
****************

Synopsis:

.. code-block:: c

         #include <math.h>
         double log(double x);

Description:

   The log function computes the natural logarithm of x.  A domain
   error occurs if the argument is negative.  A range error occurs if the
   argument is zero and the logarithm of zero cannot be represented.

Returns:

   The log function returns the natural logarithm.


The log10 function
******************

Synopsis:

.. code-block:: c

         #include <math.h>
         double log10(double x);

Description:

   The log10 function computes the base-ten logarithm of x.  A domain
   error occurs if the argument is negative.  A range error occurs if the
   argument is zero and the logarithm of zero cannot be represented.

Returns:

   The log10 function returns the base-ten logarithm.


The log2 function (Not in C89 standard)
***************************************

Synopsis:

.. code-block:: c

         #include <math.h>
         double log2(double x);

Description:

   The log2 function computes the base-two logarithm of x.  A domain
   error occurs if the argument is negative.  A range error occurs if the
   argument is zero and the logarithm of zero cannot be represented.

Returns:

   The log2 function returns the base-two logarithm.


stdio.h
-------

In contrast to the C standard, `fputc` and `fgetc` are built-in functions, you
do not need to include `stdio.h` to use them.

The globals `stdin` and `stdout` should be set to an input or output by the user.

The `fputs` function prints `string` to the output `handle`.

.. code-block:: c

        void fputs(unsigned string[], unsigned handle);

The `fgets` function reads a line, up to `maxlength` characters, or a line end
from the input `handle`. The string will be null terminated. `maxlength`
includes the null character.

.. code-block:: c

        void fgets(unsigned string[], unsigned maxlength, unsigned handle);

The `puts` function prints `string` to stdout.

.. code-block:: c

        void puts(unsigned string[]);

The `gets` function reads a line, up to `maxlength` characters, or a line end
from stdin. The string will be null terminated. `maxlength`
includes the null character.

.. code-block:: c

        void gets(unsigned string[], unsigned maxlength);

The `getc` returns a single character from stdin.

.. code-block:: c

        unsigned long getc();

The `putc` writes a single character to stdout.

.. code-block:: c

        void putc(unsigned c);

<stdlib.h>
----------

macros
******

The header <stdlib.h> defines the following macros:

+ NULL
+ RAND_MAX
+ MB_CUR_MAX
+ MB_LEN_MAX

.. note::

    The EXIT_FAILURE and EXIT_SUCCESS macros are not defined.

`RAND_MAX` expands to an integral constant expression, the value of which
is the maximum value returned by the rand function.
`MB_CUR_MAX` expands to a positive integer expression whose value is the
maximum number of bytes in a multibyte character for the extended
character set specified by the current locale (category LC_CTYPE ),
and whose value is never greater than `MB_LEN_MAX`.

.. note::

    The EXIT_FAILURE and EXIT_SUCCESS macros are not defined.

`RAND_MAX` expands to an integral constant expression, the value of which
is the maximum value returned by the rand function.


`MB_CUR_MAX` expands to a positive integer expression whose value is the
maximum number of bytes in a multibyte character for the extended
character set specified by the current locale (category LC_CTYPE ),
and whose value is never greater than `MB_LEN_MAX`.

types
*****

The header <stdlib.h> defines the following types:

+ div_t


The atof function
*****************

Synopsis:

    .. code-block:: C

         #include <stdlib.h>
         double atof(const char *nptr);

Description:

   The atof function converts the initial portion of the string
   pointed to by nptr to double representation.  Except for the behavior
   on error, it is equivalent to

         strtod(nptr, (char **)NULL)

Returns:

   The atof function returns the converted value.

.. note::

	This function is not implemented!!!


The atoi function
*****************

Synopsis:

    .. code-block::

         #include <stdlib.h>
         int atoi(const char *nptr);

Description:

   The atoi function converts the initial portion of the string
pointed to by nptr to int representation.  Except for the behavior on
error, it is equivalent to

         (int)strtol(nptr, (char **)NULL, 10)

Returns:

   The atoi function returns the converted value.

.. note::

	This function is not implemented!!!


The atol function
*****************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         long int atol(const char *nptr);

Description:

   The atol function converts the initial portion of the string
pointed to by nptr to long int representation.  Except for the
behavior on error, it is equivalent to

         strtol(nptr, (char **)NULL, 10)

Returns:

   The atol function returns the converted value.

.. note::

	This function is not implemented!!!

The strtod function
*******************

Synopsis:

    .. code-block::

         #include <stdlib.h>
         double strtod(const char *nptr, char **endptr);

.. note::

	This function is not implemented!!!

The strtol function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         long int strtol(const char *nptr, char **endptr, int base);

.. note::

	This function is not implemented!!!


The strtoul function
********************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         unsigned long int strtoul(const char *nptr, char **endptr,
                  int base);

.. note::

	This function is not implemented!!!


The rand function
*****************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int rand(void);

Description:

   The rand function computes a sequence of pseudo-random integers in
   the range 0 to RAND_MAX.

   The implementation shall behave as if no library function calls the
   rand function.

Returns:

   The rand function returns a pseudo-random integer.


The srand function
******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void srand(unsigned int seed);

Description:

   The srand function uses the argument as a seed for a new sequence
   of pseudo-random numbers to be returned by subsequent calls to rand.
   If srand is then called with the same seed value, the sequence of
   pseudo-random numbers shall be repeated.  If rand is called before any
   calls to srand have been made, the same sequence shall be generated as
   when srand is first called with a seed value of 1.

Returns:

   The srand function returns no value.


The malloc function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void *malloc(size_t size);

Description:

   The malloc function allocates space for an object whose size is
   specified by size and whose value is indeterminate.

Returns:

   The malloc function returns either a null pointer or a pointer to
   the allocated space.

The calloc function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void *calloc(size_t nmemb, size_t size);

Description:

   The calloc function allocates space for an array of nmemb objects,
   each of whose size is size.  The space is initialized to all bits
   zero.

Returns:

   The calloc function returns either a null pointer or a pointer to
   the allocated space.


The realloc function
********************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void *realloc(void *ptr, size_t size);


   The realloc function changes the size of the object pointed to by
   ptr to the size specified by size.  The contents of the object shall
   be unchanged up to the lesser of the new and old sizes.  If the new
   size is larger, the value of the newly allocated portion of the object
   is indeterminate.  If ptr is a null pointer, the realloc function
   behaves like the malloc function for the specified size.  Otherwise,
   if ptr does not match a pointer earlier returned by the calloc,
   malloc, or realloc function, or if the space has been deallocated by
   a call to the free or realloc function, the behavior is undefined.  If
   the space cannot be allocated, the object pointed to by ptr is
   unchanged.  If size is zero and ptr is not a null pointer, the object
   it points to is freed.

Returns:

   The realloc function returns either a null pointer or a pointer to
   the possibly moved allocated space.

The free function
*****************


Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void free(void *ptr);

Description:

   The free function causes the space pointed to by ptr to be
   deallocated, that is, made available for further allocation.  If ptr
   is a null pointer, no action occurs.  Otherwise, if the argument does
   not match a pointer earlier returned by the calloc, malloc, or
   realloc function, or if the space has been deallocated by a call to
   free or realloc, the behavior is undefined.

Returns:

   The free function returns no value.


The abort function
******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void abort(void);

.. note::

	this function is not implemented!!!


The atexit function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int atexit(void (*func)(void));

.. note::

	this function is not implemented!!!

The exit function
*****************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void exit(int status);

.. note::

	This function is not implemented!!!


The getenv function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         char *getenv(const char *name);

.. note::

	this function is not implemented!!!


The system function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int system(const char *string);

.. note::

	This function is not implemented!!!


The bsearch function
********************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void *bsearch(const void *key, const void *base,
                  size_t nmemb, size_t size,
                  int (*compar)(const void *, const void *));

.. note::

	This function is not implemented!!!


The qsort function
******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         void qsort(void *base, size_t nmemb, size_t size,
                  int (*compar)(const void *, const void *));

.. note::

	This function is not implemented!!!


The abs function
****************

Synopsis:

    .. code-block:: C

         #include <stdlib.h>
         int abs(int j);

Description:

   The abs function computes the absolute value of an integer j.  If
   the result cannot be represented, the behavior is undefined.

Returns:

   The abs function returns the absolute value.


The div function
****************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         div_t div(int numer, int denom);

Description:

   The div function computes the quotient and remainder of the
   division of the numerator numer by the denominator denom .  If the
   division is inexact, the sign of the resulting quotient is that of the
   algebraic quotient, and the magnitude of the resulting quotient is the
   largest integer less than the magnitude of the algebraic quotient.  If
   the result cannot be represented, the behavior is undefined;
   otherwise, quot * denom + rem shall equal numer .

Returns:

   The div function returns a structure of type div_t, comprising
   both the quotient and the remainder.  The structure shall contain the
   following members, in either order.

   .. code-block:: c

         int quot;   /*  quotient */
         int rem;    /*  remainder */


The labs function
*****************

Synopsis:

    ..code-block::

         #include <stdlib.h>
         long int labs(long int j);

Description:

   The labs function is similar to the abs function, except that the
   argument and the returned value each have type long int.


The ldiv function
*****************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         ldiv_t ldiv(long int numer, long int denom);

Description:

   The ldiv function is similar to the div function, except that the
   arguments and the members of the returned structure (which has type
   ldiv_t ) all have type long int.


The mblen function
******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int mblen(const char *s, size_t n);

.. note::

	This function is not implemented!!!


The mbtowc function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int mbtowc(wchar_t *pwc, const char *s, size_t n);

.. note::

	This function is not implemented!!!


The wctomb function
*******************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         int wctomb(char *s, wchar_t wchar);

.. note::

	This function is not implemented!!!


The mbstowcs function
*********************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         size_t mbstowcs(wchar_t *pwcs, const char *s, size_t n);

.. note::

	This function is not implemented!!!


The wcstombs function
*********************

Synopsis:

    .. code-block:: c

         #include <stdlib.h>
         size_t wcstombs(char *s, const wchar_t *pwcs, size_t n);

.. note::

	This function is not implemented!!!

