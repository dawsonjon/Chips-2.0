__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct

class NotConstant(Exception):
    pass


def constant_fold(expression):

    """Replace an expression with a constant if possible"""

    try:
        return Constant(expression.value(), expression.type_(), expression.size(), expression.signed())
    except NotConstant:
        return expression


class Process:

    def generate(self):
        instructions = []

        #generate declarations first
        for declaration in self.functions:
            if hasattr(declaration, "declarations"):
                instructions.extend(declaration.generate())

        instructions.append(
            {"op"   :"jmp_and_link",
             "dest" :self.main.return_address,
             "label":"function_%s"%id(self.main)})

        instructions.append(
            {"op":"stop"})


        #then generate functions. This will ensure that memory has been
        #reserved for globals before functions are compiled.
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
        self.allocator.freeze()
        return instructions


class Break:

    def generate(self): return [
        {"op":"goto", "label":"break_%s"%id(self.loop)}]


class Continue:

    def generate(self): return [
        {"op":"goto", "label":"continue_%s"%id(self.loop)}]


class Assert:

    def generate(self):
        result = self.allocator.new(self.expression.size())
        instructions = self.expression.generate(result, self.allocator)
        self.allocator.free(result)

        instructions.append(
            {"op":"assert", 
             "src":result, 
             "line":self.line, 
             "file":self.filename})

        return instructions


class Return:

    def generate(self):
        if hasattr(self, "expression"):

            result = self.allocator.new(self.function.size)
            instructions=self.function.return_value.copy(
                self.expression, 
                result, 
                self.allocator)
            self.allocator.free(result)

        else:
            instructions = []

        instructions.append(
            {"op":"jmp_to_reg", 
             "src":self.function.return_address})

        return instructions


class Report:

    def generate(self):
        result = self.allocator.new(self.expression.size())
        instructions = self.expression.generate(result, self.allocator)
        self.allocator.free(result)

        if self.expression.size() == 4:
            if self.expression.type_() == "float":
                instructions.append(
                    {"op":"float_report",
                     "src":result,
                     "line":self.line,
                     "file":self.filename})
            else:
                if self.expression.signed():
                            instructions.append(
                            {"op":"unsigned_report",
                             "src":result,
                             "line":self.line,
                             "file":self.filename,})
                else:
                            instructions.append(
                            {"op":"report",
                             "src":result,
                             "line":self.line,
                             "file":self.filename,})

        elif self.expression.size() == 8:

            if self.expression.type_() == "float":
                instructions.append(
                    {"op":"long_float_report",
                     "src":result,
                     "line":self.line,
                     "file":self.filename})
            else:
                if self.expression.signed():
                            instructions.append(
                            {"op":"long_report",
                             "src":result,
                             "line":self.line,
                             "file":self.filename,})
                else:
                            instructions.append(
                            {"op":"long_unsigned_report",
                             "src":result,
                             "line":self.line,
                             "file":self.filename,})

        return instructions


class WaitClocks:

    def generate(self):
        result = self.allocator.new(self.expression.size())
        instructions = self.expression.generate(result, self.allocator)
        self.allocator.free(result)
        instructions.append({"op":"wait_clocks", "src":result})
        return instructions


class If:

    def generate(self):

        try:

            if self.expression.value():
                return self.true_statement.generate()
            else:
                if self.false_statement:
                    return self.false_statement.generate()
                else:
                    return []

        except NotConstant:

            result = self.allocator.new(self.expression.size())
            instructions = []
            instructions.extend(self.expression.generate(result, self.allocator))

            if self.expression.size() == 8:
                instructions.append(
                    {"op"    : "or",
                     "src"   : result,
                     "srcb"   : result + 1,
                     "dest" : result})

            instructions.append(
                {"op"    : "jmp_if_false",
                 "src"   : result,
                 "label" : "else_%s"%id(self)})

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
        result = self.allocator.new(self.expression.size())
        test = self.allocator.new(self.expression.size())
        instructions = self.expression.generate(result, self.allocator)
        for value, case in self.cases.iteritems():

            instructions.append({
                "op":"literal", 
                "dest":test, 
                "literal":value & 0xffffffff,
                 })

            instructions.append({
                "op":"equal", 
                "dest":test, 
                "src":result, 
                "srcb":test
                })

            if self.expression.size() == 8:

                instructions.append({
                    "op":"literal", 
                    "dest":test + 1, 
                    "literal":(value >> 32) & 0xffffffff
                    })

                instructions.append({
                    "op":"equal", 
                    "dest":test + 1, 
                    "src":result + 1, 
                    "srcb":test + 1
                    })

                instructions.append({
                    "op":"and", 
                    "dest":test, 
                    "src": test, 
                    "srcb": test + 1
                    })

            instructions.append({
                "op":"jmp_if_true", 
                "src":test, 
                "label":"case_%s"%id(case)
                })

        if hasattr(self, "default"):

            instructions.append({
                "op":"goto", 
                "label":"case_%s"%id(self.default)
                })

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
            result = self.allocator.new(self.expression.size())

            instructions.extend(
                self.expression.generate(result, self.allocator))

            if self.expression.size() == 8:
                instructions.append({
                    "op"    : "or",
                    "src"   : result,
                    "srcb"   : result + 1,
                    "dest" : result
                    })

            instructions.append({
                "op":"jmp_if_false", 
                "src":result, 
                "label":"end_%s"%id(self)
                })

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

    def __init__(self, allocator, initializer, name, type_, size, signed, const):
        self.initializer = initializer
        self.allocator = allocator
        self._type = type_
        self._size = size
        self._signed = signed
        self._const = const
        self.name = name

    def instance(self):
        register = self.allocator.new(self.size(), "variable "+self.name)

        return VariableInstance(
            register, 
            self.initializer, 
            self.type_(), 
            self.size(), 
            self.signed(), 
            self.const(),
            self.allocator)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class VariableInstance:

    def __init__(self, register, initializer, type_, size, signed, const, allocator):
        self.register = register
        self._type = type_
        self.initializer = initializer
        self._size = size
        self._signed = signed
        self._const = const
        self.allocator = allocator

    def generate(self):
        return self.initializer.generate(self.register, self.allocator)

    def reference(self):
        return Variable(self)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def argument_size(self):
        return self.size()

    def signed(self):
        return self._signed

    def const(self):
        return self._const


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
        self._type = type_
        self._size = size * element_size
        self._signed = False
        self.element_type = element_type
        self.element_size = element_size
        self.element_signed = element_signed
        self.initializer = initializer
        self.initialize_memory = initialize_memory

    def instance(self):

        location = self.allocator.new_array(
            self.size(), 
            self.initializer)

        register = self.allocator.new(4, "array")

        return ArrayInstance(
            location,
            register,
            self.size(),
            self.type_(),
            self.initializer,
            self.initialize_memory,
            self.element_type,
            self.element_size,
            self.element_signed)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed

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
        self._type = type_
        self._size = size
        self._signed = False
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
            location=self.location 
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

        return instructions


    def reference(self):
        return Array(self)

    def type_(self):
        return self._type

    def size(self):
        return self._size


    def signed(self):
        return self._signed


class StructDeclaration:

    def __init__(self, members):
        self.members = members
        self._type = "struct {%s}"%"; ".join(
            [i.type_() for i in members.values()])
        self._size = sum([i.size() for i in members.values()])
        self._signed = False

    def instance(self):
        instances = {}
        for name, declaration in self.members.iteritems():
            instances[name] = declaration.instance()
        return StructInstance(instances)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed


class StructInstance:

    def __init__(self, members):
        self.members = members
        self._type = "struct {%s}"%"; ".join(
            [i.type_() for i in members.values()])
        self._size = sum([i.size() for i in members.values()])
        self._signed = False

    def generate(self):
        instructions = []
        for member in self.members.values():
            instructions.extend(member.generate())
        return instructions

    def reference(self):
        return Struct(self)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed


class DiscardExpression:

    def __init__(self, expression, allocator):
        self.expression = expression
        self.allocator = allocator

    def generate(self):
        result = self.allocator.new(self.expression.size())
        instructions = self.expression.generate(result, self.allocator)
        self.allocator.free(result)
        return instructions


class Expression:

    def __init__(self, t, size, signed):
        self.type_var=t
        self.size_var=size
        self.signed_var=signed

    def type_(self):
        return self.type_var

    def size(self):
        return self.size_var

    def argument_size(self):
        return self.size_var

    def signed(self):
        return self.signed_var

    def value(self):
        raise NotConstant

    def const(self):
        return True

    def int_value(self):
        if self.type_() == "float":
            if self.size() == 8:
                byte_value = struct.pack(">d", self.value())
                value  = ord(byte_value[0]) << 56
                value |= ord(byte_value[1]) << 48
                value |= ord(byte_value[2]) << 40
                value |= ord(byte_value[3]) << 32
                value |= ord(byte_value[4]) << 24
                value |= ord(byte_value[5]) << 16
                value |= ord(byte_value[6]) << 8
                value |= ord(byte_value[7])
                return value
            elif self.size() == 4:
                byte_value = struct.pack(">f", self.value())
                value  = ord(byte_value[0]) << 24
                value |= ord(byte_value[1]) << 16
                value |= ord(byte_value[2]) << 8
                value |= ord(byte_value[3])
                return value
        else:
            return int(self.value())


class Object(Expression):

    def __init__(self, instance):
        Expression.__init__(self, instance.type_(), instance.size(), instance.signed())
        self.instance = instance

    def value(self):
        raise NotConstant

    def const(self):
        return False


def AND(left, right):
    return ANDOR(left, right, "jmp_if_false")


def OR(left, right):
    return ANDOR(left, right, "jmp_if_true")


class ANDOR(Expression):

    def __init__(self, left, right, op):
        self.left = constant_fold(left)
        self.right = constant_fold(right)
        self.op = op

        Expression.__init__(
            self, 
            "int", 
            max(left.size(), right.size()), 
            left.signed() and right.signed())

    def generate(self, result, allocator):
        instructions = self.left.generate(result, allocator)
        if self.left.size() == 8:
            temp = allocator.new(4)
            instructions.append(
                {"op"    : "or",
                 "src"   : result,
                 "srcb"   : result + 1,
                 "dest" : temp})
            instructions.append({"op":self.op, "src":temp, "label":"end_%s"%id(self)})
            allocator.free(temp)
        elif self.left.size() == 4:
            instructions.append({"op":self.op, "src":result, "label":"end_%s"%id(self)})
        instructions.extend(self.right.generate(result, allocator))
        instructions.append({"op":"label", "label":"end_%s"%id(self)})
        return instructions

    def value(self):
        if self.op == "jmp_if_false":
            return self.left.value() and self.right.value()
        else:
            return self.left.value() or self.right.value()


def get_binary_type(left, right, operator):

    """
    Given the type of the left and right hand operators, determine the type
    of the resulting value.
    """

    binary_types = {
        "==" : ("int", 4, True),
        "!=" : ("int", 4, True),
        "<"  : ("int", 4, True),
        ">"  : ("int", 4, True),
        "<=" : ("int", 4, True),
        ">=" : ("int", 4, True),
        }

    signature = ",".join([operator])
    if signature in binary_types:
        type_, size, signed = binary_types[signature]
    else:
        type_ = left.type_()
        size = max(left.size(), right.size())
        signed = left.signed() and right.signed()

    return type_, size, signed

class Binary(Expression):

    def __init__(self, operator, left, right):
        self.left = constant_fold(left)
        self.right = constant_fold(right)
        self.operator = operator
        type_, size, signed = get_binary_type(left, right, operator)

        Expression.__init__(
            self, 
            type_, 
            size, 
            signed)

    def generate(self, result, allocator):
        left = allocator.new(self.left.size())
        instructions = self.left.generate(left, allocator)
        right = allocator.new(self.right.size())
        instructions.extend(self.right.generate(right, allocator))

        operation, reverse_operands = select_binary_instruction(
            self.left.size(), 
            self.right.size(), 
            self.type_(), 
            self.left.signed(), 
            self.right.signed(), 
            self.operator)

        if reverse_operands:

            instructions.append({
                "op"  :operation,
                "dest":result,
                "src" :right,
                "srcb":left,
                })

        else:

            instructions.append({
                "op"  :operation,
                "dest":result,
                "src" :left,
                "srcb":right
                })

        allocator.free(right)
        allocator.free(left)
        return instructions

    def value(self):

        if self.type_() == "int":

            return int(eval("%s %s %s"%(
                self.left.value(), 
                self.operator, 
                self.right.value())))

        else:

            return float(eval("%s %s %s"%(
                self.left.value(), 
                self.operator, 
                self.right.value())))


def SizeOf(expression):
    return Constant(expression.size())

class IntToLong(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 8, expression.signed())

    def generate(self, result, allocator):
        new_register = allocator.new(4)
        instructions = self.expression.generate(new_register, allocator)

        if self.expression.signed():
            instructions.extend([{
                "op"   : "int_to_long", 
                "dest" : result, 
                "src"  : new_register
                }])
        else:
            instructions.extend([{
                "op"   : "unsigned_int_to_long", 
                "dest" : result, 
                "src"  : new_register
                }])

        allocator.free(new_register)
        return instructions

    def value(self):
        return self.expression.value()

class LongToInt(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 4, expression.signed())

    def generate(self, result, allocator):
        instructions = self.expression.generate(result, allocator)
        return instructions

    def value(self):
        return self.expression.value()

class IntToFloat(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 4, True)

    def generate(self, result, allocator):
        new_register = allocator.new(self.size())
        instructions = self.expression.generate(new_register, allocator)

        instructions.extend([{
            "op"   : "int_to_float", 
            "dest" : result, 
            "src"  : new_register
            }])

        allocator.free(new_register)
        return instructions

    def value(self):
        return float(self.expression.value())


class FloatToInt(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 4, True)

    def generate(self, result, allocator):
        new_register = allocator.new(self.size())
        instructions = self.expression.generate(new_register, allocator)

        instructions.extend([{
            "op"   : "float_to_int", 
            "dest" : result, 
            "src"  : new_register
            }])

        allocator.free(new_register)
        return instructions

    def value(self):
        return int(self.expression.value())

class DoubleToLong(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 8, True)

    def generate(self, result, allocator):
        new_register = allocator.new(8)
        instructions = self.expression.generate(new_register, allocator)

        instructions.append({
            "op"   : "load_hi", 
            "src"  : new_register+1, 
            "srcb" : new_register+1
            })
        instructions.append({
            "op"   : "double_to_long", 
            "dest" : result, 
            "src"  : new_register
            })
        instructions.append({
            "op"   : "result_hi", 
            "dest" : result+1, 
            })

        allocator.free(new_register)
        return instructions

    def value(self):
        return int(self.expression.value())

class LongToDouble(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 8, True)

    def generate(self, result, allocator):
        new_register = allocator.new(8)
        instructions = self.expression.generate(new_register, allocator)

        instructions.append({
            "op"   : "load_hi", 
            "src"  : new_register+1, 
            "srcb" : new_register+1
            })
        instructions.append({
            "op"   : "long_to_double", 
            "dest" : result, 
            "src"  : new_register
            })
        instructions.append({
            "op"   : "result_hi", 
            "dest" : result+1, 
            })

        allocator.free(new_register)
        return instructions

    def value(self):
        return int(self.expression.value())

class DoubleToFloat(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 4, True)

    def generate(self, result, allocator):
        new_register = allocator.new(8)
        instructions = self.expression.generate(new_register, allocator)

        instructions.append({
            "op"   : "load_hi", 
            "src"  : new_register+1, 
            "srcb" : new_register+1
            })
        instructions.append({
            "op"   : "double_to_float", 
            "dest" : result, 
            "src"  : new_register
            })

        allocator.free(new_register)
        return instructions

    def value(self):
        return int(self.expression.value())

class FloatToDouble(Expression):

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 8, True)

    def generate(self, result, allocator):
        new_register = allocator.new(8)
        instructions = self.expression.generate(new_register, allocator)

        instructions.append({
            "op"   : "float_to_double", 
            "dest" : result, 
            "src"  : new_register
            })
        instructions.append({
            "op"   : "result_hi", 
            "dest" : result+1, 
            })

        allocator.free(new_register)
        return instructions

    def value(self):
        return int(self.expression.value())


class Unary(Expression):

    def __init__(self, operator, expression):
        self.expression = constant_fold(expression)
        self.operator = operator

        Expression.__init__(
            self, 
            expression.type_(), 
            expression.size(), 
            expression.signed())

    def generate(self, result, allocator):
        new_register = allocator.new(self.size())
        instructions = self.expression.generate(new_register, allocator)

        assert self.operator == "~"
        instructions.extend([{
            "op":"not", 
            "dest":result, 
            "src":new_register,
            }])

        allocator.free(new_register)
        return instructions

    def value(self):
        return eval("%s%s"%(self.operator, self.expression.value()))


class FunctionCall(Expression):

    def __init__(self, function):
        self.function = function

        Expression.__init__(
            self, 
            function.type_, 
            function.size, 
            function.signed)

    def generate(self, result, allocator):
        instructions = []

        for expression, argument in zip(
                self.arguments, 
                self.function.arguments):

            temp_register = allocator.new(expression.argument_size())

            instructions.extend(
                argument.copy(expression, temp_register, allocator))

            allocator.free(temp_register)

        instructions.append({
            "op"   :"jmp_and_link",
            "dest" :self.function.return_address,
            "label":"function_%s"%id(self.function)
            })

        if hasattr(self.function, "return_value"):

            instructions.extend(self.function.return_value.generate(
                result, 
                allocator))


        return instructions


class Output(Expression):

    def __init__(self, handle, expression):
        self.handle = handle
        self.expression = expression
        Expression.__init__(self, "int", 4, False)

    def generate(self, result, allocator):
        temp1 = allocator.new(4)
        instructions = self.handle.generate(temp1, allocator)
        instructions.extend(self.expression.generate(result, allocator))

        instructions.append({
            "op"   : "write", 
            "src"  : temp1, 
            "srcb" : result
            })

        allocator.free(temp1)
        return instructions


class FileWrite(Expression):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        Expression.__init__(
            self, 
            expression.type_(), 
            expression.size(), 
            expression.signed())

    def generate(self, result, allocator):
        instructions = self.expression.generate(result, allocator)

        if self.expression.type_() == "float" and self.expression.size() == 8:
            instructions.append({
                "op"        : "long_float_file_write", 
                "src"       : result, 
                "file_name" : self.name,
                })
        elif self.expression.type_() == "float" and self.expression.size() == 4:
            instructions.append({
                "op"        : "float_file_write", 
                "src"       : result, 
                "file_name" : self.name,
                })
        else:
            instructions.append({
                "op"        : "file_write", 
                "src"       : result, 
                "file_name" : self.name,
                })

        return instructions


class Input(Expression):

    def __init__(self, handle):
        self.handle = handle
        Expression.__init__(self, "int", 4, False)

    def generate(self, result, allocator):
        temp1 = allocator.new(4)
        instructions = self.handle.generate(temp1, allocator)

        instructions.append({
            "op"   : "read",
            "src"  : temp1,
            "dest" : result
            })

        allocator.free(temp1)
        return instructions


class FileRead(Expression):

    def __init__(self, name):
        self.name = name
        Expression.__init__(self, "int", 4, True)

    def generate(self, result, allocator):
        return [{"op"   :"file_read", "dest" :result, "file_name":self.name}]


class Ready(Expression):

    def __init__(self, handle):
        self.handle = handle
        Expression.__init__(self, "int", 4, False)

    def generate(self, result, allocator):
        temp1 = allocator.new(4)
        instructions = self.handle.generate(temp1, allocator)

        instructions.append({
            "op"   :"ready", 
            "src"  : temp1,
            "dest" :result
            })

        allocator.free(temp1)
        return instructions


class Struct(Object):

    def __init__(self, instance):
        Object.__init__(self, instance)

    def generate(self, result, allocator):
        instructions = []
        if result != self.declaration.register:

            instructions.append({
                "op"  :"move",
                "dest":result,
                "src" :self.declaration.register
                })

        return instructions

    def copy(self, expression, result, allocator):
        instructions = []

        for lvalue, rvalue in zip(
            self.instance.members.values(), 
            expression.instance.members.values()):

            instructions.extend(
                lvalue.reference().copy(rvalue.reference(), result, allocator))

        return instructions


class Array(Object):

    def __init__(self, instance):
        Object.__init__(self, instance)

    def generate(self, result, allocator):
        instructions = []
        if result != self.instance.register:

            instructions.append({
                "op"   : "move",
                "dest" : result,
                "src"  : self.instance.register
                })

        return instructions

    def copy(self, expression, result, allocator):
        instructions = expression.generate(result, allocator)
        if result != self.instance.register:

            instructions.append({
                "op"   : "move",
                "dest" : self.instance.register,
                "src"  : result
                })

        return instructions

    def argument_size(self):
        return 4


class ConstArray(Object):

    def __init__(self, instance):
        Object.__init__(self, instance)

    def generate(self, result, allocator):
        instructions = []
        #If initialize memory is true, the memory content will initialised (as at configuration time)
        #If initialize memory is false, then the memory will need to be filled by the program.
        if not self.instance.initialize_memory and self.instance.initializer is not None:
            location = self.instance.location
            for value in self.instance.initializer:

                instructions.append({
                    "op":"memory_write_literal",
                    "address":location,
                    "value":value & 0xffffffff,
                    })

                location += 1

                if self.size() == 8:

                    instructions.append({
                        "op":"memory_write_literal",
                        "address":location,
                        "value":value >> 32,
                        })

                    location += 1



        instructions.append({
            "op":"literal",
            "literal":self.instance.location,
            "dest":self.instance.register,
            })

        if result != self.instance.register:

            instructions.append({
                "op"   : "move",
                "dest" : result,
                "src"  : self.instance.register,
                })

        return instructions

    def copy(self, expression, result, allocator):
        instructions = expression.generate(result, allocator)
        if result != self.instance.register:

            instructions.append({
                "op"   : "move",
                "dest" : self.instance.register,
                "src"  : result,
                })

        return instructions

    def argument_size(self):
        return 4


class ArrayIndex(Object):

    def __init__(self, instance, index_expression):
        Object.__init__(self, instance)
        assert self.type_var.endswith("[]")
        self.type_var = self.type_var[:-2]
        self.size_var = instance.element_size
        self.index_expression = index_expression

    def generate(self, result, allocator):
        instructions = []
        address = allocator.new(4)
        blocks_reg = allocator.new(4)
        one = allocator.new(4)

        blocks = self.instance.element_size//4

        instructions.extend(self.index_expression.generate(address, allocator))


        instructions.append({
            "op"      :"literal",
            "literal" :blocks,
            "dest"    :blocks_reg,
            })

        instructions.append({
            "op"      : "multiply",
            "src"     : blocks_reg,
            "srcb"    : address,
            "dest"    : address,
            })

        instructions.append({
            "op"    :"add",
            "dest"  :address,
            "src"   :address,
            "srcb"  :self.instance.register,
            })

        instructions.append({
            "op"      :"literal",
            "literal" :1,
            "dest"    :one,
            })


        for i in range(blocks):

            instructions.append({
                "op"    :"memory_read_request",
                "src"   :address,
                "sequence": str(id(self)) + str(i),
                })

            instructions.append({
                "op"    :"memory_read_wait",
                "src"   :address,
                "sequence": str(id(self)) + str(i),
                })

            instructions.append({
                "op"    :"memory_read",
                "src"   :address,
                "dest"  :result+i,
                "sequence": str(id(self)) + str(i),
                })

            #no need to increment the last time round
            if i+1 == blocks:
                break

            instructions.append({
                "op"     :"add",
                "srcb"   :one,
                "dest"   :address,
                "src"    :address,
                })

        allocator.free(address)
        allocator.free(one)
        allocator.free(blocks_reg)
        return instructions

    def copy(self, expression, result, allocator):
        address = allocator.new(4)
        one = allocator.new(4)
        blocks_reg = allocator.new(4)

        blocks = self.instance.element_size//4

        instructions = expression.generate(result, allocator)
        instructions.extend(self.index_expression.generate(address, allocator))


        instructions.append({
            "op"      :"literal",
            "literal" :blocks,
            "dest"    :blocks_reg,
            })

        instructions.append({
            "op"      : "multiply",
            "src"     : blocks_reg,
            "srcb"    : address,
            "dest"    : address,
            })

        instructions.append({
            "op"     :"add",
            "dest"   :address,
            "src"    :address,
            "srcb"   :self.instance.register,
            })

        instructions.append({
            "op"      :"literal",
            "literal" :1,
            "dest"    :one,
            })
        
        for i in range(blocks):

            instructions.append({
                "op"    :"memory_write",
                "src"   :address,
                "srcb"  :result + i
                })

            #no need to increment the last time round
            if i+1 == blocks:
                break

            instructions.append({
                "op"     :"add",
                "srcb"   :one,
                "dest"   :address,
                "src"    :address
                })

        allocator.free(address)
        allocator.free(one)
        allocator.free(blocks_reg)
        return instructions


class Variable(Object):
    def __init__(self, instance):
        Object.__init__(self, instance)

    def generate(self, result, allocator):
        instructions = []
        if result != self.instance.register:

            instructions.append({
                "op"  :"move",
                "dest":result,
                "src" :self.instance.register
                })

            if self.size() == 8:
                instructions.append({
                    "op"  :"move",
                    "dest":result+1,
                    "src" :self.instance.register+1
                    })

        return instructions

    def copy(self, expression, result, allocator):
        instructions = expression.generate(result, allocator)
        if result != self.instance.register:

            instructions.append({
                "op"   : "move",
                "dest" : self.instance.register,
                "src"  : result
                })

            if self.size() == 8:

                instructions.append({
                    "op"   : "move",
                    "dest" : self.instance.register+1,
                    "src"  : result+1
                    })

        return instructions

    def const(self):
        return self.instance.const()

    def value(self):
        if self.const():
            return self.instance.initializer.value()
        else:
            raise NotConstant


class PostIncrement(Expression):

    def  __init__(self, operator, lvalue, allocator):
        self.operator = operator
        self.lvalue = lvalue
        allocator = allocator
        Expression.__init__(self, lvalue.type_(), lvalue.size(), lvalue.signed())

    def generate(self, result, allocator):

        instructions = []

        instructions.append({
             "op"    : "move",
             "src"   : self.lvalue.instance.register,
             "dest"  : result,
         })

        #FIXME Does this work for longs?
        temp = allocator.new(4)
        instructions.append({
             "op"      : "literal",
             "literal" : 1,
             "dest"    : temp,
         })

        increment_instruction = select_increment_instruction(
            self.lvalue.size(), 
            self.lvalue.type_(), 
            self.lvalue.signed(), 
            self.operator,
        )

        instructions.append({
             "op"    : increment_instruction,
             "dest"  : self.lvalue.instance.register,
             "src"   : self.lvalue.instance.register,
             "srcb"  : temp,
        })
        allocator.free(temp)

        return instructions


class Assignment(Expression):

    def __init__(self, lvalue, expression, allocator):
        Expression.__init__(self, lvalue.type_(), lvalue.size(), lvalue.signed())
        self.lvalue = lvalue
        self.expression = expression
        self.allocator = allocator

    def generate(self, result, allocator):
        return self.lvalue.copy(self.expression, result, allocator)


class Constant(Expression):

    def __init__(self, value, type_="int", size=4, signed=True):
        self._value = value
        Expression.__init__(self, type_, size, signed)

    def generate(self, result, allocator):

        int_value = self.int_value()

        instructions = [{
            "op":"literal", 
            "dest":result, 
            "signed":self.signed(),
            "literal":int_value & 0xffffffff}]

        if self.size() == 8:

            instructions.append({
                "op":"literal", 
                "dest":result + 1, 
                "signed":self.signed(),
                "literal":(int_value >> 32) & 0xffffffff})

        return instructions

    def value(self):
       return self._value

def select_binary_instruction(left_size, right_size, type_, left_signed, right_signed, operation):
    operation_names = {
        "+"  : ("add", False, False),
        "-"  : ("subtract", False, False),
        "/"  : ("divide", False, True),
        "*"  : ("multiply", False, False),
        "%"  : ("modulo", False, False),
        ">"  : ("greater", False, True),
        ">=" : ("greater_equal", False, True),
        "<"  : ("greater", True, True),
        "<=" : ("greater_equal", True, True),
        ">>" : ("shift_right", False, True),
        "<<" : ("shift_left", False, False),
        "&"  : ("and", False, False),
        "|"  : ("or", False, False),
        "^"  : ("xor", False, False),
        "==" : ("equal", False, False),
        "!=" : ("not_equal", False, False)
        }

    name, reverse_operands, sign_sensitive = operation_names[operation]

    if type_ == "float":
        name = "float_" + name

    if left_size == 8 or right_size == 8:
        name = "long_" + name    

    if sign_sensitive and not (left_signed and right_signed):
        name = "unsigned_" + name    

    return name, reverse_operands

def select_increment_instruction(size, type_, signed, operation):
    operation_names = {
        "+"  : "add",
        "-"  : "subtract"}

    name = operation_names[operation]

    if type_ == "float":
        name = "float_" + name

    if size == 8:
        name = "long_" + name    

    return name
