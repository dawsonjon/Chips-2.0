__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

from register_map import *

def push(instructions, reg):
    instructions.append({"op":"store", "a":tos, "b":reg})
    instructions.append({"op":"addl", "z":tos, "a":tos, "literal":1})
    return instructions

def pop(instructions, reg):
    instructions.append({"op":"addl", "z":tos, "a":tos, "literal":-1})
    instructions.append({"op":"load", "z":reg, "a":tos})
    return instructions

def pop_object(instructions, n, leave_on_stack):
    pop(instructions, obj)
    instructions.append({"op":"addl", "z":obj, "a":obj, "literal":n-1})
    if leave_on_stack:
        instructions.append({"op":"addl", "z":tos_copy, "a":tos, "literal":0})
    for i in range(n):
        if leave_on_stack:
            instructions.append({"op":"addl", "z":tos_copy, "a":tos_copy, "literal":-1})
            instructions.append({"op":"load", "z":temp, "a":tos_copy})
        else:
            pop(instructions, temp)
        instructions.append({"op":"store", "a":obj, "b":temp})
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":-1})
    return instructions

def push_object(instructions, n):
    pop(instructions, obj)
    for i in range(n):
        instructions.append({"op":"load", "z":temp, "a":obj})
        push(instructions, temp)
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":1})
    return instructions

def pop_global(instructions, n, offset):
    instructions.append({"op":"literal", "z":obj, "literal":offset+n-1})
    for i in range(n):
        pop(instructions, temp)
        instructions.append({"op":"store", "a":obj, "b":temp})
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":-1})
    return instructions

def push_global(instructions, n, offset):
    instructions.append({"op":"literal", "z":obj, "literal":offset})
    for i in range(n):
        instructions.append({"op":"load", "z":temp, "a":obj})
        push(instructions, temp)
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":1})
    return instructions

def pop_local(instructions, n, offset):
    instructions.append({"op":"literal", "z":obj, "literal":offset+n-1})
    instructions.append({"op":"add", "z":obj, "a":obj, "b":frame})
    for i in range(n):
        pop(instructions, temp)
        instructions.append({"op":"store", "a":obj, "b":temp})
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":-1})
    return instructions

def push_local(instructions, n, offset):
    instructions.append({"op":"literal", "z":obj, "literal":offset})
    instructions.append({"op":"add", "z":obj, "a":obj, "b":frame})
    for i in range(n):
        instructions.append({"op":"load", "z":temp, "a":obj})
        push(instructions, temp)
        instructions.append({"op":"addl", "z":obj, "a":obj, "literal":1})
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
