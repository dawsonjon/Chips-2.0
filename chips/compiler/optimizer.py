__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

def cleanup_functions(instructions):

    """Remove functions that are not called"""


    #This is an iterative processr. Once a function is removed,
    #there may be more unused functions
    while 1:

        #find function calls
        live_functions = {}
        for instruction in instructions:
            if instruction["op"] == "jmp_and_link":
                if instruction["label"].startswith("function"):
                    live_functions[instruction["label"]] = None

        #remove instructions without function calls
        kept_instructions = []
        generate_on = True
        for instruction in instructions:
            if instruction["op"] == "label":
                if instruction["label"].startswith("function"):
                    if instruction["label"] in live_functions:
                        generate_on = True
                    else:
                        generate_on = False
            if generate_on:
                kept_instructions.append(instruction)

        if len(instructions) == len(kept_instructions):
            return kept_instructions
        instructions = kept_instructions

def reallocate_registers(instructions, registers):

    register_map = {}
    new_registers = {}
    n = 0
    for register in sorted(registers.keys()):
        definition = registers[register]
        register_map[register] = n
        new_registers[n] = definition
        n+=1

    for instruction in instructions:
        if "dest" in instruction:
            instruction["dest"] = register_map[instruction["dest"]]
        if "src" in instruction:
            instruction["src"] = register_map[instruction["src"]]
        if "srcb" in instruction:
            instruction["srcb"] = register_map[instruction["srcb"]]

    return instructions, new_registers

def cleanup_registers(instructions, registers):

    #find all the registers that are read from.
    used_registers = {}
    for instruction in instructions:
        if "src" in instruction:
            used_registers[instruction["src"]] = None
        if "srcb" in instruction:
            used_registers[instruction["srcb"]] = None

    #remove them from the list of allocated registers
    kept_registers = {}
    for register, description in registers.iteritems():
        if register in used_registers:
            kept_registers[register] = description

    #remove all instructions that read from unused registers
    kept_instructions = []
    for instruction in instructions:
        if "dest" in instruction:
            if instruction["dest"] in kept_registers:
                kept_instructions.append(instruction)
        else:
            kept_instructions.append(instruction)

    return reallocate_registers(kept_instructions, kept_registers)
