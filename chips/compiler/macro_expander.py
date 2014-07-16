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
        elif instruction["op"] == "long_greater":
            new_instructions.extend(long_greater(instruction))
        elif instruction["op"] == "long_add":
            new_instructions.extend(long_add(instruction))
        elif instruction["op"] == "long_subtract":
            new_instructions.extend(long_subtract(instruction))
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

def long_shift_left(allocator, instruction):
    """
    Long Shift Left (by a programable amount)
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
        "op"  : "shift_left",
        "src" : dest,
        "dest": dest
        },

        {
        "op"  : "shift_left_with_carry",
        "src" : dest + 1,
        "dest": dest + 1
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

def long_shift_right(allocator, instruction):
    """
    Long Shift Left (by a programable amount)
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
        "op"  : "shift_right",
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

def long_not_equal(allocator, instruction):
    """ perform not_equal function on long numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    temp = allocator.new(4, "macro_temp")
    new_instruction = [
        {
        "op"  : "not_equal",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        {
        "op"  : "not_equal",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": temp
        },

        {
        "op"   : "or",
        "src"  : temp,
        "srcb" : dest,
        "dest" : dest
        },
    ]
    allocator.free(temp)
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
        "op"  : "greater",
        },

        {
        "op"  : "and",
        },
        {
        "op"  : "or",
        },

    ]
    return new_instruction

def unsigned_long_greater(allocator, instruction):

    """ perform greater function on long unsigned numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    end = unique()

    new_instruction = [
        #msb greater?
        {
        "op"  : "unsigned_greater",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest
        },

        #return true
        {
        "op"  : "jmp_if_true",
        "src" : dest,
        "label": end
        },

        #msb equal?
        {
        "op"  : "equal",
        "src" : srcb + 1,
        "srcb" : src + 1,
        "dest": dest
        },

        #return flase if not
        {
        "op"  : "jmp_if_false",
        "src" : dest,
        "label":end
        },

        #lsb greater?
        {
        "op"  : "unsigned_greater",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        #end
        {
        "op"   : "label",
        "label" : end
        },

    ]
    return new_instruction

def long_greater_equal(allocator, instruction):
    """ perform greater function on long numbers """


    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    end = unique()

    new_instruction = [
        #msb greater?
        {
        "op"  : "greater",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest
        },

        #return true
        {
        "op"  : "jmp_if_true",
        "src" : dest,
        "label": end
        },

        #msb equal?
        {
        "op"  : "equal",
        "src" : srcb + 1,
        "srcb" : src + 1,
        "dest": dest
        },

        #return flase if not
        {
        "op"  : "jmp_if_false",
        "src" : dest,
        "label":end
        },

        #lsb greater?
        {
        "op"  : "unsigned_greater_equal",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        #end
        {
        "op"   : "label",
        "label" : end
        },

    ]
    return new_instruction

def unsigned_long_greater_equal(allocator, instruction):
    """ perform greater equal function on long unsigned numbers """


    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    end = unique()

    new_instruction = [
        #msb greater?
        {
        "op"  : "unsigned_greater",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest
        },

        #return true
        {
        "op"  : "jmp_if_true",
        "src" : dest,
        "label": end
        },

        #msb equal?
        {
        "op"  : "equal",
        "src" : srcb + 1,
        "srcb" : src + 1,
        "dest": dest
        },

        #return flase if not
        {
        "op"  : "jmp_if_false",
        "src" : dest,
        "label":end
        },

        #lsb greater?
        {
        "op"  : "unsigned_greater_equal",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        #end
        {
        "op"   : "label",
        "label" : end
        },

    ]
    return new_instruction

def long_and(allocator, instruction):
    """ perform and function on long numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    new_instruction = [
        {
        "op"  : "and",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        {
        "op"  : "and",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest + 1
        },
    ]
    return new_instruction

def long_or(allocator, instruction):
    """ perform or function on long numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    new_instruction = [
        {
        "op"  : "or",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        {
        "op"  : "or",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest + 1
        },
    ]
    return new_instruction

def long_xor(allocator, instruction):
    """ perform xor function on long numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]
    new_instruction = [
        {
        "op"  : "xor",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        {
        "op"  : "xor",
        "src" : src + 1,
        "srcb" : srcb + 1,
        "dest": dest + 1
        },
    ]
    return new_instruction

def long_not(allocator, instruction):
    """ perform not function on long numbers """

    src = instruction["src"]
    dest = instruction["dest"]
    new_instruction = [
        {
        "op"  : "not",
        "src" : src,
        "dest": dest
        },

        {
        "op"  : "not",
        "src" : src + 1,
        "dest": dest + 1
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

def long_multiply(allocator, instruction):
    """ perform multiply function on long numbers """

    src = instruction["src"]
    srcb = instruction["srcb"]
    dest = instruction["dest"]

    temp = allocator.new(4, "result_hi")

    new_instruction = [

        {
        "op"  : "multiply",
        "src" : src,
        "srcb" : srcb,
        "dest": dest
        },

        {
        "op"  : "result_hi",
        "dest": dest + 1
        },

        {
        "op"  : "multiply",
        "src" : src,
        "srcb" : srcb + 1,
        "dest": temp
        },

        {
        "op"  : "add",
        "src" : dest + 1,
        "srcb" : temp,
        "dest": dest + 1
        },

        {
        "op"  : "multiply",
        "src" : src + 1,
        "srcb" : srcb,
        "dest": temp
        },

        {
        "op"  : "add",
        "src" : dest + 1,
        "srcb" : temp,
        "dest": dest + 1
        },

    ]

    allocator.free(temp);

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
