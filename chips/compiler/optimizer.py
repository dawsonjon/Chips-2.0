__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

def parallelise(instructions):

  def modifies_register(instruction):

    """Return the register modified by this instruction if any"""

    if "dest" in instruction:
      return instruction["dest"]
    return None

  def uses_registers(instruction):

    """Return the registers used by this instruction if any"""

    registers = []
    for field in ["src", "srcb"]:
      if field in instruction:
        registers.append(instruction[field])
    return registers

  def accesses_memory(instruction):

    """Return the array modified by this instruction if any"""

    return instruction["op"] in ["memory_write", "memory_read_request", "memory_read"]

  def is_solitary(instruction):

    """Return True if an instruction cannot be executed in parallel with other instructions"""

    return instruction["op"] in ["read", "write", "ready", "label"]

  def is_jump(instruction):

    """Return True if an instruction contains a branch or jump"""

    return instruction["op"] in ["goto", "jmp_if_true", "jmp_if_false", "jmp_and_link",
                                 "jmp_to_reg"]

  def is_dependent(instruction, frame, preceding):

    """determine whether an instruction is dependent on the outcome of:
    - an instruction within the current frame
    - preceding instructions not within the frame """

    for i in frame + preceding:
      if modifies_register(i) is not None:
        if modifies_register(i) in uses_registers(instruction):
          return True
        if modifies_register(i) == modifies_register(instruction):
          return True
      if accesses_memory(i) and accesses_memory(instruction):
          return True
      if is_jump(i):
        return True
    for i in preceding:
      if modifies_register(instruction) is not None:
        if modifies_register(instruction) in uses_registers(i):
          return True
      if accesses_memory(i) and accesses_memory(instruction):
          return True
    if is_jump(instruction) and preceding:
      return True
    return False

  def add_instructions(frame, instructions):

    """Add more instructions to the current frame if dependencies allow."""

    instructions_added = True
    while instructions_added:
      instructions_added = False
      for index, instruction in enumerate(instructions):
        if is_solitary(instruction):
          return
        for i in frame:
          if is_jump(i):
            return
          if is_solitary(i):
            return
        if not is_dependent(instruction, frame, instructions[:index]):
          frame.append(instructions.pop(index))
          instructions_added = True
          break

  frames = []
  while instructions:
    frame = [instructions.pop(0)]
    add_instructions(frame, instructions)
    frames.append(frame)
  return frames
