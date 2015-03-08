__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

def cleanup_functions(instructions):

    """Remove functions that are not called"""


    #This is an iterative processor. Once a function is removed,
    #there may be more unused functions
    while 1:

        #find function calls
        live_functions = {}
        for instruction in instructions:
            if instruction["op"] == "call":
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
