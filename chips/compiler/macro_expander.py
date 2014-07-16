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

def shift_left(allocator, instruction):
    """
    Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    start = unique()
    end = unique()

    counter = allocator.new(4, "shift_counter")
    one = allocator.new(4, "one")

    new_instruction = [
        {
        "op"  : "literal",
        "literal" : 1,
        "dest": one
        },

        {
        "op"  : "literal",
        "literal" : 0x3f,
        "dest": counter
        },

        {
        "op"  : "move",
        "src" : src,
        "dest": dest
        },

        {
        "op"  : "and",
        "src" : srcb,
        "srcb" : counter,
        "dest": counter
        },

        {
        "op"    : "label",
        "label" : start
        },


        {
        "op"    : "jmp_if_false",
        "src"   : counter,
        "label" : end
        },

        {
        "op"  : "shift_left",
        "src" : dest,
        "dest": dest
        },

        {
        "op"   : "subtract",
        "src"  : counter,
        "srcb" : one,
        "dest" : counter
        },


        {
        "op"    : "goto",
        "label" : start
        },


        {
        "op"    : "label",
        "label" : end
        },
    ]
    allocator.free(counter)
    allocator.free(one)

    return new_instruction

def shift_right(allocator, instruction):
    """
    Shift Right (by a programable amount)
    Implemented using 1 bit shifts.
    """
    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    start = unique()
    end = unique()
    counter = allocator.new(4, "shift_counter")
    one = allocator.new(4, "one")
    new_instruction = [
        {
        "op"  : "literal",
        "literal" : 1,
        "dest": one
        },

        {
        "op"  : "literal",
        "literal" : 0x3f,
        "dest": counter
        },

        {
        "op"  : "move",
        "src" : src,
        "dest": dest
        },

        {
        "op"  : "and",
        "src" : srcb,
        "srcb" : counter,
        "dest": counter
        },

        {
        "op"    : "label",
        "label" : start
        },

        {
        "op"    : "jmp_if_false",
        "src"   : counter,
        "label" : end
        },

        {
        "op"  : "shift_right",
        "src" : dest,
        "dest": dest
        },

        {
        "op"   : "subtract",
        "src"  : counter,
        "srcb" : one,
        "dest" : counter
        },


        {
        "op"    : "goto",
        "label" : start
        },

        {
        "op"    : "label",
        "label" : end
        },
    ]
    allocator.free(counter)
    allocator.free(one)

    return new_instruction

def unsigned_shift_right(allocator, instruction):
    """
    Shift Right (by a programable amount)
    Implemented using 1 bit shifts.
    """
    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    start = unique()
    end = unique()
    counter = allocator.new(4, "shift_counter")
    one = allocator.new(4, "one")
    new_instruction = [
        {
        "op"  : "literal",
        "literal" : 1,
        "dest": one
        },

        {
        "op"  : "literal",
        "literal" : 0x3f,
        "dest": counter
        },

        {
        "op"  : "move",
        "src" : src,
        "dest": dest
        },

        {
        "op"  : "and",
        "src" : srcb,
        "srcb" : counter,
        "dest": counter
        },

        {
        "op"    : "label",
        "label" : start
        },

        {
        "op"    : "jmp_if_false",
        "src"   : counter,
        "label" : end
        },

        {
        "op"  : "unsigned_shift_right",
        "src" : dest,
        "dest": dest
        },

        {
        "op"   : "subtract",
        "src"  : counter,
        "srcb" : one,
        "dest" : counter
        },


        {
        "op"    : "goto",
        "label" : start
        },

        {
        "op"    : "label",
        "label" : end
        },
    ]
    allocator.free(counter)
    allocator.free(one)

    return new_instruction

def long_shift_left(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #shift low
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "shift_left",
        },

        #shift high
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "shift_left_with_carry",
        },
    ]

    return new_instruction

def long_shift_right(instruction):

    """Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #shift high
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "shift_right",
        },

        #shift low
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "shift_right_with_carry",
        },
    ]

    return new_instruction

def unsigned_long_shift_right(allocator, instruction):
    """
    Unsigned Long Shift Left (by a programable amount)
    Implemented using 1 bit shifts.
    """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    start = unique()
    end = unique()

    counter = allocator.new(4, "shift_counter")
    one = allocator.new(4, "one")

    new_instruction = [
        {
        "op"  : "literal",
        "literal" : 1,
        "dest": one
        },

        {
        "op"  : "literal",
        "literal" : 0x7f,
        "dest": counter
        },

        {
        "op"  : "move",
        "src" : src,
        "dest": dest
        },

        {
        "op"  : "move",
        "src" : src + 1,
        "dest": dest + 1
        },

        {
        "op"  : "and",
        "src" : srcb,
        "srcb" : counter,
        "dest": counter
        },

        {
        "op"    : "label",
        "label" : start
        },


        {
        "op"    : "jmp_if_false",
        "src"   : counter,
        "label" : end
        },

        {
        "op"  : "unsigned_shift_right",
        "src" : dest + 1,
        "dest": dest + 1
        },

        {
        "op"  : "shift_right_with_carry",
        "src" : dest,
        "dest": dest
        },

        {
        "op"   : "subtract",
        "src"  : counter,
        "srcb" : one,
        "dest" : counter
        },

        {
        "op"    : "goto",
        "label" : start
        },


        {
        "op"    : "label",
        "label" : end
        },
    ]
    allocator.free(counter)
    allocator.free(one)

    return new_instruction

def long_report(allocator, instruction):

    src = instruction["src"]

    new_instruction = [
        {
        "op"  : "load_hi",
        "src" : src + 1,
        "srcb": src + 1,
        },
        instruction,
    ]

    return new_instruction

def unsigned_short_to_long(allocator, instruction):
    """
    Convert a short data type to a long data type
    """

    src = instruction["src"]
    dest = instruction["dest"]
    new_instruction = [
        {
        "op"  : "literal",
        "literal" : 0,
        "dest": dest + 1
        },

        {
        "op"  : "move",
        "src" : src,
        "dest": dest
        },
    ]

    return new_instruction

def long_equal(instruction):
    """ perform equal function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },

        {
        "op"  : "pop_b_lo",
        },

        {
        "op"  : "pop_a_hi",
        },

        {
        "op"  : "pop_a_lo",
        },

        {
        "op"  : "push_a_hi",
        },

        {
        "op"  : "push_b_hi",
        },

        {
        "op"  : "equal",
        },

        {
        "op"  : "push_a_lo",
        },

        {
        "op"  : "push_b_lo",
        },

        {
        "op"  : "equal",
        },

        {
        "op"   : "and",
        },
    ]
    return new_instruction

def long_not_equal(instruction):

    """ perform not_equal function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },

        {
        "op"  : "pop_b_lo",
        },

        {
        "op"  : "pop_a_hi",
        },

        {
        "op"  : "pop_a_lo",
        },

        {
        "op"  : "push_a_hi",
        },

        {
        "op"  : "push_b_hi",
        },

        {
        "op"  : "not_equal",
        },

        {
        "op"  : "push_a_lo",
        },

        {
        "op"  : "push_b_lo",
        },

        {
        "op"  : "not_equal",
        },

        {
        "op"   : "or",
        },
    ]

    return new_instruction

def long_greater(instruction):
    """ perform greater function on long numbers """


    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "greater",
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "equal",
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "unsigned_greater",
        },

        {
        "op"  : "and",
        },
        {
        "op"  : "or",
        },

    ]
    return new_instruction

def unsigned_long_greater(instruction):

    """ perform greater function on long unsigned numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "unsigned_greater",
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "equal",
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "unsigned_greater",
        },
        {
        "op"  : "and",
        },
        {
        "op"  : "or",
        },

    ]
    return new_instruction

def long_greater_equal(instruction):

    """ perform greater function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "greater",
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "equal",
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "unsigned_greater_equal",
        },
        {
        "op"  : "and",
        },
        {
        "op"  : "or",
        },

    ]

    return new_instruction

def unsigned_long_greater_equal(instruction):

    """ perform greater equal function on long unsigned numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb greater?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "unsigned_greater",
        },

        #msb equal?
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "equal",
        },

        #lsb greater?
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "unsigned_greater_equal",
        },
        {
        "op"  : "and",
        },
        {
        "op"  : "or",
        },

    ]
    return new_instruction

def long_and(instruction):

    """ perform and function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "and",
        },

        #lsb
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "and",
        },
    ]
    return new_instruction

def long_or(instruction):

    """ perform or function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "or",
        },

        #lsb
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "or",
        },
    ]

    return new_instruction

def long_xor(instruction):
    """ perform xor function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #msb
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "xor",
        },

        #lsb
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "xor",
        },
    ]

    return new_instruction

def long_not(instruction):
    """ perform not function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "not",
        },
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "not",
        },
    ]
    return new_instruction

def long_add(instruction):
    """ perform add function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #add
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "add",
        },

        #add_with_carry
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "add_with_carry",
        },

    ]

    return new_instruction

def long_subtract(instruction):
    """ perform subtract function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #add
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "subtract",
        },

        #add_with_carry
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "subtract_with_carry",
        },

    ]
    return new_instruction

def long_multiply(instruction):

    """ perform multiply function on long numbers """

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },

        #
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "multiply",
        },
        {
        "op"  : "carry",
        },

        #
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_b_hi",
        },
        {
        "op"  : "multiply",
        },

        #
        {
        "op"  : "push_a_hi",
        },
        {
        "op"  : "push_b_lo",
        },
        {
        "op"  : "multiply",
        },

        {
        "op"  : "add",
        },
        {
        "op"  : "add",
        },

    ]

    return new_instruction

def long_float_add(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "long_float_add",
        },
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_a_hi",
        },

    ]
    return new_instruction

def long_float_subtract(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "long_float_subtract",
        },
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_a_hi",
        },

    ]
    return new_instruction

def long_float_multiply(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "long_float_multiply",
        },
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_a_hi",
        },
    ]
    return new_instruction

def long_float_divide(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_hi",
        },
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_hi",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "long_float_divide",
        },
        {
        "op"  : "push_a_lo",
        },
        {
        "op"  : "push_a_hi",
        },
    ]
    return new_instruction

def float_add(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "float_add",
        },
        {
        "op"  : "push_a_lo",
        },

    ]
    return new_instruction

def float_subtract(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "float_subtract",
        },
        {
        "op"  : "push_a_lo",
        },

    ]
    return new_instruction

def float_multiply(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "float_multiply",
        },
        {
        "op"  : "push_a_lo",
        },
    ]
    return new_instruction

def float_divide(instruction):

    new_instruction = [
        {
        "op"  : "pop_b_lo",
        },
        {
        "op"  : "pop_a_lo",
        },
        {
        "op"  : "float_divide",
        },
        {
        "op"  : "push_a_lo",
        },
    ]

    return new_instruction
