from register_map import *
from instruction_utils import *

sn = 0
def unique():
    global sn
    label = "macro_" + str(sn)
    sn += 1
    return label

def push_pop(instructions):

    """substitue push and pop macros with real instructions"""

    new_instructions = []
    i=0
    while i<len(instructions):
        instruction = instructions[i]
        trace = instruction["trace"]
        if i<len(instructions)-1:
            next_instruction = instructions[i+1]
        else:
            #dummy instruction
            next_instruction = {"op"}

        #if instruction["op"] == "push" and next_instruction["op"] == "pop":
            #to = next_instruction["reg"]
            #from_ = instruction["reg"]
            #if to != from_:
                #new_instructions.append({
                    #"op":"addl", 
                    #"literal":0, 
                    #"z":next_instruction["reg"], 
                    #"a":instruction["reg"],
                    #"comment":"pushpop"
                #})
            #i += 1
        if instruction["op"] == "push":
            #push
            new_instructions.append({"trace":trace, "op":"store", "a":tos, "b":instruction["reg"], "comment":"push"})
            new_instructions.append({"trace":trace, "op":"addl", "z":tos, "a":tos, "literal":1})
        elif instruction["op"] == "pop":
            #pop
            new_instructions.append({"trace":trace, "op":"addl", "z":tos, "a":tos, "literal":-1, "comment":"pop"})
            new_instructions.append({"trace":trace, "op":"load", "z":instruction["reg"], "a":tos})
        else:
            new_instructions.append(instruction)
        i+=1

    return new_instructions

def expand_macros(instructions, allocator):
    new_instructions = []
    for instruction in instructions:
        trace = instruction["trace"]
        if instruction["op"] == "long_equal":
            new_instructions.extend(long_equal(trace, instruction))
        elif instruction["op"] == "long_not_equal":
            new_instructions.extend(long_not_equal(trace, instruction))
        elif instruction["op"] == "long_greater":
            new_instructions.extend(long_greater(trace, instruction))
        elif instruction["op"] == "long_greater_equal":
            new_instructions.extend(long_greater_equal(trace, instruction))
        elif instruction["op"] == "unsigned_long_greater":
            new_instructions.extend(unsigned_long_greater(trace, instruction))
        elif instruction["op"] == "unsigned_long_greater_equal":
            new_instructions.extend(unsigned_long_greater_equal(trace, instruction))
        elif instruction["op"] == "long_add":
            new_instructions.extend(long_add(trace, instruction))
        elif instruction["op"] == "long_subtract":
            new_instructions.extend(long_subtract(trace, instruction))
        elif instruction["op"] == "long_multiply":
            new_instructions.extend(long_multiply(trace, instruction))
        elif instruction["op"] == "long_and":
            new_instructions.extend(long_and(trace, instruction))
        elif instruction["op"] == "long_or":
            new_instructions.extend(long_or(trace, instruction))
        elif instruction["op"] == "long_xor":
            new_instructions.extend(long_xor(trace, instruction))
        elif instruction["op"] == "long_shift_left":
            new_instructions.extend(long_shift_left(trace, instruction))
        elif instruction["op"] == "long_shift_right":
            new_instructions.extend(long_shift_right(trace, instruction))
        elif instruction["op"] == "unsigned_long_shift_right":
            new_instructions.extend(unsigned_long_shift_right(trace, instruction))
        elif instruction["op"] == "long_not":
            new_instructions.extend(long_not(trace, instruction))
        elif instruction["op"] == "long_float_add":
            new_instructions.extend(long_float_add(trace, instruction))
        elif instruction["op"] == "long_float_subtract":
            new_instructions.extend(long_float_subtract(trace, instruction))
        elif instruction["op"] == "long_float_multiply":
            new_instructions.extend(long_float_multiply(trace, instruction))
        elif instruction["op"] == "long_float_divide":
            new_instructions.extend(long_float_divide(trace, instruction))
        else:
            new_instructions.append(instruction)

    return push_pop(new_instructions)

def long_shift_left(trace, instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    end = unique()

    instructions = []
    #shift msb and lsb by up to 32
    instructions.append({"trace":trace,"op": "shift_left",            "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace,"op": "shift_left_with_carry", "a":result_hi, "b":result_b, "z":result_hi})

    #if shift amount is less than or equal to 32
    instructions.append({"trace":trace,"op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"trace":trace,"op":"greater",       "a":result_b, "b":thirty_two, "z":greater_than_32})
    instructions.append({"trace":trace,"op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"trace":trace, "op":"subtract",              "a":result_b, "b":thirty_two, "z":result_b})

    #shift msb and lsb again by up to 32
    instructions.append({"trace":trace, "op":"shift_left",            "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace, "op":"shift_left_with_carry", "a":result_hi, "b":result_b, "z":result_hi})
    instructions.append({"trace":trace, "op":"label", "label":end})
    return instructions

def unsigned_long_shift_right(trace, instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    instructions = []
    #shift msb and lsb by up to 32
    instructions.append({"trace":trace, "op": "unsigned_shift_right",   "a":result_hi, "b":result_b, "z":result_hi})
    instructions.append({"trace":trace, "op": "shift_right_with_carry", "a":result, "b":result_b, "z":result})

    #if shift amount is less than or equal to 32
    instructions.append({"trace":trace, "op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"trace":trace, "op":"greater",       "a":result_b, "b":thirty_two, "z":greater_than_32})
    instructions.append({"trace":trace, "op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"trace":trace, "op":"subtract",               "a":result_b, "b":thirty_two, "z":result_b})

    #shift msb and lsb again by up to 32
    instructions.append({"trace":trace, "op":"unsigned_shift_right",   "a":result_hi, "b":result_b, "z":result_hi})
    instructions.append({"trace":trace, "op":"shift_right_with_carry", "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace, "op":"label", "label":end})
    return instructions

def long_shift_right(trace, instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    instructions = []
    #shift msb and lsb by up to 32
    instructions.append({"trace":trace, "op": "shift_right",            "a":result_hi, "b":result_b, "z":result_hi})
    instructions.append({"trace":trace, "op": "shift_right_with_carry", "a":result, "b":result_b, "z":result})

    #if shift amount is less than or equal to 32
    instructions.append({"trace":trace, "op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"trace":trace, "op":"greater",       "a":result_b, "b":thirty_two, "z":greater_than_32})
    instructions.append({"trace":trace, "op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"trace":trace, "op":"subtract",               "a":result_b, "b":thirty_two, "z":result_b})

    #shift msb and lsb again by up to 32
    instructions.append({"trace":trace, "op":"shift_right",            "a":result_hi, "b":result_b, "z":result_hi})
    instructions.append({"trace":trace, "op":"shift_right_with_carry", "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace, "op":"label", "label":end})
    return instructions

def long_equal(trace, instruction):
    """ perform equal function on long numbers """

    instructions = []
    instructions.append({"trace":trace, "op":"equal", "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({"trace":trace, "op":"equal", "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace, "op":"and",   "a":result, "b":result_hi, "z":result})
    return instructions

def long_not_equal(trace, instruction):
    """ perform not_equal function on long numbers """

    instructions = []
    instructions.append({"trace":trace, "op":"not_equal", "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({"trace":trace, "op":"not_equal", "a":result, "b":result_b, "z":result})
    instructions.append({"trace":trace, "op":"or",        "a":result, "b":result_hi, "z":result})
    return instructions

def long_greater(trace, instruction):
    """ perform greater function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "unsigned_greater", "a":result, "b":result_b, "z":result})
    instructions.append({ "trace":trace, "op"  : "greater",          "a":result_hi, "b":result_b_hi, "z":result_b})
    instructions.append({ "trace":trace, "op"  : "equal",            "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "and",              "a":result, "b":result_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"   : "or",              "a":result_b, "b":result_hi, "z":result})
    return instructions

def unsigned_long_greater(trace, instruction):
    """ perform greater function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "unsigned_greater", "a":result, "b":result_b, "z":result})
    instructions.append({ "trace":trace, "op"  : "unsigned_greater", "a":result_hi, "b":result_b_hi, "z":result_b})
    instructions.append({ "trace":trace, "op"  : "equal",            "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "and",              "a":result, "b":result_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "or",               "a":result_b, "b":result_hi, "z":result})
    return instructions

def long_greater_equal(trace, instruction):
    """ perform greater function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "unsigned_greater_equal", "a":result, "b":result_b, "z":result})
    instructions.append({ "trace":trace, "op"  : "greater",                "a":result_hi, "b":result_b_hi, "z":result_b})
    instructions.append({ "trace":trace, "op"  : "equal",                  "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "and",                    "a":result, "b":result_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "or",                     "a":result_b, "b":result_hi, "z":result})
    return instructions

def unsigned_long_greater_equal(trace, instruction):
    """ perform greater equal function on long unsigned numbers """

    instructions = []
    instructions.append({ "trace":trace, "op" : "unsigned_greater_equal", "a":result, "b":result_b, "z":result})
    instructions.append({ "trace":trace, "op" : "unsigned_greater",       "a":result_hi, "b":result_b_hi, "z":result_b})
    instructions.append({ "trace":trace, "op" : "equal",                  "a":result_hi, "b":result_b_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op" : "and",                    "a":result, "b":result_hi, "z":result_hi})
    instructions.append({ "trace":trace, "op"  : "or",                    "a":result_b, "b":result_hi, "z":result})
    return instructions

def long_and(trace, instruction):
    """ perform and function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op":"and", "z":result, "a":result, "b":result_b})
    instructions.append({ "trace":trace, "op":"and", "z":result_hi, "a":result_hi, "b":result_b_hi})
    return instructions

def long_or(trace, instruction):
    """ perform or function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "or", "z":result, "a":result, "b":result_b})
    instructions.append({ "trace":trace, "op"  : "or", "z":result_hi, "a":result_hi, "b":result_b_hi})
    return instructions

def long_xor(trace, instruction):
    """ perform xor function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "xor", "z":result, "a":result, "b":result_b})
    instructions.append({ "trace":trace, "op"  : "xor", "z":result_hi, "a":result_hi, "b":result_b_hi})
    return instructions

def long_not(trace, instruction):
    """ perform not function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op" : "not", "z":result, "a":result})
    instructions.append({ "trace":trace, "op" : "not", "z":result_hi, "a":result_hi})
    return instructions

def long_add(trace, instruction):
    """ perform add function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "add", "z":result, "a":result, "b":result_b})
    instructions.append({ "trace":trace, "op"  : "add_with_carry", "z":result_hi, "a":result_hi, "b":result_b_hi})
    return instructions

def long_subtract(trace, instruction):
    """ perform subtract function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "subtract", "z":result, "a":result, "b":result_b})
    instructions.append({ "trace":trace, "op"  : "subtract_with_carry", "z":result_hi, "a":result_hi, "b":result_b_hi})
    return instructions

def long_multiply(trace, instruction):

    """ perform multiply function on long numbers """

    instructions = []
    instructions.append({ "trace":trace, "op"  : "multiply", "z":result_b_hi, "a":result_b_hi, "b":result})
    instructions.append({ "trace":trace, "op"  : "multiply", "z":result_hi, "a":result_b, "b":result_hi})
    instructions.append({ "trace":trace, "op"  : "multiply", "z":result, "a":result_b, "b":result})
    instructions.append({ "trace":trace, "op"  : "carry", "z":result_b})
    instructions.append({ "trace":trace, "op"  : "add", "z":result_b, "a":result_b, "b":result_b_hi})
    instructions.append({ "trace":trace, "op"  : "add", "z":result_hi, "a":result_hi, "b":result_b})
    return instructions

def long_float_add(trace, instruction):
    instructions = []
    instructions.append({"trace":trace, "op":"b_hi", "z":result_b_hi, "a":result_b_hi})
    instructions.append({"trace":trace, "op":"b_lo", "z":result_b, "a":result_b})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"long_float_add"})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    return instructions

def long_float_subtract(trace, instruction):
    instructions = []
    instructions.append({"trace":trace, "op":"b_hi", "z":result_b_hi, "a":result_b_hi})
    instructions.append({"trace":trace, "op":"b_lo", "z":result_b, "a":result_b})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"long_float_subtract"})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    return instructions

def long_float_multiply(trace, instruction):
    instructions = []
    instructions.append({"trace":trace, "op":"b_hi", "z":result_b_hi, "a":result_b_hi})
    instructions.append({"trace":trace, "op":"b_lo", "z":result_b, "a":result_b})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"long_float_multiply"})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    return instructions

def long_float_divide(trace, instruction):
    instructions = []
    instructions.append({"trace":trace, "op":"b_hi", "z":result_b_hi, "a":result_b_hi})
    instructions.append({"trace":trace, "op":"b_lo", "z":result_b, "a":result_b})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"long_float_divide"})
    instructions.append({"trace":trace, "op":"a_lo", "z":result, "a":result})
    instructions.append({"trace":trace, "op":"a_hi", "z":result_hi, "a":result_hi})
    return instructions
