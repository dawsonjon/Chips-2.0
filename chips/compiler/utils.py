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
