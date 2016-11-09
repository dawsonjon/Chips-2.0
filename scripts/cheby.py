from sympy.mpmath import chebyfit
from math import *

def horner(a, b):
    return "(x *%s +\n %s)"%(a, b) 

polynomial, error = chebyfit(exp, [0.0, 1.0], 11, True)
print "e^x"
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(lambda x:2.0**x, [0.0, 1.0], 11, True)
print "2^x"
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(lambda x: 1+log(x, 2.0), [1.0, 2.0], 3, True)
print "log2(x)"
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(lambda x: sqrt(x), [1.0, 2.0], 8, True)
print "sqrt(x)"
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(lambda x: cos(x), [0, pi/2], 7, True)
print "cos(x)"
print error
print reduce(horner, polynomial)
