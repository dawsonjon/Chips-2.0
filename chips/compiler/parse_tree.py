__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct
from itertools import chain
from register_map import *
from instruction_utils import *
from instruction_utils import _return

class NotConstant(Exception):

    """This expression gets raised when a non-constant ...
    
    expression is evaluated at compile time.

    """

    pass

def flatten(sequence):

    """Turn a list containing other lists into a single list"""

    try:
        l = []
        for i in sequence:
            l.extend(flatten(i))
    except:
        l = sequence
    return l

def constant_fold(expression):

    """Replace an expression with a constant if possible"""

    try:
        return Constant(
            expression.value(), 
            expression.type_(), 
            expression.size(), 
            expression.signed()
        )
    except NotConstant:
        return expression

def bits_to_float(bits):

    """convert integer containing the ieee 754 representation into a float"""

    byte_string = (
        chr((bits & 0xff000000) >> 24) +
        chr((bits & 0xff0000) >> 16) +
        chr((bits & 0xff00) >> 8) +
        chr((bits & 0xff))
    )
    return struct.unpack(">f", byte_string)[0]

def bits_to_double(bits):

    """convert integer containing the ieee 754 representation into a float"""

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

class Process:

    """A process is a whole C program.
    
    Within a chip there may more than one process.
    
    """

    def generate(self):

        called_functions = []
        referenced_globals = []
        def find_functions(function):
            if function not in called_functions:
                called_functions.append(function)
                for global_object in function.referenced_globals:
                    if global_object not in referenced_globals:
                        referenced_globals.append(global_object)
            for i in function.called_functions:
                if i not in called_functions:
                    find_functions(i)
        find_functions(self.main)

        instructions = []
        instructions.append({"op":"literal", "z":tos, "literal":0})
        instructions.append({"op":"literal", "z":frame, "literal":0})

        #reserve stack space for global objects and function return values
        globals_and_functions = set(called_functions + referenced_globals)
        global_size = sum([i.size() for i in globals_and_functions])
        if global_size:
            instructions.append({"op":"addl", "z":tos, "a":tos, "literal":global_size//4})
        offset = 0
        for global_object in globals_and_functions:
            instructions.extend(global_object.initialise(offset))
            offset += global_object.size()//4

        #start with a call to main
        call(instructions, "function_%s"%id(self.main))

        #then stop
        instructions.append(
            {"op":"stop"})

        #then generate functions. This will ensure that memory has been
        #reserved for globals before functions are compiled.
        for function in called_functions:
            instructions.extend(function.generate())

        return instructions


class Function:

    """A Function Object"""

    def __init__(self, name, type_, size, signed):
        self.offset = 0
        self.local = False
        self.name = name
        self._type_ = type_
        self._size = size
        self._signed = signed
        self.called_functions = []
        self.referenced_globals = []

    def generate(self):
        instructions = []
        instructions.append({
            "op":"label", 
            "label":"function_%s"%id(self),
        })
        instructions.append({
            "op"   :"addl",
            "z" : tos,
            "a" : tos,
            "literal":self.offset,
        })
        instructions.extend(self.statement.generate())
        if not hasattr(self, "return_statement"):
            _return(instructions)
        return instructions

    def initialise(self, offset):
        self.return_pointer = offset
        return []

    def reference(self):
        return self

    def size(self):
        return self._size

    def type_(self):
        return self._type_

    def signed(self):
        return self._signed


class Break:

    """Exit a loop or case statement"""

    def generate(self): return [{
        "op":"goto", 
        "label":"break_%s"%id(self.loop)
    }]


class Continue:

    """go straight to the next loop iteration"""

    def generate(self): return [{
        "op":"goto", 
        "label":"continue_%s"%id(self.loop)
     }]


class Assert:

    """ if an expression evaluates to false, raise an error """

    def generate(self):
        instructions = self.expression.generate()
        instructions.append({
            "op":"assert",
            "a":result,
            "line":self.line,
            "file":self.filename,
        })

        return instructions


class Return:

    """ return from a function """

    def generate(self):
        instructions = []
        if hasattr(self, "expression"):
            instructions.extend(self.expression.generate())
            store_object(
                instructions, 
                n=self.function.size()//4, 
                offset=self.function.return_pointer,
                local=False
            )
        _return(instructions)

        return instructions


class Report:

    """ report the value of an exression - simulation only """

    def generate(self):
        instructions = self.expression.generate()

        if self.expression.size() == 4:
            instructions.append({
                "op":"a_lo",
                "z":result,
                "a":result,
            })
            if self.expression.type_() == "float":
                instructions.append({
                    "op":"float_report",
                    "line":self.line,
                    "file":self.filename
                })
            else:
                if self.expression.signed():
                    instructions.append({
                        "op":"report",
                        "line":self.line,
                        "file":self.filename,
                    })
                else:
                    instructions.append({
                        "op":"unsigned_report",
                        "line":self.line,
                        "file":self.filename,
                    })

        elif self.expression.size() == 8:

            instructions.append({
                "op":"a_hi",
                "a":result_hi,
                "z":result_hi,
            })
            instructions.append({
                "op":"a_lo",
                "a":result,
                "z":result,
            })
            if self.expression.type_() == "float":
                instructions.append({
                    "op":"long_float_report",
                    "line":self.line,
                    "file":self.filename,
                })
            else:
                if self.expression.signed():
                    instructions.append({
                        "op":"long_report",
                        "line":self.line,
                        "file":self.filename,
                    })
                else:
                    instructions.append({
                        "op":"long_unsigned_report",
                        "line":self.line,
                        "file":self.filename,
                    })

        return instructions


class WaitClocks:

    """ stop execution for n clock cycles """

    def generate(self):
        instructions = self.expression.generate()
        instructions.append({"op":"wait_clocks", "a":result})
        return instructions


class If:

    """ if statement """

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
            instructions = []
            instructions.extend(self.expression.generate())
            if self.expression.size() == 8:
                instructions.append({
                    "op":"or",
                    "z":result,
                    "a":result,
                    "b":result_hi,
                })
            instructions.append({
                "op"    : "jmp_if_false",
                "a"     : result,
                "label" : "else_%s"%id(self),
            })
            instructions.extend(self.true_statement.generate())
            instructions.append({
                "op":"goto", 
                "label":"end_%s"%id(self)
            })
            instructions.append({"op":"label", "label":"else_%s"%id(self)})
            if self.false_statement:
                instructions.extend(self.false_statement.generate())
            instructions.append({"op":"label", "label":"end_%s"%id(self)})
            return instructions


class Switch:

    """ switch statment """

    def generate(self):
        instructions = []
        instructions.extend(self.expression.generate())
        if self.expression.size() == 4:
            for value, case in self.cases.iteritems():
                instructions.append({
                    "op":"literal",
                    "z":temp,
                    "literal" : value & 0xffffffff,
                })
                instructions.append({
                    "op":"equal",
                    "a":result,
                    "b":temp,
                    "z":temp
                })
                instructions.append({
                    "op":"jmp_if_true",
                    "label":"case_%s"%id(case),
                    "a":temp,
                })
        else:
            for value, case in self.cases.iteritems():
                instructions.append({
                    "op":"literal",
                    "z":temp,
                    "literal" : value & 0xffffffff,
                })
                instructions.append({
                    "op":"literal",
                    "z":temp1,
                    "literal" : (value >> 32) & 0xffffffff,
                })
                instructions.append({
                    "op":"equal",
                    "a":result,
                    "b":temp,
                    "z":temp
                })
                instructions.append({
                    "op":"equal",
                    "a":result_hi,
                    "b":temp1,
                    "z":temp1
                })
                instructions.append({
                    "op":"and",
                    "a":temp,
                    "b":temp1,
                    "z":temp
                })
                instructions.append({
                    "op":"jmp_if_true",
                    "label":"case_%s"%id(case),
                    "a":temp,
                })

        if hasattr(self, "default"):
            instructions.append({
                "op":"goto",
                "label":"case_%s"%id(self.default)
            })
        instructions.append({
            "op":"goto",
            "label":"break_%s"%id(self),
        })

        instructions.extend(self.statement.generate())
        instructions.append({"op":"label", "label":"break_%s"%id(self)})
        return instructions


class Case:

    """ case statment """

    def generate(self):
        instructions = []
        instructions.append({
            "op":"label",
            "label":"case_%s"%id(self),
        })
        return instructions


class Default:

    """ default case statment """

    def generate(self):
        return [{"op":"label", "label":"case_%s"%id(self)}]


class Loop:

    """ A loop while or do-while are synthesised from this """

    def generate(self):
        instructions = [{"op":"label", "label":"begin_%s"%id(self)}]
        instructions.append({"op":"label", "label":"continue_%s"%id(self)})
        instructions.extend(self.statement.generate())
        instructions.append({
            "op":"goto", 
            "label":"begin_%s"%id(self)
        })
        instructions.append({"op":"label", "label":"break_%s"%id(self)})
        return instructions

class For:

    """ A for loop """

    def generate(self):
        instructions = []
        if hasattr(self, "statement1"):
            instructions.extend(self.statement1.generate())
        instructions.append({"op":"label", "label":"begin_%s"%id(self)})
        if hasattr(self, "expression"):

            instructions.extend(self.expression.generate())
            if self.expression.size() == 8:
                instructions.append({
                    "op":"or",
                    "z":result,
                    "a":result,
                    "b":result_hi,
                    })
            instructions.append({
                "op":"jmp_if_false",
                "a":result,
                "label":"end_%s"%id(self)
                })

        instructions.extend(self.statement3.generate())
        instructions.append({"op":"label", "label":"continue_%s"%id(self)})
        if hasattr(self, "statement2"):
            instructions.extend(self.statement2.generate())
        instructions.append({
            "op":"goto", 
            "label":"begin_%s"%id(self)
        })
        instructions.append({"op":"label", "label":"end_%s"%id(self)})
        instructions.append({"op":"label", "label":"break_%s"%id(self)})
        return instructions


class Block:

    """ a block of statements enclosed by braces """

    def generate(self):
        instructions = []
        for statement in self.statements:
            instructions.extend(statement.generate())
        return instructions


class CompoundDeclaration:

    """ more than one declaration on the same line """

    def __init__(self, declarations):
        self.declarations = declarations

    def generate(self):
        instructions = []
        for declaration in self.declarations:
            instructions.extend(declaration.generate());
        return instructions


class VariableDeclaration:

    """ variable declaration """

    def __init__(self, name, type_, size, signed, const):
        self._type = type_
        self._size = size
        self._signed = signed
        self._const = const
        self.name = name
        self.initializer = Constant(0, type_, size, signed)

    def instance(self, function):

        if hasattr(function, "is_global"):
            local = False
        else:
            local = True

        offset = function.offset
        function.offset += self.size()//4

        return VariableInstance(
            local,
            offset,
            self.initializer,
            self.type_(),
            self.size(),
            self.signed(),
            self.const())

    def argument_instance(self, function):
        return self.instance(function)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def argument_size(self):
        return self._size

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class VariableInstance:

    """ instance of a variable """

    def __init__(self, local, offset, initializer, type_, size, signed, const):
        self.local = local
        self.offset = offset
        self._type = type_
        self.initializer = initializer
        self._size = size
        self._signed = signed
        self._const = const

    def initialise(self, offset):
        #initialise is used for global variables before program starts
        assert not self.local
        self.offset = offset
        instructions = []
        instructions.extend(self.initializer.generate())
        store_object(instructions, n=self.size()//4, offset=self.offset, local=False)
        return instructions

    def generate(self):
        #generate is used for local variables each time a function is called
        assert self.local
        instructions = []
        instructions.extend(self.initializer.generate())
        store_object(instructions, n=self.size()//4, offset=self.offset, local=True)
        return instructions

    def reference(self):
        return Variable(self)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class ArrayDeclaration:

    """An Array Declaration.

    Use instance to create an instance of the array,
    or array_iargument_instance if this is a function argument

    """

    def __init__(
        self,
        elements,
        element_declaration
    ):

        self.elements = elements
        self.element_declaration = element_declaration
        self.initializer = None

    def instance(self, function):

        """Create an instance of an array"""

        if hasattr(function, "is_global"):
            local = False
        else:
            local = True
        offset = function.offset
        function.offset += self.size()//4
        return ArrayInstance(
            local = local,
            offset = offset,
            elements = self.elements,
            element_declaration = self.element_declaration,
            initializer = self.initializer,
        )

    def argument_instance(self, function):

        """Create an instance of an array (function argument)"""

        local = True
        offset = function.offset
        function.offset += 1
        return ArrayArgumentInstance(
            offset = offset,
            elements = self.elements,
            element_declaration = self.element_declaration,
            initializer = self.initializer,
        )

    def type_(self):
        return self.element_declaration.type_() + "[]"

    def size(self):
        return self.elements * self.element_declaration.size()

    def argument_size(self):
        return 4

    def signed(self):
        return self.element_declaration.signed()

class ArrayArgumentInstance:

    """An instance of an array used as a function argument
    
    Array arguments used as function arguments behave as references
    and the same size as a pointer (4 bytes in this case).

    """

    def __init__(
        self,
        offset,
        elements,
        element_declaration,
        initializer,
    ):
        self.local = True
        self.offset = offset
        self.elements = elements
        self.element_declaration = element_declaration
        self.initializer = initializer

    def reference(self):

        """Return a reference to an array argument"""

        return ArrayArgument(self)

    def type_(self):
        return self.element_declaration.type_() + "[]"

    def size(self):
        return 4

    def signed(self):
        return self.element_declaration.signed()

class ArrayInstance:

    """An instance of an Array"""

    def __init__(
        self,
        local,
        offset,
        elements,
        element_declaration,
        initializer,
    ):
        self.local = local
        self.offset = offset
        self.elements = elements
        self.element_declaration = element_declaration
        self.initializer = initializer

    def initialise(self, offset):

        """Arrays with a global scope are initialised here"""

        self.offset = offset
        instructions = []
        assert not self.local
        if self.initializer:
            for location, expression in enumerate(flatten(self.initializer)):
                instructions.extend(expression.generate())
                store_object(instructions, n=expression.size()//4, offset=self.offset+location, local=False)
        return instructions

    def generate(self):

        """Arrays with a local scope are initialised here"""

        assert self.local
        instructions = []
        if self.initializer:
            for location, expression in enumerate(flatten(self.initializer)):
                instructions.extend(expression.generate())
                store_object(instructions, n=expression.size()//4, offset=self.offset+location, local=True)
        return instructions

    def reference(self):

        """A reference to this array instance"""

        return Array(self)

    def type_(self):
        return self.element_declaration.type_()+"[]"

    def size(self):
        return self.element_declaration.size()*self.elements

    def signed(self):
        return self.element_declaration.signed()


class StructDeclaration:

    """ a declaration of a struct object """

    def __init__(self, member_names, member_declarations):
        self.member_names = member_names
        self.member_declarations = member_declarations
        self._size = sum([i.size() for i in member_declarations])
        self._signed = False

    def argument_instance(self, function):
        return self.instance(function)

    def instance(self, function):

        """ create an instance of this struct """

        if hasattr(function, "is_global"):
            local = False
        else:
            local = True
        offset = function.offset
        function.offset += self.size()//4
        self.member_instances = (
                i.instance(function) 
                for i in self.member_declarations
        )

        return StructInstance(
            local,
            offset,
            self.type_(),
            self.size(),
            self.signed(),
            self.member_names,
            self.member_instances,
            self
        )

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def argument_size(self):
        return self._size

    def signed(self):
        return self._signed


class StructInstance:

    """an instance of a struct object"""

    def __init__(
        self, 
        local, 
        offset, 
        type_, 
        size, 
        signed, 
        member_names, 
        member_instances,
        declaration
    ):
        self.member_names = member_names
        self.member_instances = member_instances
        self.local = local
        self.offset = offset
        self._type = type_
        self._size = size
        self._signed = signed
        self.declaration = declaration


    def generate(self):
        instructions = []
        return instructions

    def initialise(self, offset):
        assert not self.local
        self.offset = offset
        instructions = []
        return instructions

    def reference(self):
        return Struct(self, self.declaration)

    def type_(self):
        return self._type

    def size(self):
        return self._size

    def signed(self):
        return self._signed


class DiscardExpression:

    def __init__(self, expression):
        self.expression = expression

    def generate(self):
        instructions = self.expression.discard()
        return instructions


class Expression:

    """ A base class from which expressions can be derived.

    All expression have a value method 
    (but it will raise an exception if it is not a constant)

    All expressions have a type and a size, they may be signed or unsigned.

    Expressions have a generate method which moves their value onto the stack.
    
    """

    def __init__(self, t, size, signed):
        self.type_var=t
        self.size_var=size
        self.signed_var=signed

    def type_(self):
        return self.type_var

    def size(self):
        return self.size_var

    def signed(self):
        return self.signed_var

    def argument_size(self):
        return self.size()

    def discard(self):

        """In some instances, the value of an expression is dicarded, this
        can be achieved by removing the correct amount of data from the stack.

        A derived class can provide discard functionality directly by overriding
        this function, this can result in efficiencies because it may not be
        necassary to place a value onto the stack in the first place.
        """

        instructions = self.generate()
        if self.size() == 4:
            pass
        elif self.size() == 8:
            pass
        else:
            instructions.append({"op":"addl", "z":tos, "a":tos, "literal":-self.size()//4})
        return instructions

    def value(self):

        """return an representation of an expression

        May be an integer or floating point value.

        Used when evaluating or optimizing constant expressions

        """

        raise NotConstant

    def const(self):
        return True

    def int_value(self):

        """return an integer representation of an expression

        Even if the expression is not an integer.

        Used mainly in code generation.

        """

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

    """A base class from which other objects can be derived.

    Variables, structs, pointers and arrays are all objects

    All objects are expressions, but may also be assigned to.

    Objects tend to offer a copy method to generate code to move
    data into them from the stack.

    """

    def __init__(self, instance):
        Expression.__init__(self, instance.type_(), instance.size(), instance.signed())
        self.instance = instance

    def value(self):
        raise NotConstant

    def const(self):
        return False


def AND(left, right):

    """Psuedo class, to represent a logical and function"""

    return ANDOR(left, right, "jmp_if_false")


def OR(left, right):

    """Psuedo class, to represent a logical or function"""

    return ANDOR(left, right, "jmp_if_true")

class MultiExpression(Expression):

    """Mainly used in for loops using comma operator.
    
    The value of first expression is used, other expressions are just discarded.

    """

    def __init__(self, first, others):
        self.first = constant_fold(first)
        self.others = [constant_fold(i) for i in others]
        Expression.__init__(
            self,
            first.type_(),
            first.size(),
            first.signed())

    def generate(self):
        instructions = []
        instructions.extend(self.first.generate())
        if self.first.size() == 4:
            push(instructions, result)
        elif self.first.size() == 8:
            push(instructions, result)
            push(instructions, result_hi)
        for expression in self.others:
            instructions.extend(expression.discard())
        if self.first.size() == 4:
            pop(instructions, result)
        elif self.first.size() == 8:
            pop(instructions, result_hi)
            pop(instructions, result)
        return instructions

class ANDOR(Expression):

    """The actual class used to implement AND and OR.
    
    A common class is used to save code.

    """

    def __init__(self, left, right, op):
        self.left = constant_fold(left)
        self.right = constant_fold(right)
        self.op = op
        Expression.__init__(
            self,
            "int",
            max(left.size(), right.size()),
            left.signed() and right.signed())

    def generate(self):
        instructions = []
        instructions.extend(self.left.generate())
        if self.size() == 8:
            instructions.append({"op":"or", "z":temp, "a":result, "b":result_hi})
            instructions.append({"op":self.op, "a":temp, "label":"end_%s"%id(self)})
        else:
            instructions.append({"op":self.op, "a":result, "label":"end_%s"%id(self)})
        instructions.extend(self.right.generate())
        instructions.append({ "op":"label", "label":"end_%s"%id(self), })
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

    """A binary expression such as +-/*%&|^ ... """

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

    def generate(self):

        instructions = []

        operation, reverse_operands = select_binary_instruction(
            self.left.size(),
            self.right.size(),
            self.type_(),
            self.left.signed(),
            self.right.signed(),
            self.operator)

        if reverse_operands:
            instructions.extend(self.left.generate())
            push(instructions, result)
            if self.left.size() == 8:
                push(instructions, result_hi)
            instructions.extend(self.right.generate())
            if self.left.size() == 8:
                pop(instructions, result_b_hi)
            pop(instructions, result_b)
        else:
            instructions.extend(self.right.generate())
            push(instructions, result)
            if self.right.size() == 8:
                push(instructions, result_hi)
            instructions.extend(self.left.generate())
            if self.left.size() == 8:
                pop(instructions, result_b_hi)
            pop(instructions, result_b)


        instructions.append({ "op":operation, "z":result, "a":result, "b":result_b})

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

    """Instead of creating an expression class for sizeof operator...

    ... Just return a constant object

    """

    return Constant(expression.size())

class DoubleToBits(Expression):

    """Replace a Double precision floating point number with its integer representation

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__(self, "int", 8, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.int_value()

class FloatToBits(Expression):

    """Replace a floating point number with its integer representation

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__(self, "int", 4, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.int_value()

class BitsToDouble(Expression):

    """Replace a long integer with the floating point number it represents

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__(self, "float", 8, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return bits_to_double(self.expression.value())

class BitsToFloat(Expression):

    """Replace a long integer with the floating point number it represents

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__(self, "float", 4, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return bits_to_float(self.expression.value())

class IntToLong(Expression):

    """Extend an integer into a long one"""

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 8, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        if self.expression.signed():
            instructions.append({ "op":"int_to_long", "z":result_hi, "a":result})
        else:
            instructions.append({"op":"literal", "z":result_hi, "literal":0})
        return instructions

    def value(self):
        return self.expression.value()

class LongToInt(Expression):

    """truncate a long integer into a normal one"""

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 4, expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.value()

class IntToFloat(Expression):

    """Turn an integer into a floating point number with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 4, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })
        instructions.append({
            "op"   : "int_to_float",
        })
        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })

        return instructions

    def value(self):
        return float(self.expression.value())


class FloatToInt(Expression):

    """Turn an floating point number into an integer with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 4, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })
        instructions.append({
            "op"   : "float_to_int",
        })
        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })

        return instructions

    def value(self):
        return int(self.expression.value())

class DoubleToLong(Expression):

    """Turn an double into an integer with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "int", 8, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_hi",
            "z":result_hi,
            "a":result_hi,
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })
        instructions.append({
            "op"   : "double_to_long"
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })
        instructions.append({
            "op"   : "a_hi",
            "z":result_hi,
            "a":result_hi,
        })

        return instructions

    def value(self):
        return int(self.expression.value())

class LongToDouble(Expression):

    """Turn an integer into a double with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 8, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_hi",
            "z":result_hi,
            "a":result_hi,
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })
        instructions.append({
            "op"   : "long_to_double",
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })
        instructions.append({
            "op"   : "a_hi",
            "z":result_hi,
            "a":result_hi,
        })

        return instructions

    def value(self):
        return int(self.expression.value())

class DoubleToFloat(Expression):

    """Turn a double into a float with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 4, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_hi",
            "z":result_hi,
            "a":result_hi,
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })
        instructions.append({
            "op"   : "double_to_float",
        })
        instructions.append({
            "op"   : "a_lo",
            "z":result,
            "a":result,
        })

        return instructions

    def value(self):
        return float(self.expression.value())

class FloatToDouble(Expression):

    """Turn a float into a double with the same value
    
    Used in casting and implicit type conversions
    
    """

    def __init__(self, expression):
        self.expression = constant_fold(expression)

        Expression.__init__( self, "float", 8, True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })
        instructions.append({
            "op"   : "float_to_double",
        })
        instructions.append({
            "op"   : "a_lo",
            "a"   : result,
            "z"   : result,
        })
        instructions.append({
            "op"   : "a_hi",
            "a"   : result_hi,
            "z"   : result_hi,
        })

        return instructions

    def value(self):
        return float(self.expression.value())


class Unary(Expression):

    """Unary oprerator such as ~!- ... """

    def __init__(self, operator, expression):
        self.expression = constant_fold(expression)
        self.operator = operator

        Expression.__init__(
            self,
            expression.type_(),
            expression.size(),
            expression.signed())

    def generate(self):
        instructions = self.expression.generate()

        if self.size() == 8:
            instructions.extend([{
                "op":"long_not",
                }])
        else:
            instructions.extend([{
                "op":"not",
                "a":result,
                "z":result,
                }])

        return instructions

    def value(self):
        return eval("%s%s"%(self.operator, self.expression.value()))


class FunctionCall(Expression):

    """ A function call (which is an expression) """

    def __init__(self, function):
        self.function = function

        Expression.__init__(
            self,
            function.type_(),
            function.size(),
            function.signed())

    def generate(self):
        instructions = []

        #save non-volatile registers
        push(instructions, return_address)
        push(instructions, return_frame)

        #put arguments on stack
        argument_size = 0
        for expression in self.arguments:
            instructions.extend(expression.generate())
            argument_size += expression.argument_size()
            if expression.argument_size() == 4:
                push(instructions, result)
            elif expression.argument_size() == 8:
                push(instructions, result)
                push(instructions, result_hi)
            else:
                pass

        #call the function
        call(instructions, "function_%s"%id(self.function))

        #take the arguments off again
        instructions.append({
            "op":"addl",
            "z":tos,
            "a":tos,
            "literal":-argument_size//4,
        })

        #reload non-volatile registers
        pop(instructions, return_frame)
        pop(instructions, return_address)

        #retrieve the return value and place on the stack
        if self.function.size():
            load_object(
                instructions, 
                n=self.function.size()//4, 
                offset=self.function.return_pointer, 
                local=False
            )

        return instructions


class Output(Expression):

    """ Write an expression to the output numbered "handle" """

    def __init__(self, handle, expression):
        self.handle = handle
        self.expression = expression
        Expression.__init__(self, "void", 0, False)

    def generate(self):
        instructions = self.handle.generate()
        push(instructions, result)
        instructions.extend(self.expression.generate())
        pop(instructions, temp)
        instructions.append({"op":"write", "a":temp, "b":result})
        return instructions


class FileWrite(Expression):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        Expression.__init__(
            self,
            "void",
            0,
            False)

    def generate(self):
        instructions = self.expression.generate()

        if self.expression.type_() == "float" and self.expression.size() == 8:
            instructions.append({"op":"a_hi", "z":result_hi, "a":result_hi})
            instructions.append({"op":"a_lo", "z":result, "a":result})
            instructions.append({"op":"long_float_file_write", "file_name" : self.name})
        elif self.expression.type_() == "float" and self.expression.size() == 4:
            instructions.append({ "op":"float_file_write", "a":result, "file_name":self.name})
        elif self.expression.type_() == "int" and self.expression.size() == 8:
            instructions.append({"op":"a_hi", "z":result_hi, "a":result_hi})
            instructions.append({"op":"a_lo", "z":result, "a":result})
            instructions.append({"op":"long_file_write", "file_name":self.name})
        else:
            instructions.append({"op":"file_write", "a":result, "file_name" : self.name})

        return instructions


class Input(Expression):

    def __init__(self, handle):
        self.handle = handle
        Expression.__init__(self, "int", 4, False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append({"op":"read", "z":result, "a":result})
        return instructions


class FileRead(Expression):

    def __init__(self, name):
        self.name = name
        Expression.__init__(self, "int", 4, True)

    def generate(self):
        instructions = []
        instructions.append({"op":"file_read", "z":result, "file_name":self.name})
        return instructions


class Ready(Expression):

    def __init__(self, handle):
        self.handle = handle
        Expression.__init__(self, "int", 4, False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append({"op":"ready", "z":result, "a":result})

        return instructions

class OutputReady(Expression):

    def __init__(self, handle):
        self.handle = handle
        Expression.__init__(self, "int", 4, False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append({"op":"output_ready", "z":result, "a":result})

        return instructions

class Struct(Object):

    def __init__(self, instance, declaration):
        Object.__init__(self, instance)
        self.declaration = declaration

    def address(self):
        instructions = []
        if self.instance.local:
            instructions.append({ "op" : "addl", "z":result, "a":frame, "literal":self.instance.offset})
        else:
            instructions.append({ "op" : "literal", "z":result, "literal":self.instance.offset})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        load_object(instructions, n=self.size()//4, offset=None, local=False)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if self.size() == 4:
            push(instructions, result)
        elif self.size() == 8:
            push(instructions, result)
            push(instructions, result_hi)
        instructions.extend(self.address())
        instructions.append({"op":"addl", "z":address, "a":result, "literal": 0})
        if self.size() == 4:
            pop(instructions, result)
        elif self.size() == 8:
            pop(instructions, result_hi)
            pop(instructions, result)
        store_object(instructions, n=self.size()//4, offset=None, local=False, leave_on_stack=leave_on_stack)
        return instructions

class StructMember(Object):

    def __init__(self, struct, member):
        Object.__init__(self, struct)
        declaration = struct.declaration
        member_index = declaration.member_names.index(member)
        self.declaration = declaration.member_declarations[member_index]
        self.type_var = self.declaration.type_()
        self.size_var = self.declaration.size()
        if self.type_().endswith("[]"):
            self.element_declaration = declaration.member_declarations[member_index].element_declaration
        self.struct = struct
        self.struct_offset = 0
        for name, instance in zip(declaration.member_names, declaration.member_declarations):
            if name == member:
                break
            self.struct_offset += instance.size()//4
            

    def address(self):
        instructions = []
        instructions.extend(self.struct.address())
        instructions.append({"op":"addl", "z":result, "a":result, "literal": self.struct_offset})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        load_object(instructions, n=self.size()//4, offset=None, local=False)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if self.size() == 4:
            push(instructions, result)
        elif self.size() == 8:
            push(instructions, result)
            push(instructions, result_hi)
        instructions.extend(self.address())
        instructions.append({"op":"addl", "z":address, "a":result, "literal": 0})
        if self.size() == 4:
            pop(instructions, result)
        elif self.size() == 8:
            pop(instructions, result_hi)
            pop(instructions, result)
        store_object(instructions, n=self.size()//4, offset=None, local=False, leave_on_stack=leave_on_stack)
        return instructions

class ArrayArgument(Object):

    def __init__(self, instance):
        Object.__init__(self, instance)
        self.elements = instance.elements
        self.element_declaration = instance.element_declaration

    def address(self):
        instructions = []
        instructions.append({
            "op":"addl", 
            "z":result, 
            "a":frame, 
            "literal":self.instance.offset,
        })
        instructions.append({"op":"load", "z":result, "a":result})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        return instructions


class Array(Object):

    def __init__(self, instance):
        Object.__init__(self, instance)
        self.elements = instance.elements
        self.element_declaration = instance.element_declaration

    def address(self):
        instructions = []
        if self.instance.local:
            instructions.append({"op":"addl", "z":result, "a":frame, "literal":self.instance.offset})
        else:
            instructions.append({"op":"literal", "z":result, "literal":self.instance.offset})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        return instructions

    def argument_size(self):
        return 4

class ArrayIndex(Object):

    def __init__(self, array, index_expression):
        self.array = array
        self.declaration = array.element_declaration
        if array.element_declaration.type_().endswith("[]"):
            self.element_declaration = array.element_declaration.element_declaration
        self.index_expression = index_expression

    def address(self):
        instructions = []
        instructions.extend(self.array.address())
        push(instructions, result)
        instructions.extend(self.index_expression.generate())
        pop(instructions, address)
        if self.size() > 4:
            instructions.append({"op":"literal", "z":temp, "literal":self.size()//4})
            instructions.append({"op":"multiply", "z":result, "a":result, "b":temp})
        instructions.append({"op":"add", "z":result, "a":result, "b":address})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        load_object(instructions, n=self.size()//4, offset=None, local=False)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if self.size()==4:
            push(instructions, result)
        elif self.size()==8:
            push(instructions, result)
            push(instructions, result_hi)
        instructions.extend(self.address())
        instructions.append({"op":"addl", "z":address, "a":result, "literal": 0})
        if self.size()==4:
            pop(instructions, result)
        elif self.size()==8:
            pop(instructions, result_hi)
            pop(instructions, result)
        store_object(instructions, n=self.size()//4, offset=None, local=False, leave_on_stack=leave_on_stack)
        return instructions

    def size(self):
        return self.array.element_declaration.size()

    def type_(self):
        return self.array.element_declaration.type_()

    def signed(self):
        return self.array.element_declaration.signed()


class Variable(Object):
    def __init__(self, instance):
        Object.__init__(self, instance)

    def address(self):
        instructions = []
        if self.instance.local:
            instructions.append({"op":"addl", "z":result, "a":frame, "literal":self.instance.offset})
        else:
            instructions.append({"op":"literal", "z":result, "literal":self.instance.offset})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        load_object(instructions, n=self.size()//4, offset=None, local=True)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if self.instance.local:
            instructions.append({"op":"addl", "z":address, "a":frame, "literal":self.instance.offset})
        else:
            instructions.append({"op":"literal", "z":address, "literal":self.instance.offset})
        store_object(instructions, n=self.size()//4, offset=None, local=True)
        return instructions

    def const(self):
        return self.instance.const()

    def value(self):
        if self.const():
            return self.instance.initializer.value()
        else:
            raise NotConstant


class Assignment(Expression):

    def __init__(self, lvalue, expression):
        Expression.__init__(self, lvalue.type_(), lvalue.size(), lvalue.signed())
        self.lvalue = lvalue
        self.expression = expression

    def discard(self):
        return self.lvalue.copy(self.expression, False)


    def generate(self):
        return self.lvalue.copy(self.expression, True)

class Constant(Expression):

    def __init__(self, value, type_="int", size=4, signed=True):
        self._value = value
        Expression.__init__(self, type_, size, signed)

    def generate(self):

        int_value = self.int_value()
        instructions = []
        instructions.append({"op":"literal", "z":result, "literal":int_value & 0xffffffff})
        if self.size() == 8:
            instructions.append({"op":"literal", "z":result_hi, "literal":(int_value >> 32) & 0xffffffff})
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




