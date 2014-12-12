temp = 0 
temp1 = 1 
address = 2 
tos = 3 
frame = 4 
tos_copy = 5 
return_address = 6 
return_frame = 7 
result = 8
result_hi = 9
result_b = 10
result_b_hi = 11
thirty_two = 12
greater_than_32 = 13

regmap = {
    "temp" : 0 ,
    "temp1" : 1 ,
    "address" : 2 ,
    "tos" : 3 ,
    "frame" : 4 ,
    "tos_copy" : 5 ,
    "return_address" : 6 ,
    "return_frame" : 7 ,
    "result" : 8,
    "result_hi" : 9,
    "result_b" : 10,
    "result_b_hi" : 11,
    "thirty_two" : 12,
    "greater_than_32" : 13,
}
rregmap = dict((j, i) for i, j in regmap.iteritems())
