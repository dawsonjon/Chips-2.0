__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

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

    #sign = number & 0x10000
    #number = number & 0xffff
    #if sign:
        #number =  ~0xffff | number
    return int(number)

class Process:
    def generate(self):
        instructions = []
        for function in self.functions:
            if hasattr(function, "declarations"):
                instructions.extend(function.generate())
        instructions.append({"op"   :"jmp_and_link",
                             "dest" :self.main.return_address,
                             "label":"function_%s"%id(self.main)})
        instructions.append({"op":"stop"})
        for function in self.functions:
            if not hasattr(function, "declarations"):
                instructions.extend(function.generate())
        return instructions

class Function:
    def generate(self):
        instructions = []
        instructions.append({"op":"label", "label":"function_%s"%id(self)})
        instructions.extend(self.statement.generate())
        if not hasattr(self, "return_value"):
            instructions.append({"op":"jmp_to_reg", "src":self.return_address})
        return instructions

class Break:
    def generate(self): return [{"op":"goto", "label":"break_%s"%id(self.loop)}]

class Continue:
    def generate(self): return [{"op":"goto", "label":"continue_%s"%id(self.loop)}]

class Assert:
    def generate(self):
        result = self.allocator.new(self.expression.size)
        instructions = self.expression.generate(result)
        self.allocator.free(result)
        instructions.append({"op":"assert", "src":result, "line":self.line, "file":self.filename})
        return instructions

class Return:
    def generate(self):
        if hasattr(self, "expression"):
            instructions = self.expression.generate(self.function.return_value)
        else:
            instructions = []
        instructions.append({"op":"jmp_to_reg", "src":self.function.return_address})
        return instructions

class Report:
    def generate(self):
        result = self.allocator.new(self.expression.size)
        instructions = self.expression.generate(result)
        self.allocator.free(result)
        instructions.append({"op":"report",
                             "src":result,
                             "line":self.line,
                             "file":self.filename,
                             "signed":self.expression.signed})
        return instructions

class WaitClocks:
    def generate(self):
        result = self.allocator.new(self.expression.size)
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
            result = self.allocator.new(self.expression.size)
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
        result = self.allocator.new(self.expression.size)
        test = self.allocator.new(self.expression.size)
        instructions = self.expression.generate(result)
        for value, case in self.cases.iteritems():
            instructions.append({"op":"==", "dest":test, "src":result, "right":value, "signed":True})
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
        instructions.append({"op":"label", "label":"begin_%s"%id(self)})
        if hasattr(self, "expression"):
            result = self.allocator.new(self.expression.size)
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
    def __init__(self, allocator, initializer, name, type_, size, signed):
        self.initializer = initializer
        self.allocator = allocator
        self.type_ = type_
        self.size = size
        self.signed = signed
        self.name = name
    def instance(self):
        register = self.allocator.new(self.size, "variable "+self.name)
        return VariableInstance(register, self.initializer, self.type_, self.size, self.signed)

class VariableInstance:
    def __init__(self, register, initializer, type_, size, signed):
        self.register = register
        self.type_ = type_
        self.initializer = initializer
        self.size = size
        self.signed = signed
    def generate(self):
        return self.initializer.generate(self.register)

class ArrayDeclaration:
    def __init__(self,
                 allocator,
                 size,
                 type_,
                 element_type,
                 element_size,
                 element_signed,
                 initializer = None,
                 initialize_memory = False):

        self.allocator = allocator
        self.type_ = type_
        self.size = size
        self.signed = False
        self.element_type = element_type
        self.element_size = element_size
        self.element_signed = element_signed
        self.initializer = initializer
        self.initialize_memory = initialize_memory

    def instance(self):
        location = self.allocator.new_array(self.size, self.initializer, self.element_size)
        register = self.allocator.new(2, "array")
        return ArrayInstance(location,
                             register,
                             self.size,
                             self.type_,
                             self.initializer,
                             self.initialize_memory,
                             self.element_type,
                             self.element_size,
                             self.element_signed)

class ArrayInstance:
    def __init__(self,
                 location,
                 register,
                 size,
                 type_,
                 initializer,
                 initialize_memory,
                 element_type,
                 element_size,
                 element_signed):

        self.register = register
        self.location = location
        self.type_ = type_
        self.size = size
        self.signed = False
        self.element_type = element_type
        self.element_size = element_size
        self.element_signed = element_signed
        self.initializer = initializer
        self.initialize_memory = initialize_memory

    def generate(self, result=None):
        instructions = []
        #If initialize memory is true, the memory content will initialised (as at configuration time)
        #If initialize memory is false, then the memory will need to be filled by the program.
        if not self.initialize_memory and self.initializer is not None:
            location = 0
            for value in self.initializer:
                instructions.append({
                    "op":"memory_write_literal",
                    "address":location,
                    "value":value,
                    "element_size":self.element_size
                })
                location += 1
        instructions.append({
            "op":"literal",
            "literal":self.location,
            "dest":self.register
        })
        #this bit here is to make string literals work,
        #in this case an array instance is created implicitly,
        #but the value of the expression is the array register.
        if result is not None and result != self.register:
            instructions.append({
                "op"  :"move",
                "dest":result,
                "src" :self.register
            })
        return instructions

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
    def __init__(self,
          name,
          type_,
          size,
          signed,
          parser,
          element_type,
          element_size,
          element_signed):
        self.type_=type_
        self.size=size
        self.signed=signed
        self.element_type = element_type
        self.element_size = element_size
        self.element_signed = element_signed
        parser.scope[name] = self
        self.register = parser.allocator.new(size, "function argument "+name)
    def generate(self): return []

class DiscardExpression:
    def __init__(self, expression, allocator):
        self.expression = expression
        self.allocator = allocator

    def generate(self):
        result = self.allocator.new(self.expression.size)
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
        self.type_ = "int"
        self.size = left.size
        self.signed = left.signed

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
        self.type_ = self.left.type_
        self.size = max(left.size, right.size)
        self.signed = left.signed and right.signed

    def generate(self, result):
        new_register = self.allocator.new(self.size)
        try:
            instructions = self.right.generate(new_register)
            instructions.append({"op"  :self.operator,
                                 "dest":result,
                                 "left":value(self.left),
                                 "src":new_register,
                                 "signed":self.signed})
        except NotConstant:
            try:
                instructions = self.left.generate(new_register)
                instructions.append({"op"   :self.operator,
                                     "dest" :result,
                                     "src"  :new_register,
                                     "right":value(self.right),
                                     "signed" :self.signed})
            except NotConstant:
                instructions = self.left.generate(new_register)
                right = self.allocator.new(self.right.size)
                instructions.extend(self.right.generate(right))
                instructions.append({"op"  :self.operator,
                                     "dest":result,
                                     "src" :new_register,
                                     "srcb":right,
                                     "signed":self.signed})
                self.allocator.free(right)
        self.allocator.free(new_register)
        return instructions

    def value(self):
        return eval("%s %s %s"%(value(self.left), self.operator, value(self.right)))

def SizeOf(expression):
    return Constant(expression.size)

class Unary:
    def __init__(self, operator, expression, allocator):
        self.expression = constant_fold(expression)
        self.operator = operator
        self.type_ = self.expression.type_
        self.size = expression.size
        self.signed = expression.signed
        self.allocator = allocator

    def generate(self, result):
        new_register = self.allocator.new(self.size)
        instructions = self.expression.generate(new_register)
        instructions.extend([{"op":self.operator, "dest":result, "src":new_register}])
        self.allocator.free(new_register)
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
        if hasattr(self.function, "return_value"):
            instructions.append({"op"   :"move",
                                 "dest" :result,
                                 "src"  :self.function.return_value})
        return instructions

class Output:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.type_ = "int"
        self.size = expression.size

    def generate(self, result):
        instructions = self.expression.generate(result);
        instructions.append({"op"   :"write", "src"  :result, "output":self.name})
        return instructions

class FileWrite:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.type_ = "int"
        self.size = expression.size

    def generate(self, result):
        instructions = self.expression.generate(result);
        instructions.append({"op"   :"file_write", "src"  :result, "file_name":self.name})
        return instructions

class Input:
    def __init__(self, name):
        self.name = name
        self.type_ = "int"
        self.size = 2
        self.signed = True

    def generate(self, result):
        return [{"op"   :"read", "dest" :result, "input":self.name}]

class FileRead:
    def __init__(self, name):
        self.name = name
        self.type_ = "int"
        self.size = 2
        self.signed = True

    def generate(self, result):
        return [{"op"   :"file_read", "dest" :result, "file_name":self.name}]

class Ready:
    def __init__(self, name):
        self.name = name
        self.type_ = "int"
        self.size = 2
        self.signed = True

    def generate(self, result):
        return [{"op"   :"ready", "dest" :result, "input":self.name}]

class Array:
    def __init__(self, declaration, allocator):
        self.declaration = declaration
        self.allocator = allocator
        self.storage = "register"
        self.type_ = self.declaration.type_
        self.size = int(self.declaration.size) * 2
        self.signed = False

    def generate(self, result):
        instructions = []
        if result != self.declaration.register:
            instructions.append({"op"  :"move",
                                 "dest":result,
                                 "src" :self.declaration.register})
        return instructions

class ArrayIndex:
    def __init__(self, declaration, index_expression, allocator):
        self.declaration = declaration
        self.allocator = allocator
        self.index_expression = index_expression
        self.storage = "memory"
        self.type_  = self.declaration.element_type
        self.size   = self.declaration.element_size
        self.signed = self.declaration.element_signed

    def generate(self, result):
        instructions = []
        offset = self.allocator.new(2)
        address = self.allocator.new(2)
        instructions.extend(self.index_expression.generate(offset))
        instructions.append({"op"    :"+",
                             "dest"  :address,
                             "src"   :offset,
                             "srcb"  :self.declaration.register,
                             "signed":False})
        instructions.append({"op"    :"memory_read_request",
                             "src"   :address,
                             "sequence": id(self),
                             "element_size":self.size})
        instructions.append({"op"    :"memory_read_wait",
                             "src"   :address,
                             "sequence": id(self),
                             "element_size":self.size})
        instructions.append({"op"    :"memory_read",
                             "src"   :address,
                             "dest"  :result,
                             "sequence": id(self),
                             "element_size":self.size})
        self.allocator.free(address)
        self.allocator.free(offset)
        return instructions

class Variable:
    def __init__(self, declaration, allocator):
        self.declaration = declaration
        self.allocator = allocator
        self.storage = "register"
        self.type_ = self.declaration.type_
        self.size = self.declaration.size
        self.signed = self.declaration.signed

    def generate(self, result):
        instructions = []
        if result != self.declaration.register:
            instructions.append({"op"  :"move",
                                 "dest":result,
                                 "src" :self.declaration.register})
        return instructions

class PostIncrement:
    def  __init__(self, operator, lvalue, allocator):
        self.operator = operator
        self.lvalue = lvalue
        self.allocator = allocator
        self.type_ = self.lvalue.declaration.type_
        self.size = self.lvalue.declaration.size
        self.signed = self.lvalue.declaration.signed

    def generate(self, result):

        instructions = []

        instructions.append({"op"    :"move",
                             "src"   :self.lvalue.declaration.register,
                             "dest"  :result})

        instructions.append({"op"    :self.operator,
                             "dest"  :self.lvalue.declaration.register,
                             "right" :1,
                             "src"   :self.lvalue.declaration.register,
                             "signed":self.signed})

        return instructions

class Assignment:
    def __init__(self, lvalue, expression, allocator):
        self.lvalue = lvalue
        self.expression = expression
        self.allocator = allocator
        self.type_ = self.lvalue.type_
        self.size = self.lvalue.size
        self.signed = self.lvalue.signed

    def generate(self, result):
        instructions = self.expression.generate(result)
        if self.lvalue.storage == "register":
            if result != self.lvalue.declaration.register:
                instructions.append({"op"   : "move",
                                     "dest" : self.lvalue.declaration.register,
                                     "src"  : result})

        elif self.lvalue.storage == "memory":
            index = self.allocator.new(2)
            address = self.allocator.new(2)
            instructions.extend(self.lvalue.index_expression.generate(index))
            instructions.append({"op"     :"+",
                                 "dest"   :address,
                                 "src"    :index,
                                 "srcb"   :self.lvalue.declaration.register,
                                 "signed" :self.signed})
            instructions.append({"op"    :"memory_write",
                                 "src"   :address,
                                 "srcb"  :result,
                                 "element_size" :self.lvalue.declaration.element_size})
            self.allocator.free(index)
            self.allocator.free(address)

        return instructions

class Constant:
    def __init__(self, value, size=2, signed=True):
        self._value = value
        self.type_ = "int"
        self.size = size
        self.signed = signed

    def generate(self, result):
        instructions = [{"op":"literal", "dest":result, "literal":self._value}]
        return instructions

    def value(self):
        return self._value
