sn = 0
def unique():
    global sn
    label = "macro_" + str(sn)
    sn += 1
    return label

b_hi = 0
b_lo = -1
a_hi = -2
a_lo = -3

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

    thirty_two = 0
    greater_than_32 = 1

    new_instruction = [

        #shift msb and lsb by up to 32
        {
        "op"  : "shift_left",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },
        {
        "op"  : "shift_left_with_carry",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "literal->*tos",
        "a":b_hi,
        "b":b_hi,
        "c":thirty_two,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "greater",
        "a":b_lo,
        "b":b_hi,
        "c":greater_than_32,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "a":greater_than_32,
        "b":greater_than_32,
        "c":b_hi,
        "d":0,
        "label":end,
        },

        #reduce shift amount by 32
        {
        "op"  : "subtract",
        "a":b_lo,
        "b":thirty_two,
        "c":b_lo,
        "d":0,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "shift_left",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":b_hi,
        },
        {
        "op"  : "shift_left_with_carry",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "label",
        "label":end,
        },
        {
        "op"  : "or",
        "a":1,
        "b":1,
        "c":1,
        "d":-2,
        },

    ]

    return new_instruction

def unsigned_long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    thirty_two = 0
    greater_than_32 = 1

    new_instruction = [

        #shift msb and lsb by up to 32
        {
        "op"  : "unsigned_shift_right",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "shift_right_with_carry",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "literal->*tos",
        "a":0,
        "b":0,
        "c":thirty_two,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "greater",
        "a":b_lo,
        "b":thirty_two,
        "c":greater_than_32,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "a":greater_than_32,
        "b":greater_than_32,
        "c":0,
        "d":0,
        "label":end,
        },

        #reduce shift amount by 32
        {
        "op"  : "subtract",
        "a":b_lo,
        "b":thirty_two,
        "c":b_lo,
        "d":0,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "unsigned_shift_right",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "shift_right_with_carry",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },
        {
        "op"  : "label",
        "label":end,
        },
        {
        "op"  : "or",
        "a":0,
        "b":0,
        "c":0,
        "d":-2,
        },
    ]

    return new_instruction

def long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    thirty_two = 0
    greater_than_32 = 1

    new_instruction = [

        #shift msb and lsb by up to 32
        {
        "op"  : "shift_right",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "shift_right_with_carry",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "literal->*tos",
        "a":0,
        "b":0,
        "c":thirty_two,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "greater",
        "a":b_lo,
        "b":thirty_two,
        "c":greater_than_32,
        "d":0,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "a":greater_than_32,
        "b":greater_than_32,
        "c":0,
        "d":0,
        "label":end,
        },

        #reduce shift amount by 32
        {
        "op"  : "subtract",
        "a":b_lo,
        "b":thirty_two,
        "c":b_lo,
        "d":0,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "shift_right",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "shift_right_with_carry",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },
        {
        "op"  : "label",
        "label":end,
        },
        {
        "op"  : "or",
        "a":0,
        "b":0,
        "c":0,
        "d":-2,
        },
    ]

    return new_instruction

def long_equal(instruction):

    """ perform equal function on long numbers """

    new_instruction = [
        {
        "op"  : "equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"    : 0,
        },
        {
        "op"  : "equal",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"    : 0,
        },
        {
        "op"   : "and",
        "a"    : a_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]
    return new_instruction

def long_not_equal(instruction):

    """ perform not_equal function on long numbers """

    new_instruction = [
        {
        "op"  : "not_equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"    : 0,
        },
        {
        "op"  : "not_equal",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"    : 0,
        },
        {
        "op"   : "or",
        "a"    : a_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]

    return new_instruction

def long_greater(instruction):
    """ perform greater function on long numbers """


    new_instruction = [
        {
        "op"  : "unsigned_greater",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"   : 0,
        },
        {
        "op"  : "greater",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : b_lo,
        "d"   : 0,
        },
        {
        "op"  : "equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"  : "and",
        "a"   : a_lo,
        "b"   : a_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"   : "or",
        "a"    : b_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]
    return new_instruction

def unsigned_long_greater(instruction):
    """ perform greater function on long numbers """


    new_instruction = [
        {
        "op"  : "unsigned_greater",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"   : 0,
        },
        {
        "op"  : "unsigned_greater",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : b_lo,
        "d"   : 0,
        },
        {
        "op"  : "equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"  : "and",
        "a"   : a_lo,
        "b"   : a_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"   : "or",
        "a"    : b_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]
    return new_instruction

def long_greater_equal(instruction):

    """ perform greater function on long numbers """

    new_instruction = [
        {
        "op"  : "unsigned_greater_equal",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"   : 0,
        },
        {
        "op"  : "greater",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : b_lo,
        "d"   : 0,
        },
        {
        "op"  : "equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"  : "and",
        "a"   : a_lo,
        "b"   : a_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"   : "or",
        "a"    : b_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]
    return new_instruction

def unsigned_long_greater_equal(instruction):

    """ perform greater equal function on long unsigned numbers """

    new_instruction = [
        {
        "op"  : "unsigned_greater_equal",
        "a"   : a_lo,
        "b"   : b_lo,
        "c"   : a_lo,
        "d"   : 0,
        },
        {
        "op"  : "unsigned_greater",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : b_lo,
        "d"   : 0,
        },
        {
        "op"  : "equal",
        "a"   : a_hi,
        "b"   : b_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"  : "and",
        "a"   : a_lo,
        "b"   : a_hi,
        "c"   : a_hi,
        "d"   : 0,
        },
        {
        "op"   : "or",
        "a"    : b_lo,
        "b"    : a_hi,
        "c"    : a_lo,
        "d"    : -3,
        },
    ]
    return new_instruction

def long_and(instruction):

    """ perform and function on long numbers """

    new_instruction = [
        #msb
        {
        "op"  : "and",
        "a":a_hi,
        "b":b_hi,
        "c":a_hi,
        "d":0,
        },

        #lsb
        {
        "op"  : "and",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":a_hi,
        },
    ]
    return new_instruction

def long_or(instruction):

    """ perform or function on long numbers """

    new_instruction = [
        #msb
        {
        "op"  : "or",
        "a":a_hi,
        "b":b_hi,
        "c":a_hi,
        "d":0,
        },

        #lsb
        {
        "op"  : "or",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":a_hi,
        },
    ]

    return new_instruction

def long_xor(instruction):
    """ perform xor function on long numbers """

    new_instruction = [
        #msb
        {
        "op"  : "xor",
        "a":a_hi,
        "b":b_hi,
        "c":a_hi,
        "d":0,
        },

        #lsb
        {
        "op"  : "xor",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":-2,
        },
    ]

    return new_instruction

def long_not(instruction):
    """ perform not function on long numbers """

    new_instruction = [
        {
        "op"  : "not",
        "a":b_hi,
        "b":b_hi,
        "c":b_hi,
        "d":0,
        },
        {
        "op"  : "not",
        "a":b_lo,
        "b":b_lo,
        "c":b_lo,
        "d":0,
        },
    ]
    return new_instruction

def long_add(instruction):
    """ perform add function on long numbers """

    new_instruction = [
        #add
        {
        "op"  : "add",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        "pop":True,
        },

        #add_with_carry
        {
        "op"  : "add_with_carry",
        "a":a_hi,
        "b":b_hi,
        "c":a_hi,
        "d":a_hi,
        "pop":True,
        },

    ]

    return new_instruction

def long_subtract(instruction):
    """ perform subtract function on long numbers """

    new_instruction = [
        {
        "op"  : "subtract",
        "a":a_lo,
        "b":b_lo,
        "c":a_lo,
        "d":0,
        },

        #add_with_carry
        {
        "op"  : "subtract_with_carry",
        "a":a_hi,
        "b":b_hi,
        "c":a_hi,
        "d":a_hi,
        },

    ]
    return new_instruction

def long_multiply(instruction):

    """ perform multiply function on long numbers """

    new_instruction = [
        {
        "op"  : "multiply",
        "a":b_hi,
        "b":a_lo,
        "c":b_hi,
        "d":0,
        },
        {
        "op"  : "multiply",
        "a":b_lo,
        "b":a_hi,
        "c":a_hi,
        "d":0,
        },
        {
        "op"  : "multiply",
        "a":b_lo,
        "b":a_lo,
        "c":a_lo,
        "d":0,
        },
        {
        "op"  : "carry",
        "a":b_hi,
        "b":b_hi,
        "c":b_lo,
        "d":0,
        },
        {
        "op"  : "add",
        "a":b_lo,
        "b":b_hi,
        "c":b_lo,
        "d":0,
        },
        {
        "op"  : "add",
        "a":a_hi,
        "b":b_lo,
        "c":a_hi,
        "d":a_hi,
        },
    ]

    return new_instruction

def long_float_add(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_b_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "long_float_add",
        "a":0,
        "b":0,
        "c":0,
        "d":0,
        },
        {
        "op"  : "push_a_lo",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
        {
        "op"  : "push_a_hi",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },

    ]
    return new_instruction

def long_float_subtract(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_b_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "long_float_subtract",
        "a":0,
        "b":0,
        "c":0,
        "d":0,
        },
        {
        "op"  : "push_a_lo",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
        {
        "op"  : "push_a_hi",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },

    ]
    return new_instruction

def long_float_multiply(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_b_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "long_float_multiply",
        "a":0,
        "b":0,
        "c":0,
        "d":0,
        },
        {
        "op"  : "push_a_lo",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
        {
        "op"  : "push_a_hi",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
    ]
    return new_instruction

def long_float_divide(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_b_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_hi",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "pop_a_lo",
        "a":0,
        "b":0,
        "c":0,
        "d":-1,
        },
        {
        "op"  : "long_float_divide",
        "a":0,
        "b":0,
        "c":0,
        "d":0,
        },
        {
        "op"  : "push_a_lo",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
        {
        "op"  : "push_a_hi",
        "a":0,
        "b":0,
        "c":1,
        "d":1,
        },
    ]
    return new_instruction
