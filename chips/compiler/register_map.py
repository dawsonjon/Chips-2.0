temp = 0 
temp1 = 1 
temp2 = 2 
obj = 3 
tos = 4 
frame = 5 
tos_copy = 6 
return_address = 7 
return_frame = 8 
a_hi = 9
b_hi = 10
a_lo = 11
b_lo = 12
thirty_two = 13
greater_than_32 = 14

regmap = {
    "temp" : 0 ,
    "temp1" : 1 ,
    "temp2" : 2 ,
    "obj" : 3 ,
    "tos" : 4 ,
    "frame" : 5 ,
    "tos_copy" : 6 ,
    "return_address" : 7 ,
    "return_frame" : 8 ,
    "a_hi" : 9,
    "b_hi" : 10,
    "a_lo" : 11,
    "b_lo" : 12,
    "thirty_two" : 13,
    "greater_than_32" : 14,
}
rregmap = dict((j, i) for i, j in regmap.iteritems())
