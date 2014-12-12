__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

from register_map import *

def push(instructions, reg):
    """Push the content of *reg(* onto the stack"""
    instructions.append({"op":"push", "reg":reg})
    return instructions

def pop(instructions, reg):
    """Pop one item off the stack into reg"""
    instructions.append({"op":"pop", "reg":reg})
    return instructions

def store_object(instructions, n, offset, local, leave_on_stack=False):
    """Store an item into the specified location
    if n = 1 the item is taken from the result register
    if n = 2 the item is taken from result and result_hi register
    if n > 2 the item is taken from the stack
    if local is true, the location is assumed to be relative to the frame register
    if offset is not specified, assume that address is in address
    if leave_on_stack is true the item is coppied to the specified location, but left on the stack.
    if the item was not on the stack in the first place, the value is left in the result registers either way.
    """
    if offset is not None:
        if local:
            instructions.append({"op":"addl", "z":address, "a":frame, "literal":offset})
        else:
            instructions.append({"op":"literal", "z":address, "literal":offset})
    if n == 1:
        instructions.append({"op":"store", "b":result, "a":address})
    elif n == 2:
        instructions.append({"op":"store", "b":result, "a":address})
        instructions.append({"op":"addl", "z":address, "a":address, "literal":1})
        instructions.append({"op":"store", "b":result_hi, "a":address})
    else:
        instructions.append({"op":"addl", "z":address, "a":address, "literal":n-1})
        if leave_on_stack:
            instructions.append({"op":"addl", "z":tos_copy, "a":tos, "literal":0})
            for i in range(n):
                instructions.append({"op":"addl", "z":tos_copy, "a":tos_copy, "literal":-1})
                instructions.append({"op":"load", "z":result, "a":tos_copy})
                instructions.append({"op":"store", "b":result, "a":address})
                if i < n-1:
                    instructions.append({"op":"addl", "z":address, "a":address, "literal":-1})
        else:
            for i in range(n):
                pop(instructions, result)
                instructions.append({"op":"store", "b":result, "a":address})
                if i < n-1:
                    instructions.append({"op":"addl", "z":address, "a":address, "literal":-1})
    return instructions

def load_object(instructions, n, offset, local):
    """Load an item into the specified location
    if n = 1 the item is taken from the result register
    if n = 2 the item is taken from result and result_hi register
    if n > 2 the item is taken from the stack
    if local is true, the location is assumed to be relative to the frame register
    if offset is not specified, assume that address is in result
    """
    if offset is not None:
        if local:
            instructions.append({"op":"addl", "z":address, "a":frame, "literal":offset})
        else:
            instructions.append({"op":"literal", "z":address, "literal":offset})
    else:
        instructions.append({"op":"addl", "z":address, "a":result, "literal":0})
    if n == 1:
        instructions.append({"op":"load", "z":result, "a":address})
    elif n == 2:
        instructions.append({"op":"load", "z":result, "a":address})
        instructions.append({"op":"addl", "z":address, "a":address, "literal":1})
        instructions.append({"op":"load", "z":result_hi, "a":address})
    else:
        for i in range(n):
            instructions.append({"op":"load", "z":result, "a":address})
            if i < n-1:
                instructions.append({"op":"addl", "z":address, "a":address, "literal":1})
            push(instructions, result)
    return instructions

def call(instructions, label):
    instructions.append({"op":"addl", "z":return_frame, "a":frame, "literal":0})
    instructions.append({"op":"addl", "z":frame, "a":tos, "literal":0})
    instructions.append({"op":"call", "z":return_address, "label":label})
    return instructions

def _return(instructions):
    instructions.append({"op":"addl", "z":tos, "a":frame, "literal":0})
    instructions.append({"op":"addl", "z":frame, "a":return_frame, "literal":0})
    instructions.append({"op":"return", "a":return_address})
    return instructions
