from numpy import uint32
from numpy import int32
from numpy import uint64
import struct


def calculate_jumps(instructions):
    """change symbolic labels into numeric addresses"""

    # calculate the values of jump locations
    location = 0
    labels = {}
    new_instructions = []
    for instruction in instructions:
        if instruction["op"] == "label":
            labels[instruction["label"]] = location
        else:
            new_instructions.append(instruction)
            location += 1
    instructions = new_instructions

    # substitute real values for labeled jump locations
    for instruction in instructions:
        if "label" in instruction:
            instruction["label"] = labels[instruction["label"]]

    return instructions


def float_to_bits(f):
    """
    Convert a floating point number into an integer containing the ieee 754
    representation.
    """

    value = 0
    for byte in struct.pack(">f", f):
        value <<= 8
        value |= ord(byte)
    return uint32(value)


def double_to_bits(f):
    """
    Convert a double precision floating point number into a 64 bit integer
    containing the ieee 754 representation.
    """

    value = 0
    for byte in struct.pack(">d", f):
        value <<= 8
        value |= ord(byte)
    return uint64(value)


def bits_to_float(bits):
    """
    Convert integer containing the ieee 754 representation into a float.
    """

    byte_string = (
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">f", byte_string)[0]


def bits_to_double(bits):
    """
    Convert integer containing the ieee 754 representation into a float.
    """

    bits = int(bits)
    byte_string = (
        chr((bits & 0xff00000000000000) >> 56) +
        chr((bits & 0xff000000000000) >> 48) +
        chr((bits & 0xff0000000000) >> 40) +
        chr((bits & 0xff00000000) >> 32) +
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">d", byte_string)[0]


def join_words(hi, lo):
    """join two 32 bit words into a 64 bit word"""

    return uint64((int(hi) << 32) | (int(lo) & 0xffffffff))


def split_word(lw):
    """split a 64 bit words into two 32 bit words"""

    return int32(int(lw) >> 32), int32(int(lw) & 0xffffffff)
