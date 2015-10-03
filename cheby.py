from sympy.mpmath import chebyfit
from math import *

def horner(a, b):
    return "(x *%s +\n %s)"%(a, b) 

polynomial, error = chebyfit(exp, [0.0, 1.0], 11, True)
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(lambda x:2.0**x, [0.0, 1.0], 11, True)
print error
print reduce(horner, polynomial)

polynomial, error = chebyfit(log, [0.0, 1000], 11, True)
print error
print reduce(horner, polynomial)
