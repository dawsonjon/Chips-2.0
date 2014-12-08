from register_map import *
from instruction_utils import *

sn = 0
def unique():
    global sn
    label = "macro_" + str(sn)
    sn += 1
    return label

def expand_macros(instructions, allocator):
    new_instructions = []
    for instruction in instructions:
        if instruction["op"] == "long_equal":
            new_instructions.extend(long_equal(instruction))
        elif instruction["op"] == "long_not_equal":
            new_instructions.extend(long_not_equal(instruction))
        elif instruction["op"] == "long_greater":
            new_instructions.extend(long_greater(instruction))
        elif instruction["op"] == "long_greater_equal":
            new_instructions.extend(long_greater_equal(instruction))
        elif instruction["op"] == "unsigned_long_greater":
            new_instructions.extend(unsigned_long_greater(instruction))
        elif instruction["op"] == "unsigned_long_greater_equal":
            new_instructions.extend(unsigned_long_greater_equal(instruction))
        elif instruction["op"] == "long_add":
            new_instructions.extend(long_add(instruction))
        elif instruction["op"] == "long_subtract":
            new_instructions.extend(long_subtract(instruction))
        elif instruction["op"] == "long_multiply":
            new_instructions.extend(long_multiply(instruction))
        elif instruction["op"] == "long_and":
            new_instructions.extend(long_and(instruction))
        elif instruction["op"] == "long_or":
            new_instructions.extend(long_or(instruction))
        elif instruction["op"] == "long_xor":
            new_instructions.extend(long_xor(instruction))
        elif instruction["op"] == "long_shift_left":
            new_instructions.extend(long_shift_left(instruction))
        elif instruction["op"] == "long_shift_right":
            new_instructions.extend(long_shift_right(instruction))
        elif instruction["op"] == "unsigned_long_shift_right":
            new_instructions.extend(unsigned_long_shift_right(instruction))
        elif instruction["op"] == "long_not":
            new_instructions.extend(long_not(instruction))
        elif instruction["op"] == "long_float_add":
            new_instructions.extend(long_float_add(instruction))
        elif instruction["op"] == "long_float_subtract":
            new_instructions.extend(long_float_subtract(instruction))
        elif instruction["op"] == "long_float_multiply":
            new_instructions.extend(long_float_multiply(instruction))
        elif instruction["op"] == "long_float_divide":
            new_instructions.extend(long_float_divide(instruction))
        else:
            new_instructions.append(instruction)

    return new_instructions

def long_shift_left(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    end = unique()

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    #shift msb and lsb by up to 32
    instructions.append({"op": "shift_left",            "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op": "shift_left_with_carry", "a":a_hi, "b":b_lo, "z":a_hi})

    #if shift amount is less than or equal to 32
    instructions.append({"op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"op":"greater",       "a":b_lo, "b":thirty_two, "z":greater_than_32})
    instructions.append({"op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"op":"subtract",              "a":b_lo, "b":thirty_two, "z":b_lo})

    #shift msb and lsb again by up to 32
    instructions.append({"op":"shift_left",            "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op":"shift_left_with_carry", "a":a_hi, "b":b_lo, "z":a_hi})
    instructions.append({"op":"label", "label":end})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def unsigned_long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    #shift msb and lsb by up to 32
    instructions.append({"op": "unsigned_shift_right",   "a":a_hi, "b":b_lo, "z":a_hi})
    instructions.append({"op": "shift_right_with_carry", "a":a_lo, "b":b_lo, "z":a_lo})

    #if shift amount is less than or equal to 32
    instructions.append({"op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"op":"greater",       "a":b_lo, "b":thirty_two, "z":greater_than_32})
    instructions.append({"op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"op":"subtract",               "a":b_lo, "b":thirty_two, "z":b_lo})

    #shift msb and lsb again by up to 32
    instructions.append({"op":"unsigned_shift_right",   "a":a_hi, "b":b_lo, "z":a_hi})
    instructions.append({"op":"shift_right_with_carry", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op":"label", "label":end})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    #shift msb and lsb by up to 32
    instructions.append({"op": "shift_right",            "a":a_hi, "b":b_lo, "z":a_hi})
    instructions.append({"op": "shift_right_with_carry", "a":a_lo, "b":b_lo, "z":a_lo})

    #if shift amount is less than or equal to 32
    instructions.append({"op":"literal", "z":thirty_two, "literal":32})
    instructions.append({"op":"greater",       "a":b_lo, "b":thirty_two, "z":greater_than_32})
    instructions.append({"op":"jmp_if_false",  "a":greater_than_32, "label":end})

    #reduce shift amount by 32
    instructions.append({"op":"subtract",               "a":b_lo, "b":thirty_two, "z":b_lo})

    #shift msb and lsb again by up to 32
    instructions.append({"op":"shift_right",            "a":a_hi, "b":b_lo, "z":a_hi})
    instructions.append({"op":"shift_right_with_carry", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op":"label", "label":end})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_equal(instruction):
    """ perform equal function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({"op":"equal", "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({"op":"equal", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op":"and",   "a":a_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def long_not_equal(instruction):
    """ perform not_equal function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({"op":"not_equal", "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({"op":"not_equal", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({"op":"or",        "a":a_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def long_greater(instruction):
    """ perform greater function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "unsigned_greater", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({ "op"  : "greater",          "a":a_hi, "b":b_hi, "z":b_lo})
    instructions.append({ "op"  : "equal",            "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({ "op"  : "and",              "a":a_lo, "b":a_hi, "z":a_hi})
    instructions.append({ "op"   : "or",              "a":b_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def unsigned_long_greater(instruction):
    """ perform greater function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "unsigned_greater", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({ "op"  : "unsigned_greater", "a":a_hi, "b":b_hi, "z":b_lo})
    instructions.append({ "op"  : "equal",            "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({ "op"  : "and",              "a":a_lo, "b":a_hi, "z":a_hi})
    instructions.append({ "op"  : "or",               "a":b_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def long_greater_equal(instruction):
    """ perform greater function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "unsigned_greater_equal", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({ "op"  : "greater",                "a":a_hi, "b":b_hi, "z":b_lo})
    instructions.append({ "op"  : "equal",                  "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({ "op"  : "and",                    "a":a_lo, "b":a_hi, "z":a_hi})
    instructions.append({ "op"  : "or",                     "a":b_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def unsigned_long_greater_equal(instruction):
    """ perform greater equal function on long unsigned numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op" : "unsigned_greater_equal", "a":a_lo, "b":b_lo, "z":a_lo})
    instructions.append({ "op" : "unsigned_greater",       "a":a_hi, "b":b_hi, "z":b_lo})
    instructions.append({ "op" : "equal",                  "a":a_hi, "b":b_hi, "z":a_hi})
    instructions.append({ "op" : "and",                    "a":a_lo, "b":a_hi, "z":a_hi})
    instructions.append({ "op"  : "or",                    "a":b_lo, "b":a_hi, "z":a_lo})
    push(instructions, a_lo)
    return instructions

def long_and(instruction):
    """ perform and function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op":"and", "z":a_lo, "a":a_lo, "b":b_lo})
    instructions.append({ "op":"and", "z":a_hi, "a":a_hi, "b":b_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_or(instruction):
    """ perform or function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "or", "z":a_lo, "a":a_lo, "b":b_lo})
    instructions.append({ "op"  : "or", "z":a_hi, "a":a_hi, "b":b_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_xor(instruction):
    """ perform xor function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "xor", "z":a_lo, "a":a_lo, "b":b_lo})
    instructions.append({ "op"  : "xor", "z":a_hi, "a":a_hi, "b":b_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_not(instruction):
    """ perform not function on long numbers """

    instructions = []
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op" : "not", "z":a_lo, "a":a_lo})
    instructions.append({ "op" : "not", "z":a_hi, "a":a_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_add(instruction):
    """ perform add function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "add", "z":a_lo, "a":a_lo, "b":b_lo})
    instructions.append({ "op"  : "add_with_carry", "z":a_hi, "a":a_hi, "b":b_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_subtract(instruction):
    """ perform subtract function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "subtract", "z":a_lo, "a":a_lo, "b":b_lo})
    instructions.append({ "op"  : "subtract_with_carry", "z":a_hi, "a":a_hi, "b":b_hi})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_multiply(instruction):

    """ perform multiply function on long numbers """

    instructions = []
    pop(instructions, b_hi)
    pop(instructions, b_lo)
    pop(instructions, a_hi)
    pop(instructions, a_lo)
    instructions.append({ "op"  : "multiply", "z":b_hi, "a":b_hi, "b":a_lo})
    instructions.append({ "op"  : "multiply", "z":a_hi, "a":b_lo, "b":a_hi})
    instructions.append({ "op"  : "multiply", "z":a_lo, "a":b_lo, "b":a_lo})
    instructions.append({ "op"  : "carry", "z":b_lo})
    instructions.append({ "op"  : "add", "z":b_lo, "a":b_lo, "b":b_hi})
    instructions.append({ "op"  : "add", "z":a_hi, "a":a_hi, "b":b_lo})
    push(instructions, a_lo)
    push(instructions, a_hi)
    return instructions

def long_float_add(instruction):
    instructions = []
    pop(instructions, temp)
    instructions.append({"op":"b_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"b_lo", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    instructions.append({"op":"long_float_add"})
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    push(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    push(instructions, temp)
    return instructions

def long_float_subtract(instruction):
    instructions = []
    pop(instructions, temp)
    instructions.append({"op":"b_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"b_lo", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    instructions.append({"op":"long_float_subtract"})
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    push(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    push(instructions, temp)
    return instructions

def long_float_multiply(instruction):
    instructions = []
    pop(instructions, temp)
    instructions.append({"op":"b_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"b_lo", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    instructions.append({"op":"long_float_multiply"})
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    push(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    push(instructions, temp)
    return instructions

def long_float_divide(instruction):
    instructions = []
    pop(instructions, temp)
    instructions.append({"op":"b_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"b_lo", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    pop(instructions, temp)
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    instructions.append({"op":"long_float_divide"})
    instructions.append({"op":"a_lo", "z":temp, "a":temp})
    push(instructions, temp)
    instructions.append({"op":"a_hi", "z":temp, "a":temp})
    push(instructions, temp)
    return instructions
