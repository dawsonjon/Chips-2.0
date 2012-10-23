#!/usr/bin/env python
"""A C to VHDL compiler"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import sys
import os

#Helper functions
####################################################################################################
class C2VHDLError(Exception):
    def __init__(self, message, filename=None, lineno=None):
        self.message = message
        self.filename = os.path.abspath(filename)
        self.lineno = lineno
        

def unique(l):

  """In the absence of set in older python implementations, make list values unique"""

  return dict(zip(l, l)).keys()

class NotConstant(Exception):
  pass

def value(expression):

  """If an expression can be evaluated at compile time, return the value"""

  if hasattr(expression, "value"):
    return truncate(expression.value())
  else:
    raise NotConstant

def constant_fold(expression):

  """Replace an expression with a constant if possible"""

  try:
    return Constant(value(expression))
  except NotConstant:
    return expression

def truncate(number):

  """Truncate arithmetic results to the target number of bits"""

  sign = number & 0x10000
  number = number & 0xffff
  if sign:
    number =  ~0xffff | number
  return number

#Lexical Scanner
####################################################################################################
class Tokens:

  """Break the input file into a stream of tokens, provide functions to traverse the stream."""

  def __init__(self, filename):
    self.tokens = []
    self.filename = None
    self.lineno = None
    self.scan(filename)

  def scan(self, filename):
    try:
      input_file = open(filename)    
    except IOError:
      raise C2VHDLError("Cannot open file: "+filename)

    operators = ["!", "~", "+", "-", "*", "/", "//", "%", "=", "==", "<", ">", "<=", ">=", "!=",
    "|", "&", "^", "||", "&&", "(", ")", "{", "}", "[", "]", ";", "<<", ">>", ",", "+=", "-=",
    "*=", "/=", "%=", "&=", "|=", "<<=", ">>=", "++", "--", "?", ":", "."]

    token = []
    tokens = []
    lineno = 1
    for line in input_file:
      line = line+" "
      if line.strip().startswith("#include"):
        filename = line.strip().replace("#include", "").strip(' ><"')
        self.scan(filename)
        continue 
      newline = True
      for char in line:
        if not token:
          token = char
        #c style comment
	elif (token + char).startswith("/*"):
	  if (token + char).endswith("*/"):
	    token = ""
	  else:
	    token += char
        #c++ style comment
        elif token.startswith("//"):
          if newline:
            token = char
          else:
            token += char
        #identifier
        elif token[0].isalpha():
          if char.isalnum() or char== "_":
            token += char
          else:
            tokens.append((filename, lineno, token.lower()))
            token = char
        #number
        elif token[0].isdigit():
          if char.isdigit() or char.upper() in ".XABCDEF":
            token += char
          else:
            tokens.append((filename, lineno, token))
            token = char
        #operator
        elif token in operators:
          if token + char in operators:
            token += char
          else:
            tokens.append((filename, lineno, token))
            token = char
        else:
          token = char
        newline = False
      lineno += 1
    self.tokens.extend(tokens)

  def error(self, string):
      raise C2VHDLError(string + "\n", self.filename, self.lineno)

  def peek(self):
    if self.tokens:
      return self.tokens[0][2]
    else:
      return ""

  def get(self):
    if self.tokens:
      self.lineno = self.tokens[0][1]
      self.filename = self.tokens[0][0]
    filename, lineno, token = self.tokens.pop(0)
    return token

  def end(self):
    return not self.tokens

  def expect(self, expected):
    filename, lineno, actual = self.tokens.pop(0)
    if self.tokens:
      self.lineno = self.tokens[0][1]
      self.filename = self.tokens[0][0]
    if actual == expected:
      return
    else:
      self.error("Expected: %s, got: %s"%(expected, actual))

#Register Allocator
####################################################################################################
class Allocator:

  """Maintain a pool of registers, variables and arrays. Keep track of what they are used for."""

  def __init__(self, reuse):
    self.registers = []
    self.arrays = []
    self.all_arrays = []
    self.all_registers = {}
    self.reuse = reuse

  def new_array(self, size):
    reg = 0
    while reg in self.arrays:
      reg += 1
    self.arrays.append(reg)
    self.all_arrays.append((reg, size))
    return reg

  def new(self, name="temporary_register"):
    reg = 0
    while reg in self.registers:
      reg += 1
    self.registers.append(reg)
    self.all_registers[reg] = name
    return reg

  def free(self, register):
    if register in self.registers and self.reuse:
      self.registers.remove(register)

#Parser
####################################################################################################
class Parser:

  """Turn the C input file into a tree of expressions and statements."""

  def __init__(self, input_file, reuse):
    self.scope = {}
    self.function = None
    self.loop = None
    self.tokens = Tokens(input_file)
    self.allocator = Allocator(reuse)
    self.structs = []

  def parse_process(self):
    process = Process()
    process.allocator = self.allocator
    process.inputs = []
    process.outputs = []
    process.functions = []
    while not self.tokens.end():
      if self.tokens.peek() == "struct":
        self.parse_define_struct()
      elif self.tokens.peek() == "typedef":
        self.parse_typedef_struct()
      else:
        process.functions.append(self.parse_function())
    process.main = self.main
    return process

  def parse_function(self):
    function = Function()
    function.allocator = self.allocator
    stored_scope = self.scope
    if self.tokens.get() not in ["int", "short", "long", "char"]:
      self.tokens.error("unknown type")
    function.name = self.tokens.get()
    self.tokens.expect("(")
    function.return_address = self.allocator.new(function.name+" return address")
    function.return_value = self.allocator.new(function.name+" return value")
    function.arguments = []
    while self.tokens.peek() != ")":
      if self.tokens.get() not in ["int", "short", "long", "char"]:
        self.tokens.error("unknown type")
      argument = self.tokens.get()
      function.arguments.append(Argument(argument, self))
      if self.tokens.peek() == ",":
        self.tokens.expect(",")
      else:
        break
    self.tokens.expect(")")
    self.function = function
    function.statement = self.parse_statement()
    if not hasattr(function, "return_statement"):
      self.tokens.error("Function must have a return statement")
    self.function = None
    self.scope = stored_scope
    self.scope[function.name] = function
    #main thread is last function
    self.main = function
    return function

  def parse_break(self):
    break_ = Break()
    break_.loop = self.loop
    self.tokens.expect("break")
    self.tokens.expect(";")
    return break_

  def parse_continue(self):
    continue_ = Continue()
    continue_.loop = self.loop
    self.tokens.expect("continue")
    self.tokens.expect(";")
    return continue_

  def parse_return(self):
    return_ = Return()
    return_.function = self.function
    self.function.return_statement = return_
    self.tokens.expect("return")
    return_.expression = self.parse_expression()
    self.tokens.expect(";")
    return return_

  def parse_assert(self):
    assert_ = Assert()
    assert_.allocator = self.allocator
    self.tokens.expect("assert")
    self.tokens.expect("(")
    assert_.expression = self.parse_expression()
    self.tokens.expect(")")
    self.tokens.expect(";")
    assert_.line = self.tokens.lineno
    assert_.filename = self.tokens.filename
    return assert_

  def parse_report(self):
    report_ = Report()
    report_.allocator = self.allocator
    self.tokens.expect("report")
    self.tokens.expect("(")
    report_.expression = self.parse_expression()
    self.tokens.expect(")")
    self.tokens.expect(";")
    report_.line = self.tokens.lineno
    report_.filename = self.tokens.filename
    return report_

  def parse_wait_clocks(self):
    wait_clocks = WaitClocks()
    wait_clocks.allocator = self.allocator
    self.tokens.expect("wait_clocks")
    self.tokens.expect("(")
    wait_clocks.expression = self.parse_expression()
    self.tokens.expect(")")
    self.tokens.expect(";")
    wait_clocks.line = self.tokens.lineno
    return wait_clocks

  def parse_statement(self):
    if self.tokens.peek() in ["int", "short", "long", "char"] + self.structs:
      return self.parse_compound_declaration()
    elif self.tokens.peek() == "struct":
      return self.parse_struct_declaration()
    elif self.tokens.peek() == "if":
      return self.parse_if()
    elif self.tokens.peek() == "while":
      return self.parse_while()
    elif self.tokens.peek() == "for":
      return self.parse_for()
    elif self.tokens.peek() == "return":
      return self.parse_return()
    elif self.tokens.peek() == "break":
      return self.parse_break()
    elif self.tokens.peek() == "continue":
      return self.parse_continue()
    elif self.tokens.peek() == "{":
      return self.parse_block()
    elif self.tokens.peek() == "assert":
      return self.parse_assert()
    elif self.tokens.peek() == "report":
      return self.parse_report()
    elif self.tokens.peek() == "switch":
      return self.parse_switch()
    elif self.tokens.peek() == "case":
      return self.parse_case()
    elif self.tokens.peek() == "default":
      return self.parse_default()
    elif self.tokens.peek() == "wait_clocks":
      return self.parse_wait_clocks()
    else:
      expression = self.parse_discard()
      self.tokens.expect(";")
      return expression

  def parse_discard(self):
    return DiscardExpression(self.parse_expression(), self.allocator)

  def parse_assignment(self):
    assignment_operators = ["=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "<<=", ">>=", "++", "--"]
    lvalue = self.parse_ternary_expression()
    if self.tokens.peek() in assignment_operators:
      if not hasattr(lvalue, "declaration"):
        self.tokens.error("left hand operand of assignment is not modifiable")
      operator = self.tokens.get()
      if operator == "=":
        expression = self.parse_ternary_expression()
      elif operator in ["++", "--"]:
        expression = Binary(operator[:-1], lvalue, Constant(1), self.allocator)
      else:
        expression = Binary(operator[:-1], lvalue, self.parse_ternary_expression(), self.allocator)
      return Assignment(lvalue, expression, self.allocator)
    else:
      return lvalue

  def parse_if(self):
    if_ = If()
    if_.allocator = self.allocator
    self.tokens.expect("if")
    self.tokens.expect("(")
    if_.expression = self.parse_expression()
    self.tokens.expect(")")
    if_.true_statement = self.parse_statement()
    if self.tokens.peek() == "else":
      self.tokens.expect("else")
      if_.false_statement = self.parse_statement()
    else:
      if_.false_statement = None
    return if_

  def parse_switch(self):
    switch = Switch()
    switch.cases = {}
    self.tokens.expect("switch")
    self.tokens.expect("(")
    expression = self.parse_expression()
    self.tokens.expect(")")
    stored_loop = self.loop
    self.loop = switch
    statement = self.parse_statement()
    self.loop = stored_loop
    switch.expression = expression
    switch.allocator = self.allocator
    switch.statement = statement
    return switch

  def parse_case(self):
    self.tokens.expect("case")
    expression = self.parse_expression()
    self.tokens.expect(":")
    try:
      expression = value(expression)
      case = Case()
      self.loop.cases[expression] =  case
    except NotConstant:
      self.tokens.error("case expression must be constant")
    except AttributeError:
      self.tokens.error("case statements may only be use inside a switch statment")
    return case

  def parse_default(self):
    self.tokens.expect("default")
    self.tokens.expect(":")
    default = Default()
    if not hasattr(self.loop, "cases"):
      self.tokens.error("default statements may only be used inside a switch statment")
    if hasattr(self.loop, "default"):
      self.tokens.error("A switch statement may only have one default statement")
    self.loop.default=default
    return default

  def parse_while(self):
    loop = Loop()
    self.tokens.expect("while")
    self.tokens.expect("(")
    expression = self.parse_expression()
    self.tokens.expect(")")
    stored_loop = self.loop
    self.loop = loop
    statement = self.parse_statement()
    self.loop = stored_loop

    if_ = If()
    loop.statement = if_
    break_ = Break()
    break_.loop = loop
    if_.allocator = self.allocator
    if_.expression = expression
    if_.false_statement = break_
    if_.true_statement = statement

    return loop

  def parse_for(self):
    for_ = For()
    for_.allocator = self.allocator
    self.tokens.expect("for")
    self.tokens.expect("(")
    if self.tokens.peek() != ";":
      for_.statement1 = self.parse_discard()
    self.tokens.expect(";")
    if self.tokens.peek() != ";":
      for_.expression = self.parse_expression()
    self.tokens.expect(";")
    if self.tokens.peek() != ")":
      for_.statement2 = self.parse_discard()
    self.tokens.expect(")")
    stored_loop = self.loop
    self.loop = for_
    for_.statement3 = self.parse_statement()
    self.loop = stored_loop
    return for_

  def parse_block(self):
    block = Block()
    stored_scope = self.scope
    self.tokens.expect("{")
    block.statements = []
    while self.tokens.peek() != "}":
      block.statements.append(self.parse_statement())
    self.tokens.expect("}")
    self.scope = stored_scope
    return block

  def parse_struct_body(self):
    self.tokens.expect("{")
    members = {}
    while self.tokens.peek() != "}":
      type_ = self.tokens.get()
      name = self.tokens.get()
      members[name] = self.parse_declaration(type_, name)
      self.tokens.expect(";")
    self.tokens.expect("}")
    return members

  def parse_typedef_struct(self):
    self.tokens.expect("typedef")
    self.tokens.expect("struct")
    declaration = StructDeclaration(self.parse_struct_body())
    name = self.tokens.get()
    self.tokens.expect(";")
    self.scope[name] = declaration
    self.structs.append(name)

  def parse_define_struct(self):
    self.tokens.expect("struct")
    name = self.tokens.get()
    declaration = StructDeclaration(self.parse_struct_body())
    self.tokens.expect(";")
    self.scope[name] = declaration

  def parse_struct_declaration(self):
    self.tokens.expect("struct")
    struct_name = self.tokens.get()
    name = self.tokens.get()
    self.tokens.expect(";")
    instance = self.scope[struct_name].instance()
    self.scope[name] = instance
    return instance

  def parse_compound_declaration(self):
    type_ = self.tokens.get()
    instances = []
    while True:
      name = self.tokens.get()
      instance = self.parse_declaration(type_, name).instance()
      self.scope[name] = instance
      instances.append(instance)
      if self.tokens.peek() == ",":
        self.tokens.expect(",")
      else:
        break
    self.tokens.expect(";")
    return CompoundDeclaration(instances)

  def parse_declaration(self, type_, name):

    #struct declaration
    if type_ in self.structs:
      declaration = self.scope[type_]
    elif type_ in ["int", "short", "long", "char"]:
      #array declaration 
      if self.tokens.peek() == "[":
        self.tokens.expect("[")
        size = self.tokens.get()
        self.tokens.expect("]")
        declaration = ArrayDeclaration(self.allocator, size)

      #simple variable declaration 
      else:
        if self.tokens.peek() == "=":
          self.tokens.expect("=")
          initializer = self.parse_ternary_expression()
        else:
          initializer = Constant(0)
        declaration = VariableDeclaration(self.allocator, initializer, name)

    return declaration

  def parse_expression(self):
    expression = self.parse_assignment()
    return expression

  def parse_ternary_expression(self):
    expression = constant_fold(self.parse_or_expression())
    while self.tokens.peek() in ["?"]:
      self.tokens.expect("?")
      true_expression = constant_fold(self.parse_or_expression())
      self.tokens.expect(":")
      false_expression = constant_fold(self.parse_or_expression())
      expression = OR(AND(expression, true_expression), false_expression)
    return expression

  def parse_or_expression(self):
    expression = self.parse_and_expression()
    while self.tokens.peek() in ["||"]:
      self.tokens.expect("||")
      expression = OR(expression, self.parse_and_expression())
    return expression

  def parse_and_expression(self):
    expression = self.parse_binary_expression(["|"])
    while self.tokens.peek() in ["&&"]:
      self.tokens.expect("&&")
      expression = AND(expression, self.parse_binary_expression(["|"]))
    return expression

  def parse_binary_expression(self, operators):
    operator_precedence = {
        "|": ["^"],
        "^": ["&"],
        "&": ["==", "!="],
        "==": ["<", ">", "<=", ">="],
        "<": ["<<", ">>"],
        "<<": ["+", "-"],
        "+": ["*", "/", "%"],
    }
    if operators[0] not in operator_precedence:
      expression = self.parse_unary_expression()
      while self.tokens.peek() in operators:
        expression = Binary(self.tokens.get(), expression, self.parse_unary_expression(), self.allocator)
      return expression
    else:
      next_operators = operator_precedence[operators[0]]
      expression = self.parse_binary_expression(next_operators)
      while self.tokens.peek() in operators:
        expression = Binary(self.tokens.get(), expression, self.parse_binary_expression(next_operators), self.allocator)
      return expression

  def parse_unary_expression(self):
    if self.tokens.peek() == "!":
      operator = self.tokens.get()
      expression = self.parse_paren_expression()
      return Binary("==", expression, Constant(0), self.allocator)
    elif self.tokens.peek() == "-":
      operator = self.tokens.get()
      expression = self.parse_paren_expression()
      return Binary("-", Constant(0), expression, self.allocator)
    elif self.tokens.peek() == "~":
      operator = self.tokens.get()
      expression = self.parse_paren_expression()
      return Unary("~", expression)
    else:
      return self.parse_paren_expression()

  def parse_paren_expression(self):
    if self.tokens.peek() == "(":
      self.tokens.expect("(")
      expression = self.parse_expression()
      self.tokens.expect(")")
    else:
      expression = self.parse_number_or_variable()
    return expression

  def parse_number_or_variable(self):
    if self.tokens.peek()[0].isalpha():
      name = self.tokens.get()
      if self.tokens.peek() == "(":
        return self.parse_function_call(name)
      else:
        return self.parse_variable(name)
    else:
      return self.parse_number()

  def parse_input(self, name):
    input_name = name.replace("input_", "")
    self.tokens.expect("(")
    self.tokens.expect(")")
    return Input(input_name)

  def parse_ready(self, name):
    input_name = name.replace("ready_", "")
    self.tokens.expect("(")
    self.tokens.expect(")")
    return Ready(input_name)

  def parse_output(self, name):
    output_name = name.replace("output_", "")
    self.tokens.expect("(")
    expression = self.parse_expression()
    self.tokens.expect(")")
    return Output(output_name, expression)

  def parse_function_call(self, name):
    if name.startswith("input_"):
      return self.parse_input(name)
    if name.startswith("ready_"):
      return self.parse_ready(name)
    if name.startswith("output_"):
      return self.parse_output(name)
    function_call = FunctionCall()
    function_call.arguments = []
    self.tokens.expect("(")
    while self.tokens.peek() != ")":
      function_call.arguments.append(self.parse_expression())
      if self.tokens.peek() == ",":
        self.tokens.expect(",")
      else:
        break
    self.tokens.expect(")")

    if name not in self.scope:
      self.tokens.error("Unknown function: %s"%name)

    function_call.function = self.scope[name]
    if len(function_call.arguments) != len(function_call.function.arguments):
      self.tokens.error("Function %s takes %s arguments %s given."%(
        name,
        len(function_call.function.arguments),
        len(function_call.arguments)
      ))
    return function_call

  def parse_number(self):
    try:
      token = self.tokens.get()
      return Constant(eval(token))
    except SyntaxError:
      self.tokens.error("%s is not a number"%token)

  def parse_variable(self, name):
    if name not in self.scope:
      self.tokens.error("Unknown variable: %s"%name)
    instance = self.scope[name]
    return self.parse_variable_array_struct(instance)
 
  def parse_variable_array_struct(self, instance):
    if instance.type_ == "variable":
      return Variable(instance, self.allocator)
    elif instance.type_ == "array":
      self.tokens.expect("[")
      index_expression = self.parse_expression()
      self.tokens.expect("]")
      return Array(instance, index_expression, self.allocator)
    elif instance.type_ == "struct":
      self.tokens.expect(".")
      member = self.tokens.get()
      instance = instance.members[member]
      return self.parse_variable_array_struct(instance)

#Parse tree/Machine instruction generator
####################################################################################################

#These are the leaves of the parse tree.
#Each one provides a generate method that returns a list of machine code instructions.
#an instruction is represented as a dictionary of operands

#Statements come first...

class Process:
  def generate(self):
    instructions = []
    instructions.append({"op"   :"jmp_and_link",
                         "dest" :self.main.return_address,
                         "label":"function_%s"%id(self.main)})
    instructions.append({"op":"stop"})
    for function in self.functions:
      instructions.extend(function.generate())
    return instructions

class Function:
  def generate(self):
    instructions = []
    instructions.append({"op":"label", "label":"function_%s"%id(self)})
    instructions.extend(self.statement.generate())
    return instructions

class Break:
  def generate(self): return [{"op":"goto", "label":"break_%s"%id(self.loop)}]

class Continue:
  def generate(self): return [{"op":"goto", "label":"continue_%s"%id(self.loop)}]

class Assert:
  def generate(self):
    result = self.allocator.new()
    instructions = self.expression.generate(result)
    self.allocator.free(result)
    instructions.append({"op":"assert", "src":result, "line":self.line, "file":self.filename})
    return instructions

class Return:
  def generate(self):
    instructions = self.expression.generate(self.function.return_value)
    instructions.append({"op":"jmp_to_reg", "src":self.function.return_address})
    return instructions

class Report:
  def generate(self):
    result = self.allocator.new()
    instructions = self.expression.generate(result)
    self.allocator.free(result)
    instructions.append({"op":"report", "src":result, "line":self.line, "file":self.filename})
    return instructions

class WaitClocks:
  def generate(self):
    result = self.allocator.new()
    instructions = self.expression.generate(result)
    self.allocator.free(result)
    instructions.append({"op":"wait_clocks", "src":result})
    return instructions

class If:
  def generate(self):
    try:
      if value(self.expression):
        return self.true_statement.generate()
      else:
        if self.false_statement:
          return self.false_statement.generate()
        else:
          return []
    except NotConstant:
      result = self.allocator.new()
      instructions = []
      instructions.extend(self.expression.generate(result))
      instructions.append({"op"   :"jmp_if_false",
                           "src" :result,
                           "label":"else_%s"%id(self)})
      self.allocator.free(result)
      instructions.extend(self.true_statement.generate())
      instructions.append({"op":"goto", "label":"end_%s"%id(self)})
      instructions.append({"op":"label", "label":"else_%s"%id(self)})
      if self.false_statement:
        instructions.extend(self.false_statement.generate())
      instructions.append({"op":"label", "label":"end_%s"%id(self)})
      return instructions

class Switch:
  def generate(self):
    result = self.allocator.new()
    test = self.allocator.new()
    instructions = self.expression.generate(result)
    for value, case in self.cases.iteritems():
      instructions.append({"op":"==", "dest":test, "src":result, "right":value})
      instructions.append({"op":"jmp_if_true", "src":test, "label":"case_%s"%id(case)})
    if hasattr(self, "default"):
      instructions.append({"op":"goto", "label":"case_%s"%id(self.default)})
    self.allocator.free(result)
    self.allocator.free(test)
    instructions.extend(self.statement.generate())
    instructions.append({"op":"label", "label":"break_%s"%id(self)})
    return instructions

class Case:
  def generate(self):
    return [{"op":"label", "label":"case_%s"%id(self)}]

class Default:
  def generate(self):
    return [{"op":"label", "label":"case_%s"%id(self)}]

class Loop:
  def generate(self):
      instructions = [{"op":"label", "label":"begin_%s"%id(self)}]
      instructions.append({"op":"label", "label":"continue_%s"%id(self)})
      instructions.extend(self.statement.generate())
      instructions.append({"op":"goto", "label":"begin_%s"%id(self)})
      instructions.append({"op":"label", "label":"break_%s"%id(self)})
      return instructions

class For:
  def generate(self):
    instructions = []
    if hasattr(self, "statement1"):
      instructions.extend(self.statement1.generate())
    result = self.allocator.new()
    instructions.append({"op":"label", "label":"begin_%s"%id(self)})
    if hasattr(self, "expression"):
      instructions.extend(self.expression.generate(result))
      instructions.append({"op":"jmp_if_false", "src":result, "label":"end_%s"%id(self)})
    self.allocator.free(result)
    instructions.extend(self.statement3.generate())
    instructions.append({"op":"label", "label":"continue_%s"%id(self)})
    if hasattr(self, "statement2"):
      instructions.extend(self.statement2.generate())
    instructions.append({"op":"goto", "label":"begin_%s"%id(self)})
    instructions.append({"op":"label", "label":"end_%s"%id(self)})
    instructions.append({"op":"label", "label":"break_%s"%id(self)})
    return instructions

class Block:
  def generate(self):
    instructions = []
    for statement in self.statements:
      instructions.extend(statement.generate())
    return instructions

class CompoundDeclaration:
  def __init__(self, declarations):
    self.declarations = declarations

  def generate(self):
    instructions = []
    for declaration in self.declarations:
      instructions.extend(declaration.generate());
    return instructions

class VariableDeclaration:
  def __init__(self, allocator, initializer, name):
    self.initializer = initializer
    self.allocator = allocator
    self.name = name
  def instance(self):
    register = self.allocator.new("variable "+self.name)
    return VariableInstance(register, self.initializer)

class VariableInstance:
  def __init__(self, register, initializer):
    self.register = register
    self.type_ = "variable"
    self.initializer = initializer
  def generate(self):
    return self.initializer.generate(self.register)

class ArrayDeclaration:
  def __init__(self, allocator, size):
    self.allocator = allocator
    self.size = size
  def instance(self):
    register = self.allocator.new_array(self.size)
    return ArrayInstance(register, self.size)

class ArrayInstance:
  def __init__(self, register, size):
    self.register = register
    self.size = size
    self.type_ = "array"
  def generate(self):
    return []

class StructDeclaration:
  def __init__(self, members):
    self.members = members

  def instance(self):
    instances = {}
    for name, declaration in self.members.iteritems():
      instances[name] = declaration.instance()
    return StructInstance(instances)

class StructInstance:
  def __init__(self, members):
    self.members = members
    self.type_ = "struct"

  def generate(self):
    instructions = []
    for member in self.members.values():
      instructions.extend(member.generate())
    return instructions

class Argument:
  def __init__(self, name, parser):
    self.type_="variable"
    parser.scope[name] = self
    self.register = parser.allocator.new("function argument "+name)
  def generate(self): return []

class DiscardExpression:
  def __init__(self, expression, allocator):
    self.expression = expression
    self.allocator = allocator

  def generate(self):
    result = self.allocator.new()
    instructions = self.expression.generate(result)
    self.allocator.free(result)
    return instructions

#...then Expressions...

#Expressions generate methods accept a result argument.
#This indicates which register to put the result in.

#Expressions may also provide a value method which returns the value of an xpression
#if it can be calculated at compile time.

def AND(left, right):
  return ANDOR(left, right, "jmp_if_false")

def OR(left, right):
  return ANDOR(left, right, "jmp_if_true")

class ANDOR:
  def __init__(self, left, right, op):
    self.left = constant_fold(left)
    self.right = constant_fold(right)
    self.op = op

  def generate(self, result):
    instructions = self.left.generate(result)
    instructions.append({"op":self.op, "src":result, "label":"end_%s"%id(self)})
    instructions.extend(self.right.generate(result))
    instructions.append({"op":"label", "label":"end_%s"%id(self)})
    return instructions

  def value(self):
    if self.op == "jmp_if_false":
      return value(self.left) and value(self.right)
    else:
      return value(self.left) or value(self.right)

class Binary:
  def __init__(self, operator, left, right, allocator):
    self.left = constant_fold(left)
    self.right = constant_fold(right)
    self.operator = operator
    self.allocator = allocator

  def generate(self, result):
    try:
      instructions = self.right.generate(result)
      instructions.append({"op"  :self.operator,
                           "dest":result,
                           "left":value(self.left),
                           "srcb":result})
    except NotConstant:
      try:
        instructions = self.left.generate(result)
        instructions.append({"op"   :self.operator,
                             "dest" :result,
                             "src"  :result,
                             "right":value(self.right)})
      except NotConstant:
        instructions = self.left.generate(result)
        right = self.allocator.new()
        instructions.extend(self.right.generate(right))
        instructions.append({"op":self.operator, "dest":result, "src":result, "srcb":right})
        self.allocator.free(right)
    return instructions

  def value(self):
    return eval("%s %s %s"%(value(self.left), self.operator, value(self.right)))

class Unary:
  def __init__(self, operator, expression):
    self.expression = constant_fold(expression)
    self.operator = operator

  def generate(self, result):
    instructions = self.expression.generate(result)
    instructions.extend([{"op":self.operator, "dest":result, "src":result}])
    return instructions

  def value(self):
    return eval("%s%s"%(self.operator, value(self.expression)))

class FunctionCall:
  def generate(self, result):
    instructions = []
    for expression, argument in zip(self.arguments, self.function.arguments):
      instructions.extend(expression.generate(argument.register))
    instructions.append({"op"   :"jmp_and_link",
                         "dest" :self.function.return_address,
                         "label":"function_%s"%id(self.function)})
    instructions.append({"op"   :"move",
                         "dest" :result,
                         "src"  :self.function.return_value})
    return instructions

class Output:
  def __init__(self, name, expression):
    self.name = name
    self.expression = expression

  def generate(self, result):
    instructions = self.expression.generate(result);
    instructions.append({"op"   :"write", "src"  :result, "output":self.name})
    return instructions

class Input:
  def __init__(self, name):
    self.name = name

  def generate(self, result):
      return [{"op"   :"read", "dest" :result, "input":self.name}]

class Ready:
  def __init__(self, name):
    self.name = name

  def generate(self, result):
      return [{"op"   :"ready", "dest" :result, "input":self.name}]

class Array:
  def __init__(self, declaration, index_expression, allocator):
    self.declaration = declaration
    self.allocator = allocator
    self.index_expression = index_expression

  def generate(self, result):
    instructions = []
    index = self.allocator.new()
    instructions.extend(self.index_expression.generate(index))
    instructions.append({"op"   :"array_read",
                         "array":self.declaration.register,
                         "index":index,
                         "dest" :result,
                         "size" :self.declaration.size})
    self.allocator.free(index)
    return instructions

class Variable:
  def __init__(self, declaration, allocator):
    self.declaration = declaration
    self.allocator = allocator

  def generate(self, result):
    instructions = []
    if result != self.declaration.register:
      instructions.append({"op"  :"move",
                           "dest":result,
                           "src" :self.declaration.register})
    return instructions

class Assignment:
  def __init__(self, lvalue, expression, allocator):
    self.lvalue = lvalue
    self.expression = expression
    self.allocator = allocator

  def generate(self, result):
    instructions = self.expression.generate(result)

    if self.lvalue.declaration.type_ == "variable":

      if result != self.lvalue.declaration.register:
        instructions.append({"op"   : "move",
                             "dest" : self.lvalue.declaration.register,
                             "src"  : result})

    elif self.lvalue.declaration.type_ == "array":

      index = self.allocator.new()
      instructions.extend(self.lvalue.index_expression.generate(index))
      instructions.append({"op"    :"array_write",
                           "array" :self.lvalue.declaration.register,
                           "src"   :result,
                           "index" :index,
                           "size"  :self.lvalue.declaration.size})
      self.allocator.free(index)

    return instructions

class Constant:
  def __init__(self, value):
    self._value = value

  def generate(self, result):
    instructions = [{"op":"literal", "dest":result, "literal":self._value}]
    return instructions

  def value(self):
    return self._value

#Instruction level parallelisation
####################################################################################################

#The machine instructions generated by the Machine code generator, is a single list of instructions.
#Since we are generating code for a hardware implementation, we do not needto limit oursleves to
#issuing instructions one at a time.

#This function converts a list of instructions into a list of frames containing mutliple
#instructions. In the final implementation, all instructions within a frameare executed concurently.

#The function looks at the dependencies between one instruction and anotherto determine whether
#instructions can be reordered.

def parallelise(instructions):

  def modifies_register(instruction):

    """Return the register modified by this instruction if any"""

    if "dest" in instruction:
      return instruction["dest"]
    return None

  def uses_registers(instruction):

    """Return the registers used by this instruction if any"""

    registers = []
    for field in ["src", "srcb", "index"]:
      if field in instruction:
        registers.append(instruction[field])
    return registers

  def modifies_array(instruction):

    """Return the array modified by this instruction if any"""

    if instruction["op"] == "array_write":
      return instruction["array"]
    return None

  def uses_array(instruction):

    """Return the array used by this instruction if any"""

    if instruction["op"] == "array_read":
      return instruction["array"]
    return None

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
      if modifies_array(i) is not None:
        if modifies_array(i) == uses_array(instruction):
          return True
        if modifies_array(i) == modifies_array(instruction):
          return True
      if is_jump(i):
        return True
    for i in preceding:
      if modifies_register(i) is not None:
        if modifies_register(instruction) in uses_registers(i):
          return True
      if modifies_array(i) is not None:
        if uses_array(i) == modifies_array(instruction):
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

#VHDL Code Generator
####################################################################################################

def generate_VHDL(input_file, name, frames, output_file, registers, arrays):

  """A big ugly function to crunch through all the instructions and generate the VHDL equivilent"""

  #trandslate C operators to VHDL functions
  operator_functions = {"+" :"ADD", "-" :"SUB", "*" :"MUL", "&" :"BAND", "|" :"BOR", "^":"BXOR",
    "/" :"DIV", "%" :"MODULO", "<<":"LSHIFT", ">>":"RSHIFT", "<" :"LT", ">":"GT", "<=":"LE",
    ">=":"GE", "==":"EQ", "!=":"NE"}

  #translate VHDL functions to VHDL operators
  function_operators = {"ADD":"+", "SUB":"-", "MUL":"*", "BAND":"and", "BOR":"or", "BXOR":"xor",
    "DIV":"/", "MODULO":"mod", "LSHIFT":"SHIFT_LEFT", "RSHIFT":"SHIFT_RIGHT", "LT":"<", "GT":">",
    "LE":"<=", "GE":">=", "EQ":"=", "NE":"/="}

  #work out which operators are needed
  operators = [i["op"] for frame in frames for i in frame]
  functions = unique([operator_functions[i] for i in operators if i in operator_functions])

  #calculate the values of jump locations
  location = 0
  labels = {}
  new_frames = []
  for frame in frames:
    if frame[0]["op"] == "label":
      labels[frame[0]["label"]] = location
    else:
      new_frames.append(frame)
      location += 1
  frames = new_frames

  #substitue real values for labeled jump locations
  for frame in frames:
    for instruction in frame:
      if "label" in instruction:
        instruction["label"]=labels[instruction["label"]]

  #list all inputs and outputs used in the program
  inputs = unique([i["input"] for frame in frames for i in frame if "input" in i])
  outputs = unique([i["output"] for frame in frames for i in frame if "output" in i])
  testbench = not inputs and not outputs

  #in testbench mode, generate clk and reset internaly
  if testbench:
    input_ports = []
    signals = ["  signal CLK : std_logic;\n",
               "  signal RST : std_logic;\n",
               "  signal STOP : boolean := False;\n",
               "  signal TIMER : signed(15 downto 0);\n"]
  else:
    input_ports = ["    CLK : in std_logic", "    RST : in std_logic"]
    signals = ["  signal STOP : boolean := False;\n",
               "  signal TIMER : signed(15 downto 0);\n"]

  #output the code in VHDL
  output_file.write("--name : %s\n"%name)
  output_file.write("--tag : c components\n")
  for i in inputs:
      output_file.write("--input : INPUT_%s:16\n"%i)
  for i in outputs:
      output_file.write("--output : OUTPUT_%s:16\n"%i)
  output_file.write("--source_file : %s\n"%input_file)
  output_file.write("---%s\n"%name.title())
  output_file.write("---%s\n"%"".join(["=" for i in name]))
  output_file.write("---\n")
  output_file.write("---*Created by C2VHDL*\n\n")

  output_file.write("library ieee;\n")
  output_file.write("use ieee.std_logic_1164.all;\n")
  output_file.write("use ieee.numeric_std.all;\n\n")
  output_file.write("entity %s is\n"%name)

  #Do not generate a port in testbench mode
  if not testbench:
    output_file.write("  port(\n")
    input_ports.extend(["    INPUT_%s : in std_logic_vector(15 downto 0)"%i.upper() for i in inputs])
    input_ports.extend(["    INPUT_%s_STB : in std_logic"%i.upper() for i in inputs])
    input_ports.extend(["    OUTPUT_%s_ACK : in std_logic"%i.upper() for i in outputs])
    output_ports = []
    output_ports.extend(["    OUTPUT_%s : out std_logic_vector(15 downto 0)"%i.upper() for i in outputs])
    output_ports.extend(["    OUTPUT_%s_STB : out std_logic"%i.upper() for i in outputs])
    output_ports.extend(["    INPUT_%s_ACK : out std_logic"%i.upper() for i in inputs])
    output_file.write(";\n".join(input_ports+output_ports))
    output_file.write(");\n")

  output_file.write("end entity %s;\n\n"%name)
  output_file.write("architecture RTL of %s is\n\n"%name)

  #Generate arithmetic functions used by instructions
  for function in functions:
    output_file.write("  function %s(A:signed; B:signed) return signed is\n"%function)
    output_file.write("  begin\n")
    if function in ["ADD", "SUB", "MUL", "BOR", "BAND", "BXOR", "DIV", "MODULO"]:
      output_file.write("    return resize(A %s B, 16);\n"%function_operators[function])
    elif function in ["EQ","NE","LT","GT","LE","GE"]:
      output_file.write("    if A %s B then\n"%function_operators[function])
      output_file.write('      return X"0001";\n')
      output_file.write("    else\n")
      output_file.write('      return X"0000";\n')
      output_file.write("    end if;\n")
    elif function in ["LSHIFT", "RSHIFT"]:
      output_file.write('      return %s(A, to_integer(B));\n'%function_operators[function])
    output_file.write("  end function;\n\n")

  #Generate internal signals
  output_file.write("  signal PROGRAM_COUNTER : integer range 0 to %s;\n"%len(frames))
  for register, use in registers.iteritems():
    output_file.write("  signal REGISTER_%s: signed(15 downto 0);--%s\n"%(register, use))
  signals.extend(["  signal S_OUTPUT_%s_STB : std_logic;\n"%i.upper() for i in outputs])
  signals.extend(["  signal S_INPUT_%s_ACK : std_logic;\n"%i.upper() for i in inputs])
  for signal in signals:
    output_file.write(signal)

  #Generate arrays
  for array, size in arrays:
    size = int(size)
    output_file.write("  type ARRAY_%s_TYPE is array (0 to %s) of signed(15 downto 0);\n"%(
    array, (size-1)))
    output_file.write("  signal ARRAY_%s : ARRAY_%s_TYPE;\n"%(array, array))
  output_file.write("\nbegin\n\n")

  #In testbench mode, generate a clock internaly
  if testbench:
    output_file.write("  GENERATE_CLK : process\n")
    output_file.write("  begin\n")
    output_file.write("    while not STOP loop\n")
    output_file.write("      CLK <= '0';\n")
    output_file.write("      wait for 5 ns;\n")
    output_file.write("      CLK <= '1';\n")
    output_file.write("      wait for 5 ns;\n")
    output_file.write("    end loop;\n")
    output_file.write("    wait;\n")
    output_file.write("  end process GENERATE_CLK;\n\n")
    output_file.write("  RST <= '1', '0' after 50 ns;\n\n")

  #Generate a state machine to execute the instructions
  binary_operators = ["+", "-", "*", "/", "|", "&", "^", "<<", ">>", "<",">", ">=",
    "<=", "==", "!="]
  output_file.write("  EXECUTE : process\n")
  output_file.write("  begin\n")
  output_file.write("    wait until rising_edge(CLK);\n")
  output_file.write("    PROGRAM_COUNTER <= PROGRAM_COUNTER + 1;\n")
  output_file.write('    TIMER <= X"0000";\n')
  output_file.write("    case PROGRAM_COUNTER is\n")

  #A frame is executed in each state
  for location, frame in enumerate(frames):
    output_file.write("      when %s =>\n"%location)
    for instruction in frame:

      if instruction["op"] == "literal":
        output_file.write(
          "        REGISTER_%s <= to_signed(%s, 16);\n"%(
          instruction["dest"],
          instruction["literal"]))

      elif instruction["op"] == "move":
        output_file.write(
          "        REGISTER_%s <= REGISTER_%s;\n"%(
          instruction["dest"],
          instruction["src"]))

      elif instruction["op"] in ["~"]:
        output_file.write(
          "        REGISTER_%s <= not REGISTER_%s;\n"%(
          instruction["dest"],
          instruction["src"]))

      elif instruction["op"] in binary_operators and "left" in instruction:
        output_file.write(
          "        REGISTER_%s <= %s(to_signed(%s, 16), REGISTER_%s);\n"%(
          instruction["dest"],
          operator_functions[instruction["op"]],
          instruction["left"],
          instruction["srcb"]))

      elif instruction["op"] in binary_operators and "right" in instruction:
        output_file.write(
          "        REGISTER_%s <= %s(REGISTER_%s, to_signed(%s, 16));\n"%(
          instruction["dest"],
          operator_functions[instruction["op"]],
          instruction["src"],
          instruction["right"]))

      elif instruction["op"] in binary_operators:
        output_file.write(
          "        REGISTER_%s <= %s(REGISTER_%s, REGISTER_%s);\n"%(
          instruction["dest"],
          operator_functions[instruction["op"]],
          instruction["src"],
          instruction["srcb"]))

      elif instruction["op"] == "jmp_if_false":
        output_file.write('        if REGISTER_%s = X"0000" then\n'%(instruction["src"]));
        output_file.write("          PROGRAM_COUNTER <= %s;\n"%instruction["label"])
        output_file.write("        end if;\n")

      elif instruction["op"] == "jmp_if_true":
        output_file.write('        if REGISTER_%s /= X"0000" then\n'%(instruction["src"]));
        output_file.write("          PROGRAM_COUNTER <= %s;\n"%instruction["label"])
        output_file.write("        end if;\n")

      elif instruction["op"] == "jmp_and_link":
        output_file.write("        PROGRAM_COUNTER <= %s;\n"%instruction["label"])
        output_file.write("        REGISTER_%s <= to_signed(%s, 16);\n"%(
          instruction["dest"], location+1))

      elif instruction["op"] == "jmp_to_reg":
        output_file.write(
          "        PROGRAM_COUNTER <= to_integer(REGISTER_%s);\n"%instruction["src"])

      elif instruction["op"] == "goto":
        output_file.write("        PROGRAM_COUNTER <= %s;\n"%instruction["label"])

      elif instruction["op"] == "read":
        output_file.write("        REGISTER_%s <= signed(INPUT_%s);\n"%(
          instruction["dest"], instruction["input"]))
        output_file.write("        PROGRAM_COUNTER <= %s;\n"%location)
        output_file.write("        S_INPUT_%s_ACK <= '1';\n"%instruction["input"])
        output_file.write( "        if S_INPUT_%s_ACK = '1' and INPUT_%s_STB = '1' then\n"%(
          instruction["input"],
          instruction["input"]))
        output_file.write("          S_INPUT_%s_ACK <= '0';\n"%instruction["input"])
        output_file.write("          PROGRAM_COUNTER <= %s;\n"%(location+1))
        output_file.write("        end if;\n")

      elif instruction["op"] == "ready":
        output_file.write("        REGISTER_%s <= (0 => INPUT_%s_STB, others => '0');\n"%(
          instruction["dest"], instruction["input"]))

      elif instruction["op"] == "write":
        output_file.write("        OUTPUT_%s <= std_logic_vector(REGISTER_%s);\n"%(
          instruction["output"], instruction["src"]))
        output_file.write("        PROGRAM_COUNTER <= %s;\n"%location)
        output_file.write("        S_OUTPUT_%s_STB <= '1';\n"%instruction["output"])
        output_file.write(
          "        if S_OUTPUT_%s_STB = '1' and OUTPUT_%s_ACK = '1' then\n"%(
          instruction["output"],
          instruction["output"]))
        output_file.write("          S_OUTPUT_%s_STB <= '0';\n"%instruction["output"])
        output_file.write("          PROGRAM_COUNTER <= %s;\n"%(location+1))
        output_file.write("        end if;\n")

      elif instruction["op"] == "array_read":
        output_file.write(
          "        REGISTER_%s <= ARRAY_%s(to_integer(REGISTER_%s) mod %s);\n"%(
          instruction["dest"],
          instruction["array"],
          instruction["index"],
          instruction["size"]))

      elif instruction["op"] == "array_write":
        output_file.write(
          "        ARRAY_%s(to_integer(REGISTER_%s) mod %s) <= REGISTER_%s;\n"%(
          instruction["array"],
          instruction["index"],
          instruction["size"],
          instruction["src"]))

      elif instruction["op"] == "assert":
        output_file.write(
          '        assert REGISTER_%s /= X"0000" report "Assertion failed at line: %s in file: %s" severity failure;\n'%(
          instruction["src"],
          instruction["line"],
          instruction["file"]))

      elif instruction["op"] == "wait_clocks":
        output_file.write("        if TIMER < REGISTER_%s then\n"%instruction["src"])
        output_file.write("          PROGRAM_COUNTER <= PROGRAM_COUNTER;\n")
        output_file.write("          TIMER <= TIMER+1;\n")
        output_file.write("        end if;\n")

      elif instruction["op"] == "report":
        output_file.write(
          '        report integer\'image(to_integer(REGISTER_%s)) & " (report at line: %s in file: %s)";\n'%(
          instruction["src"],
          instruction["line"],
          instruction["file"]))

      elif instruction["op"] == "stop":
        output_file.write('        STOP <= True;\n')
        output_file.write("        PROGRAM_COUNTER <= PROGRAM_COUNTER;\n")

  output_file.write("      when others => null;\n")
  output_file.write("    end case;\n")

  #Reset program counter and control signals
  output_file.write("    if RST = '1' then\n")
  output_file.write("      PROGRAM_COUNTER <= 0;\n")
  controls = (
    ["      S_OUTPUT_%s_STB <= '0';\n"%i.upper() for i in outputs] +
    ["      S_INPUT_%s_ACK <= '0';\n"%i.upper() for i in inputs])
  for control in controls:
    output_file.write(control)
  output_file.write("    end if;\n")
  output_file.write("  end process EXECUTE;\n")

  #buffer outputs that need to be read.
  buffers = []
  buffers.extend(["  OUTPUT_%s_STB <= S_OUTPUT_%s_STB;\n"%(i.upper(),i.upper()) for i in outputs])
  buffers.extend(["  INPUT_%s_ACK <= S_INPUT_%s_ACK;\n"%(i.upper(),i.upper()) for i in inputs])
  for buffer in buffers:
    output_file.write(buffer)
  output_file.write("\nend RTL;\n")

#Main Compiler Application
####################################################################################################
if __name__ == "__main__":

  if len(sys.argv) < 2:
    print "Usage: c2vhdl.py [options] <input_file>"
    print
    print "compile options:"
    print "  no_reuse      : prevent register resuse"
    print "  no_concurrent : prevent concurrency"
    print
    print "tool options:"
    print "  ghdl          : compiles using the ghdl compiler"
    print "  modelsim      : compiles using the modelsim compiler"
    print "  run           : runs compiled code, used with ghdl or modelsimoptions"
    sys.exit(-1)

  #parse command line
  input_file = sys.argv[-1]
  reuse = "no_reuse" not in sys.argv

  try:
      #compile into VHDL
      parser = Parser(input_file, reuse)
      process = parser.parse_process()
      name = process.main.name
      instructions = process.generate()
      if "no_concurent" in sys.argv:
        frames = [[i] for i in instructions]
      else:
        frames = parallelise(instructions)
      output_file = name + ".vhd"
      output_file = open(output_file, "w")
      generate_VHDL(input_file, name, frames, output_file, parser.allocator.all_registers,
        parser.allocator.all_arrays)
      output_file.close()
  except C2VHDLError as err:
      print "Error in file:", err.filename, "at line:", err.lineno
      print err.message
      sys.exit(-1)

  #run the compiled design using the simulator of your choice.
  if "ghdl" in sys.argv:
    import os
    import tempfile
    import shutil
    vhdl_file = os.path.abspath("%s.vhd"%name)
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)
    os.system("ghdl -a %s"%vhdl_file)
    os.system("ghdl -e %s"%name)
    if "run" in sys.argv:
      result =  os.system("./%s"%name)
      if result:
        sys.exit(1)
      else:
        sys.exit(0)
    shutil.rmtree(tempdir)

  if "modelsim" in sys.argv:
    import os
    import tempfile
    import shutil
    vhdl_file = os.path.abspath("%s.vhd"%name)
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)
    os.system("vlib compiled")
    os.system("vmap work compiled")
    os.system("vcom %s"%vhdl_file)
    if "run" in sys.argv:
      result = os.system('vsim -c -do "run -all; exit;" %s'%name)
      if result:
        sys.exit(1)
      else:
        sys.exit(0)
    shutil.rmtree(tempdir)

  #Add more tools here ...
