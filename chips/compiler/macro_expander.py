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
        elif instruction["op"] == "float_add":
            new_instructions.extend(float_add(instruction))
        elif instruction["op"] == "float_subtract":
            new_instructions.extend(float_subtract(instruction))
        elif instruction["op"] == "float_multiply":
            new_instructions.extend(float_multiply(instruction))
        elif instruction["op"] == "float_divide":
            new_instructions.extend(float_divide(instruction))
        else:
            new_instructions.append(instruction)

    return new_instructions

def long_shift_left(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    end = unique()

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },


        #shift msb and lsb by up to 32
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_left",
        "pop":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_left_with_carry",
        "pop":True,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal":32,
        },
        {
        "op"  : "greater",
        "pop":True,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "label":end,
        "pop":True,
        },

        #reduce shift amount by 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal": 32,
        },
        {
        "op"  : "subtract",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_left",
        "pop":True,
        },

        #shift high
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_left_with_carry",
        "pop":True,
        },

        {
        "op"  : "label",
        "label":end,
        },
    ]

    return new_instruction

def unsigned_long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },


        #shift msb and lsb by up to 32
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_shift_right",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right_with_carry",
        "pop":True,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal":32,
        },
        {
        "op"  : "greater",
        "pop":True,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "label":end,
        "pop":True,
        },

        #reduce shift amount by 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal": 32,
        },
        {
        "op"  : "subtract",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_shift_right",
        "pop":True,
        },

        #shift high
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right_with_carry",
        "pop":True,
        },

        {
        "op"  : "label",
        "label":end,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
    ]

    return new_instruction

def long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """
    end = unique()

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },


        #shift msb and lsb by up to 32
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right_with_carry",
        "pop":True,
        },

        #if shift amount is less than or equal to 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal":32,
        },
        {
        "op"  : "greater",
        "pop":True,
        "literal":32,
        },
        {
        "op"  : "jmp_if_false",
        "label":end,
        "pop":True,
        },

        #reduce shift amount by 32
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "push_literal",
        "push":True,
        "literal": 32,
        },
        {
        "op"  : "subtract",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },

        #shift msb and lsb again by up to 32
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right",
        "pop":True,
        },

        #shift high
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "shift_right_with_carry",
        "pop":True,
        },

        {
        "op"  : "label",
        "label":end,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
    ]

    return new_instruction

def long_equal(instruction):

    """ perform equal function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },

        {
        "op"  : "pop_b_lo",
        "pop":True,
        },

        {
        "op"  : "pop_a_hi",
        "pop":True,
        },

        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        {
        "op"  : "push_a_hi",
        "push":True,
        },

        {
        "op"  : "push_b_hi",
        "push":True,
        },

        {
        "op"  : "equal",
        "pop":True,
        },

        {
        "op"  : "push_a_lo",
        "push":True,
        },

        {
        "op"  : "push_b_lo",
        "push":True,
        },

        {
        "op"  : "equal",
        "pop":True,
        },

        {
        "op"   : "and",
        "pop":True,
        },
    ]
    return new_instruction

def long_not_equal(instruction):

    """ perform not_equal function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },

        {
        "op"  : "pop_b_lo",
        "pop":True,
        },

        {
        "op"  : "pop_a_hi",
        "pop":True,
        },

        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        {
        "op"  : "push_a_hi",
        "push":True,
        },

        {
        "op"  : "push_b_hi",
        "push":True,
        },

        {
        "op"  : "not_equal",
        "pop":True,
        },

        {
        "op"  : "push_a_lo",
        "push":True,
        },

        {
        "op"  : "push_b_lo",
        "push":True,
        },

        {
        "op"  : "not_equal",
        "pop":True,
        },

        {
        "op"   : "or",
        "pop":True,
        },
    ]

    return new_instruction

def long_greater(instruction):
    """ perform greater function on long numbers """


    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "greater",
        "pop":True,
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "equal",
        "pop":True,
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_greater",
        "pop":True,
        },

        {
        "op"  : "and",
        "pop":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },

    ]
    return new_instruction

def unsigned_long_greater(instruction):

    """ perform greater function on long unsigned numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "unsigned_greater",
        "push":True,
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "equal",
        "pop":True,
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_greater",
        "push":True,
        },
        {
        "op"  : "and",
        "pop":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },

    ]
    return new_instruction

def long_greater_equal(instruction):

    """ perform greater function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "greater",
        "pop":True,
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "equal",
        "pop":True,
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_greater_equal",
        "pop":True,
        },
        {
        "op"  : "and",
        "pop":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },

    ]

    return new_instruction

def unsigned_long_greater_equal(instruction):

    """ perform greater equal function on long unsigned numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "unsigned_greater",
        "pop":True,
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "equal",
        "pop":True,
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "unsigned_greater_equal",
        "pop":True,
        },
        {
        "op"  : "and",
        "pop":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },

    ]
    return new_instruction

def long_and(instruction):

    """ perform and function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "and",
        "pop":True,
        },

        #lsb
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "and",
        "pop":True,
        },
    ]
    return new_instruction

def long_or(instruction):

    """ perform or function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },

        #lsb
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "or",
        "pop":True,
        },
    ]

    return new_instruction

def long_xor(instruction):
    """ perform xor function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #msb
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "xor",
        "pop":True,
        },

        #lsb
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "xor",
        "pop":True,
        },
    ]

    return new_instruction

def long_not(instruction):
    """ perform not function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "not",
        "pop":True,
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "not",
        "pop":True,
        },
    ]
    return new_instruction

def long_add(instruction):
    """ perform add function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #add
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "add",
        "pop":True,
        },

        #add_with_carry
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "add_with_carry",
        "pop":True,
        },

    ]

    return new_instruction

def long_subtract(instruction):
    """ perform subtract function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #add
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "subtract",
        "pop":True,
        },

        #add_with_carry
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "subtract_with_carry",
        "pop":True,
        },

    ]
    return new_instruction

def long_multiply(instruction):

    """ perform multiply function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },

        #
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "multiply",
        "pop":True,
        },
        {
        "op"  : "carry",
        "push":True,
        },

        #
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_b_hi",
        "push":True,
        },
        {
        "op"  : "multiply",
        "pop":True,
        },

        #
        {
        "op"  : "push_a_hi",
        "push":True,
        },
        {
        "op"  : "push_b_lo",
        "push":True,
        },
        {
        "op"  : "multiply",
        "pop":True,
        },

        {
        "op"  : "add",
        "pop":True,
        },
        {
        "op"  : "add",
        "pop":True,
        },

    ]

    return new_instruction

def long_float_add(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "long_float_add",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },

    ]
    return new_instruction

def long_float_subtract(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "long_float_subtract",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },

    ]
    return new_instruction

def long_float_multiply(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "long_float_multiply",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
    ]
    return new_instruction

def long_float_divide(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        "pop":True,
        },
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_hi",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "long_float_divide",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
        {
        "op"  : "push_a_hi",
        "push":True,
        },
    ]
    return new_instruction

def float_add(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "float_add",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },

    ]
    return new_instruction

def float_subtract(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "float_subtract",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },

    ]
    return new_instruction

def float_multiply(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "float_multiply",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
    ]
    return new_instruction

def float_divide(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        "pop":True,
        },
        {
        "op"  : "pop_a_lo",
        "pop":True,
        },
        {
        "op"  : "float_divide",
        },
        {
        "op"  : "push_a_lo",
        "push":True,
        },
    ]

    return new_instruction
