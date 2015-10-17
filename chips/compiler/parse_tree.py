__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct
from register_map import *
from instruction_utils import *
from instruction_utils import _return
from exceptions import C2CHIPError, NotConstant
from utils import bits_to_double, bits_to_float
from types import *

class Trace:

    """A trace object is used to keep track of the source code
    throughout the compilation process.
    """

    def __init__(self, parser):
        self.lineno = parser.tokens.lineno
        self.filename = parser.tokens.filename
        self.function = parser.function
        self.global_scope = parser.global_scope
        self.statement = parser.statement

    def __repr__(self):
        return "%s : %s" % (self.filename, self.lineno)

    def error(self, string):
        raise C2CHIPError(string + "\n", self.filename, self.lineno)


def flatten(sequence):
    """Turn a list containing other lists into a single list"""

    try:
        l = []
        for i in sequence:
            l.extend(flatten(i))
    except:
        l = sequence
    return l


def constant_fold(trace, expression):
    """Replace an expression with a constant if possible"""

    try:
        return Constant(
            trace,
            expression.value(),
            expression.type_(),
            expression.signed()
        )
    except NotConstant:
        return expression


class Process:

    """A process is a whole C program.

    Within a chip there may more than one process.

    """

    def __init__(self, trace):
        self.trace = trace

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
        instructions.append(
            {"trace": self.trace,
             "op": "literal",
             "z": tos,
             "literal": 0})
        instructions.append(
            {"trace": self.trace,
             "op": "literal",
             "z": frame,
             "literal": 0})

        # reserve stack space for global objects and function return values
        globals_and_functions = set(called_functions + referenced_globals)
        global_size = sum([size_of(i) for i in globals_and_functions])
        if global_size:
            instructions.append(
                {"trace": self.trace,
                 "op": "addl",
                 "z": tos,
                 "a": tos,
                 "literal": global_size // 4})
        offset = 0
        for global_object in globals_and_functions:
            instructions.extend(global_object.initialise(offset))
            offset += size_of(global_object) // 4

        # start with a call to main
        call(self.trace, instructions, "function_%s" % id(self.main))

        # then stop
        instructions.append({"trace": self.trace, "op": "stop"})

        # then generate functions. This will ensure that memory has been
        # reserved for globals before functions are compiled.
        for function in called_functions:
            instructions.extend(function.generate())

        # instructions.append({"trace":self.trace, "op":"return",
        # "a":return_address})

        return instructions


class GlobalScope:

    """A stand in for a function for areas where no function is in scope"""

    def __init__(self):
        self.offset = 0
        self.is_global = True
        self.referenced_globals = []
        self.global_variables = {}
        self.local_variables = {}


class Function:

    """A Function Object"""

    def __init__(self, trace, name, type_specifier):
        self.trace = trace
        self.offset = 0
        self.local = False
        self.name = name
        self._type_ = type_specifier.type_
        self._signed = type_specifier.signed
        self._const = type_specifier.const
        self.called_functions = []
        self.referenced_globals = []
        self.local_variables = {}
        self.global_variables = {}

    def generate(self):
        if not hasattr(self, "statement"):
            self.trace.error(
                "Function %s has been declared, but not defined" %
                self.name)

        instructions = []
        instructions.append({
            "trace": self.trace,
            "op": "label",
            "label": "function_%s" % id(self),
        })
        instructions.append({
            "trace": self.trace,
            "op": "addl",
            "z": tos,
            "a": tos,
            "literal": self.offset,
        })
        instructions.extend(self.statement.generate())
        if not hasattr(self, "return_statement"):
            _return(self.trace, instructions)
        return instructions

    def initialise(self, offset):
        self.return_pointer = offset
        return []

    def reference(self, trace):
        return self

    def type_(self):
        return self._type_

    def signed(self):
        return self._signed

    def const(self):
        """Potentially meaningless"""
        return self._const


class Label:

    """A labelled statement that may be the target of a goto"""

    def __init__(self, trace, statement):
        self.trace = trace
        self.statement = statement

    def generate(self):
        if self.statement is None:
            raise C2CHIPError("Function %s was never given a body"%(self.name))
            
        instructions = []
        instructions.append({
            "trace": self.trace,
            "op": "label",
            "label": "goto_label_%s" % id(self),
        })
        instructions.extend(self.statement.generate())
        return instructions


class Goto:

    """A goto statement"""

    def __init__(self, trace, goto_labels, label_name):
        self.trace = trace
        self.goto_labels = goto_labels
        self.label_name = label_name

    def generate(self):

        # labels can be declared after gotos, so
        # need to put off checking until code generation
        try:
            label = self.goto_labels[self.label_name]
        except KeyError:
            self.trace.error("label %s is not defined" % self.label_name)

        instructions = []
        instructions.append({
            "trace": self.trace,
            "op": "goto",
            "label": "goto_label_%s" % id(label),
        })
        return instructions


class Break:

    """Exit a loop or case statement"""

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        return [{
                "trace": self.trace,
                "op": "goto",
                "label": "break_%s" % id(self.loop)
                }]


class Continue:

    """go straight to the next loop iteration"""

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        return [{
                "trace": self.trace,
                "op": "goto",
                "label": "continue_%s" % id(self.loop)
                }]


class Assert:

    """ if an expression evaluates to false, raise an error """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = self.expression.generate()
        instructions.append({
            "trace": self.trace,
            "op": "assert",
            "a": result,
            "line": self.line,
            "file": self.filename,
        })

        return instructions


class Return:

    """ return from a function """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = []
        if hasattr(self, "expression"):
            instructions.extend(self.expression.generate())
            store_object(
                self.trace,
                instructions,
                n=size_of(self.function) // 4,
                offset=self.function.return_pointer,
                local=False
            )
        _return(self.trace, instructions)

        return instructions


class Report:

    """ report the value of an expression - simulation only """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = self.expression.generate()

        if size_of(self.expression) == 4:
            instructions.append({
                "trace": self.trace,
                "op": "a_lo",
                "z": result,
                "a": result,
            })
            if self.expression.type_() == "float":
                instructions.append({
                    "trace": self.trace,
                    "op": "float_report",
                    "line": self.line,
                    "file": self.filename
                })
            else:
                if self.expression.signed():
                    instructions.append({
                        "trace": self.trace,
                        "op": "report",
                        "line": self.line,
                        "file": self.filename,
                    })
                else:
                    instructions.append({
                        "trace": self.trace,
                        "op": "unsigned_report",
                        "line": self.line,
                        "file": self.filename,
                    })

        elif size_of(self.expression) == 8:

            instructions.append({
                "trace": self.trace,
                "op": "a_hi",
                "a": result_hi,
                "z": result_hi,
            })
            instructions.append({
                "trace": self.trace,
                "op": "a_lo",
                "a": result,
                "z": result,
            })
            if self.expression.type_() == "double":
                instructions.append({
                    "trace": self.trace,
                    "op": "long_float_report",
                    "line": self.line,
                    "file": self.filename,
                })
            else:
                if self.expression.signed():
                    instructions.append({
                        "trace": self.trace,
                        "op": "long_report",
                        "line": self.line,
                        "file": self.filename,
                    })
                else:
                    instructions.append({
                        "trace": self.trace,
                        "op": "long_unsigned_report",
                        "line": self.line,
                        "file": self.filename,
                    })

        return instructions


class WaitClocks:

    """ stop execution for n clock cycles """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = self.expression.generate()
        instructions.append(
            {"trace": self.trace,
             "op": "wait_clocks",
             "a": result})
        return instructions


class If:

    """ if statement """

    def __init__(self, trace):
        self.trace = trace

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
            if size_of(self.expression) == 8:
                instructions.append({
                    "trace": self.trace,
                    "op": "or",
                    "z": result,
                    "a": result,
                    "b": result_hi,
                })
            instructions.append({
                "trace": self.trace,
                "op": "jmp_if_false",
                "a": result,
                "label": "else_%s" % id(self),
            })
            instructions.extend(self.true_statement.generate())
            instructions.append({
                "trace": self.trace,
                "op": "goto",
                "label": "end_%s" % id(self)
            })
            instructions.append(
                {"trace": self.trace,
                 "op": "label",
                 "label": "else_%s" % id(self)})
            if self.false_statement:
                instructions.extend(self.false_statement.generate())
            instructions.append(
                {"trace": self.trace,
                 "op": "label",
                 "label": "end_%s" % id(self)})
            return instructions


class Switch:

    """ switch statement """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = []
        instructions.extend(self.expression.generate())
        if size_of(self.expression) == 4:
            for value, case in self.cases.iteritems():
                instructions.append({
                    "trace": self.trace,
                    "op": "literal",
                    "z": temp,
                    "literal": value & 0xffffffff,
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "equal",
                    "a": result,
                    "b": temp,
                    "z": temp
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "jmp_if_true",
                    "label": "case_%s" % id(case),
                    "a": temp,
                })
        else:
            for value, case in self.cases.iteritems():
                instructions.append({
                    "trace": self.trace,
                    "op": "literal",
                    "z": temp,
                    "literal": value & 0xffffffff,
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "literal",
                    "z": temp1,
                    "literal": (value >> 32) & 0xffffffff,
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "equal",
                    "a": result,
                    "b": temp,
                    "z": temp
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "equal",
                    "a": result_hi,
                    "b": temp1,
                    "z": temp1
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "and",
                    "a": temp,
                    "b": temp1,
                    "z": temp
                })
                instructions.append({
                    "trace": self.trace,
                    "op": "jmp_if_true",
                    "label": "case_%s" % id(case),
                    "a": temp,
                })

        if hasattr(self, "default"):
            instructions.append({
                "trace": self.trace,
                "op": "goto",
                "label": "case_%s" % id(self.default)
            })
        instructions.append({
            "trace": self.trace,
            "op": "goto",
            "label": "break_%s" % id(self),
        })

        instructions.extend(self.statement.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "break_%s" % id(self)})
        return instructions


class Case:

    """ case statement """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = []
        instructions.append({
            "trace": self.trace,
            "op": "label",
            "label": "case_%s" % id(self),
        })
        return instructions


class Default:

    """ default case statement """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        return [{
            "trace": self.trace,
            "op": "label",
            "label": "case_%s" % id(self)
        }]


class Loop:

    """ A loop while or do-while are synthesised from this """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = [{
            "trace": self.trace,
            "op": "label",
            "label": "begin_%s" % id(self)
        }]
        instructions.append({
            "trace": self.trace,
                            "op": "label",
                            "label": "continue_%s" % id(self)
                            })
        instructions.extend(self.statement.generate())
        instructions.append({
            "trace": self.trace,
            "op": "goto",
            "label": "begin_%s" % id(self)
        })
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "break_%s" % id(self)})
        return instructions


class For:

    """ A for loop """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = []
        if hasattr(self, "statement1"):
            instructions.extend(self.statement1.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "begin_%s" % id(self)})
        if hasattr(self, "expression"):

            instructions.extend(self.expression.generate())
            if size_of(self.expression) == 8:
                instructions.append({
                    "trace": self.trace,
                    "op": "or",
                    "z": result,
                    "a": result,
                    "b": result_hi,
                })
            instructions.append({
                "trace": self.trace,
                "op": "jmp_if_false",
                "a": result,
                "label": "end_%s" % id(self)
            })

        instructions.extend(self.statement3.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "continue_%s" % id(self)})
        if hasattr(self, "statement2"):
            instructions.extend(self.statement2.generate())
        instructions.append({
            "trace": self.trace,
            "op": "goto",
            "label": "begin_%s" % id(self)
        })
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "end_%s" % id(self)})
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "break_%s" % id(self)})
        return instructions


class Block:

    """ A block of statements enclosed by braces """

    def __init__(self, trace):
        self.trace = trace

    def generate(self):
        instructions = []
        for statement in self.statements:
            instructions.extend(statement.generate())
        return instructions


class Label:

    def __init__(self, name, statement):
        self.name=name
        self.statement = statement
        
    def generate(self):
        instructions=[]
        instructions.append({"op":"label", "label":"namedlabel_%s"%id(self)})
        instructions.extend(self.statement.generate())
        return instructions
        
        
class Goto:

    def __init__(self, name, function, filename, lineno):
        self.name=name #what label is being jumped to
        self.function=function  #what function object are we in, to look inside its scope
        self.filename=filename
        self.lineno=lineno
        
    def generate(self):
        if self.name not in self.function.labels_in_scope:
            raise C2CHIPError("Can't goto label not in scope: %s"%self.name + "\n", self.filename, self.lineno)
        label = self.function.labels_in_scope[self.name];        
       
        return [{"op":"goto", "label":"namedlabel_%s"%id(label)}]
        
        
class CompoundDeclaration:

    """ More than one declaration on the same line """

    def __init__(self, declarations):
        self.declarations = declarations

    def generate(self):
        instructions = []
        for declaration in self.declarations:
            instructions.extend(declaration.generate())
        return instructions


class Argument:

    """ a function argument """

    def __init__(self, trace, declaration, function):
        self.trace = trace
        self._type = declaration.type_
        self._signed = declaration.signed
        self._const = declaration.const
        self.initializer = None
        self.local = True
        self.argument = True

        self.offset = function.offset
        function.offset += arg_size_of(self) // 4

    def reference(self, trace):
        return Variable(trace, self)

    def type_(self):
        return self._type

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class LocalVariable:

    """ a local variable """

    def __init__(self, trace, declaration, initializer, function):
        self.trace = trace
        self._type = declaration.type_
        self._signed = declaration.signed
        self._const = declaration.const
        self.initializer = initializer
        self.local = True
        self.argument = False

        self.offset = function.offset
        function.offset += size_of(self) // 4

    def generate(self):
        # generate is used for local variables each time a function is called
        assert self.local
        instructions = []
        if self.initializer is not None:
            if is_array_of(self):
                for index, expression in enumerate(flatten(self.initializer)):
                    instructions.extend(expression.generate())
                    store_object(
                        self.trace,
                        instructions,
                        n=size_of(expression) // 4,
                        offset=self.offset +
                        (index * size_of(expression) // 4),
                        local=True
                    )
            else:
                instructions.extend(self.initializer.generate())
                store_object(
                    self.trace,
                    instructions,
                    n=size_of(self) // 4,
                    offset=self.offset,
                    local=True)
        return instructions

    def reference(self, trace):
        return Variable(trace, self)

    def type_(self):
        return self._type

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class GlobalVariable:

    """ a global variable """

    def __init__(self, trace, declaration, initializer, function):
        self.trace = trace
        self._type = declaration.type_
        self._signed = declaration.signed
        self._const = declaration.const
        self.initializer = initializer
        self.local = False
        self.argument = False

        self.offset = function.offset
        function.offset += size_of(self) // 4

    def initialise(self, offset):
        # initialise is used for global variables before program starts
        assert not self.local
        self.offset = offset
        instructions = []
        if self.initializer is not None:
            if is_array_of(self):
                for index, expression in enumerate(flatten(self.initializer)):
                    instructions.extend(expression.generate())
                    store_object(
                        self.trace,
                        instructions,
                        n=size_of(expression) // 4,
                        offset=self.offset +
                        (index * size_of(expression) // 4),
                        local=False
                    )
            else:
                instructions.extend(self.initializer.generate())
                store_object(
                    self.trace,
                    instructions,
                    n=size_of(self) // 4,
                    offset=self.offset,
                    local=False)
        return instructions

    def reference(self, trace):
        return Variable(trace, self)

    def type_(self):
        return self._type

    def signed(self):
        return self._signed

    def const(self):
        return self._const


class DiscardExpression:

    def __init__(self, trace, expression):
        self.expression = expression
        self.trace = trace

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

    def __init__(self, t, signed):
        self.type_var = t
        self.signed_var = signed

    def type_(self):
        return self.type_var

    def signed(self):
        return self.signed_var

    def argument_size(self):
        return self.size()

    def discard(self):
        """In some instances, the value of an expression is discarded, this can
        be achieved by removing the correct amount of data from the stack.

        A derived class can provide discard functionality directly by
        overriding this function, this can result in efficiencies because it
        may not be necessary to place a value onto the stack in the first
        place.  """

        instructions = self.generate()
        if size_of(self) == 4:
            pass
        elif size_of(self) == 8:
            pass
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": "addl",
                 "z": tos,
                 "a": tos,
                 "literal": -size_of(self) // 4})
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

        if self.type_() == "double":
            byte_value = struct.pack(">d", self.value())
            value = ord(byte_value[0]) << 56
            value |= ord(byte_value[1]) << 48
            value |= ord(byte_value[2]) << 40
            value |= ord(byte_value[3]) << 32
            value |= ord(byte_value[4]) << 24
            value |= ord(byte_value[5]) << 16
            value |= ord(byte_value[6]) << 8
            value |= ord(byte_value[7])
            return value
        elif self.type_() == "float":
            byte_value = struct.pack(">f", self.value())
            value = ord(byte_value[0]) << 24
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
        Expression.__init__(self, instance.type_(), instance.signed())
        self.instance = instance

    def value(self):
        raise NotConstant

    def const(self):
        return False


def AND(trace, left, right):
    """Pseudo class, to represent a logical and function"""

    return ANDOR(trace, left, right, "jmp_if_false")


def OR(trace, left, right):
    """Pseudo class, to represent a logical or function"""

    return ANDOR(trace, left, right, "jmp_if_true")


class MultiExpression(Expression):

    """Mainly used in for loops using comma operator.

    The value of first expression is used, other expressions are just
    discarded.

    """

    def __init__(self, trace, first, others):
        self.trace = trace
        self.first = constant_fold(trace, first)
        self.others = [constant_fold(trace, i) for i in others]
        Expression.__init__(
            self,
            first.type_(),
            first.signed())

    def generate(self):
        instructions = []
        instructions.extend(self.first.generate())
        if size_of(self.first) == 4:
            push(self.trace, instructions, result)
        elif size_of(self.first) == 8:
            push(self.trace, instructions, result)
            push(self.trace, instructions, result_hi)
        for expression in self.others:
            instructions.extend(expression.discard())
        if size_of(self.first) == 4:
            pop(self.trace, instructions, result)
        elif size_of(self.first) == 8:
            pop(self.trace, instructions, result_hi)
            pop(self.trace, instructions, result)
        return instructions


class Ternary(Expression):

    """A ternary expression"""

    def __init__(self, trace, expression, true_expression, false_expression):
        self.trace = trace
        self.expression = constant_fold(trace, expression)
        self.true_expression = constant_fold(trace, true_expression)
        self.false_expression = constant_fold(trace, false_expression)
        type_ = true_expression.type_()
        Expression.__init__(
            self,
            type_,
            true_expression.signed() and false_expression.signed())

    def generate(self):
        instructions = []
        instructions.extend(self.expression.generate())
        if size_of(self.expression) == 8:
            instructions.append(
                {"trace": self.trace,
                 "op": "or",
                 "z": temp,
                 "a": result,
                 "b": result_hi})
            instructions.append(
                {"trace": self.trace,
                 "op": "jmp_if_false",
                 "a": temp,
                 "label": "false_%s" % id(self)})
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": "jmp_if_false",
                 "a": result,
                 "label": "false_%s" % id(self)})
        instructions.extend(self.true_expression.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "goto",
             "a": result,
             "label": "end_%s" % id(self)})
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "false_%s" % id(self),
             })
        instructions.extend(self.false_expression.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "end_%s" % id(self),
             })
        return instructions

    def value(self):
        if self.expression.value():
            return self.true_expression.value()
        else:
            return self.false_expression.value()


class ANDOR(Expression):

    """The actual class used to implement AND and OR.

    A common class is used to save code.

    """

    def __init__(self, trace, left, right, op):
        self.trace = trace
        self.left = constant_fold(trace, left)
        self.right = constant_fold(trace, right)
        self.op = op
        type_ = "long" if "long" in (left.type_(), right.type_()) else "int"
        Expression.__init__(
            self,
            type_,
            left.signed()and right.signed())

    def generate(self):
        instructions = []
        instructions.extend(self.left.generate())
        if size_of(self) == 8:
            instructions.append(
                {"trace": self.trace,
                 "op": "or",
                 "z": temp,
                 "a": result,
                 "b": result_hi})
            instructions.append(
                {"trace": self.trace,
                 "op": self.op,
                 "a": temp,
                 "label": "end_%s" % id(self)})
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": self.op,
                 "a": result,
                 "label": "end_%s" % id(self)})
        instructions.extend(self.right.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "label",
             "label": "end_%s" % id(self),
             })
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

    boolean_types = ["==", "!=", "<", ">", "<=", ">="]
    if operator in boolean_types:
        type_, signed = "int", True
    elif is_pointer_to(left) and is_pointer_to(right):
        type_ = "int"
        signed = True
    else:
        type_ = left.type_()
        signed = left.signed() and right.signed()

    return type_, signed


class Binary(Expression):

    """A binary expression such as +-/*%&|^ ... """

    def __init__(self, trace, operator, left, right):
        self.trace = trace
        self.left = constant_fold(trace, left)
        self.right = constant_fold(trace, right)
        self.operator = operator
        type_, signed = get_binary_type(left, right, operator)

        Expression.__init__(
            self,
            type_,
            signed)

    def generate(self):

        instructions = []

        operation, reverse_operands = select_binary_instruction(
            self.left.type_(),
            self.left.signed(),
            self.right.signed(),
            self.operator)

        if reverse_operands:
            instructions.extend(self.left.generate())
            push(self.trace, instructions, result)
            if size_of(self.left) == 8:
                push(self.trace, instructions, result_hi)
            instructions.extend(self.right.generate())
            if size_of(self.left) == 8:
                pop(self.trace, instructions, result_b_hi)
            pop(self.trace, instructions, result_b)
        else:
            instructions.extend(self .right.generate())

            # pointer arithmetic
            if is_pointer_to(self.left) and not is_pointer_to(self.right):
                assert self.operator in ["+", "-"]
                size = type_size(self.left.type_().base_type())
                if size > 4:
                    instructions.append(
                        {"trace": self.trace,
                         "op": "literal",
                         "z": temp,
                         "literal": size // 4})
                    instructions.append(
                        {"trace": self.trace,
                         "op": "multiply",
                         "z": result,
                         "a": result,
                         "b": temp})

            push(self.trace, instructions, result)
            if size_of(self.right) == 8:
                push(self.trace, instructions, result_hi)
            instructions.extend(self.left.generate())

            # pointer arithmetic
            if is_pointer_to(self.right) and not is_pointer_to(self.left):
                assert self.operator in ["+", "-"]
                size = type_size(self.right.type_().base_type())
                if size > 4:
                    instructions.append(
                        {"trace": self.trace,
                         "op": "literal",
                         "z": temp,
                         "literal": size // 4})
                    instructions.append(
                        {"trace": self.trace,
                         "op": "multiply",
                         "z": result,
                         "a": result,
                         "b": temp})

            if size_of(self.left) == 8:
                pop(self.trace, instructions, result_b_hi)
            pop(self.trace, instructions, result_b)

        instructions.append(
            {"trace": self.trace,
             "op": operation,
             "z": result,
             "a": result,
             "b": result_b})

        # implement pointer arithmetic
        if is_pointer_to(self.right) and is_pointer_to(self.left):
            assert self.operator == "-"
            size = type_size(self.right.type_().base_type())
            if size > 4:
                locations = size // 4
                # use multiply by the reciprocal * (2^32)
                # use top half of product is quotient
                reciprocal = int(round((2.0 ** 32) / locations))
                instructions.append(
                    {"trace": self.trace,
                     "op": "literal",
                     "z": temp,
                     "literal": reciprocal})
                instructions.append(
                    {"trace": self.trace,
                     "op": "multiply",
                     "z": result,
                     "a": result,
                     "b": temp})
                instructions.append(
                    {"trace": self.trace,
                     "op": "carry",
                     "z": result_hi})
                instructions.append(
                    {"trace": self.trace,
                     "op": "literal",
                     "z": temp,
                     "literal": 0})
                instructions.append(
                    {"trace": self.trace,
                     "op": "literal",
                     "z": temp1,
                     "literal": 0x80000000})
                instructions.append(
                    {"trace": self.trace,
                     "op": "add",
                     "z": result,
                     "a": result,
                     "b": temp1})
                instructions.append(
                    {"trace": self.trace,
                     "op": "add_with_carry",
                     "z": result,
                     "a": result_hi,
                     "b": temp})

        return instructions

    def value(self):

        if self.type_() in ["int", "long"]:

            return int(eval("%s %s %s" % (
                self.left.value(),
                self.operator,
                self.right.value())))

        else:

            return float(eval("float('%f') %s float('%f')" % (
                self.left.value(),
                self.operator,
                self.right.value()
            )))


def SizeOf(trace, expression):
    """Instead of creating an expression class for sizeof operator...

    ... Just return a constant object

    """

    return Constant(trace, size_of(expression))


class DoubleToBits(Expression):

    """Replace a Double precision floating point number with its integer
    representation

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "long", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.int_value()


class FloatToBits(Expression):

    """Replace a floating point number with its integer representation

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "int", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.int_value()


class BitsToDouble(Expression):

    """Replace a long integer with the floating point number it represents

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "double", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return bits_to_double(self.expression.value())


class BitsToFloat(Expression):

    """Replace a long integer with the floating point number it represents

    Doesn't actually "do anything" just changes the type.

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "float", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return bits_to_float(self.expression.value())


class IntToLong(Expression):

    """Extend an integer into a long one"""

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "long", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        if self.expression.signed():
            instructions.append(
                {"trace": self.trace,
                 "op": "int_to_long",
                 "z": result_hi,
                 "a": result})
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": result_hi,
                 "literal": 0})
        return instructions

    def value(self):
        return self.expression.value()


class LongToInt(Expression):

    """truncate a long integer into a normal one"""

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "int", expression.signed())

    def generate(self):
        instructions = self.expression.generate()
        return instructions

    def value(self):
        return self.expression.value()


class IntToFloat(Expression):

    """Turn an integer into a floating point number with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "float", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "int_to_float",
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })

        return instructions

    def value(self):
        return float(self.expression.value())


class FloatToInt(Expression):

    """Turn an floating point number into an integer with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "int", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "float_to_int",
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })

        return instructions

    def value(self):
        return int(self.expression.value())


class PointerCast(Expression):

    """Cast a pointer to a pointer of a different type"""

    def __init__(self, trace, expression, type_):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, type_, True)

    def generate(self):
        instructions = self.expression.generate()
        return instructions


class DoubleToLong(Expression):

    """Turn an double into an integer with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "long", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "z": result_hi,
            "a": result_hi,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "double_to_long"
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "z": result_hi,
            "a": result_hi,
        })

        return instructions

    def value(self):
        return int(self.expression.value())


class LongToDouble(Expression):

    """Turn an integer into a double with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "double", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "z": result_hi,
            "a": result_hi,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "long_to_double",
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "z": result_hi,
            "a": result_hi,
        })

        return instructions

    def value(self):
        return int(self.expression.value())


class DoubleToFloat(Expression):

    """Turn a double into a float with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "float", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "z": result_hi,
            "a": result_hi,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "double_to_float",
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "z": result,
            "a": result,
        })

        return instructions

    def value(self):
        return float(self.expression.value())


class FloatToDouble(Expression):

    """Turn a float into a double with the same value

    Used in casting and implicit type conversions

    """

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(self, "double", True)

    def generate(self):
        instructions = self.expression.generate()

        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "float_to_double",
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_lo",
            "a": result,
            "z": result,
        })
        instructions.append({
            "trace": self.trace,
            "op": "a_hi",
            "a": result_hi,
            "z": result_hi,
        })

        return instructions

    def value(self):
        return float(self.expression.value())


class Unary(Expression):

    """Unary oprerator such as ~!- ... """

    def __init__(self, trace, operator, expression):
        self.expression = constant_fold(trace, expression)
        self.operator = operator
        self.trace = trace

        Expression.__init__(
            self,
            expression.type_(),
            expression.signed())

    def generate(self):
        instructions = self.expression.generate()

        if size_of(self) == 8:
            instructions.extend([{
                "trace": self.trace,
                "op": "long_not",
            }])
        else:
            instructions.extend([{
                "trace": self.trace,
                "op": "not",
                "a": result,
                "z": result,
            }])

        return instructions

    def value(self):
        return eval("%s%s" % (self.operator, self.expression.value()))


class Address(Expression):

    """Unary operator &"""

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(
            self,
            expression.type_(),
            expression.signed())

    def generate(self):
        instructions = self.expression.address()
        return instructions

    def type_(self):
        return PointerTo(self.expression.type_())


class Dereference(Object):

    """Unary operator *"""

    def __init__(self, trace, expression):
        self.expression = constant_fold(trace, expression)
        self.trace = trace

        Expression.__init__(
            self,
            expression.type_().base_type(),
            expression.signed())

    def address(self):
        instructions = []
        instructions.extend(self.expression.generate())
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.expression.generate())
        load_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=False)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if size_of(self) == 4:
            push(self.trace, instructions, result)
        elif size_of(self) == 8:
            push(self.trace, instructions, result)
            push(self.trace, instructions, result_hi)
        instructions.extend(self.expression.generate())
        instructions.append(
            {"trace": self.trace,
             "op": "addl",
             "z": address,
             "a": result,
             "literal": 0})
        if size_of(self) == 4:
            pop(self.trace, instructions, result)
        elif size_of(self) == 8:
            pop(self.trace, instructions, result_hi)
            pop(self.trace, instructions, result)
        store_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=False)
        return instructions

    def type_(self):
        is_pointer_to(self.expression)
        return self.expression.type_().base_type()


class FunctionCall(Expression):

    """ A function call (which is an expression) """

    def __init__(self, trace, function):
        self.function = function
        self.trace = trace

        Expression.__init__(
            self,
            function.type_(),
            function.signed())

    def generate(self):
        instructions = []

        # save non-volatile registers
        push(self.trace, instructions, return_address)
        push(self.trace, instructions, return_frame)

        # put arguments on stack
        argument_size = 0
        for expression in self.arguments:
            # objects 2 or smaller are left in registers
            instructions.extend(expression.generate())
            argument_size += arg_size_of(expression)
            if arg_size_of(expression) == 4:
                push(self.trace, instructions, result)
            elif arg_size_of(expression) == 8:
                push(self.trace, instructions, result)
                push(self.trace, instructions, result_hi)
            else:
                # objects larger than 2 are on stack by default
                pass

        # call the function
        call(self.trace, instructions, "function_%s" % id(self.function))

        # take the arguments off again
        instructions.append({
            "trace": self.trace,
            "op": "addl",
            "z": tos,
            "a": tos,
            "literal": -argument_size // 4,
        })

        # reload non-volatile registers
        pop(self.trace, instructions, return_frame)
        pop(self.trace, instructions, return_address)

        # retrieve the return value and place on the stack
        if size_of(self.function):
            load_object(
                self.trace,
                instructions,
                n=size_of(self.function) // 4,
                offset=self.function.return_pointer,
                local=False
            )

        return instructions


class Output(Expression):

    """ Write an expression to the output numbered "handle" """

    def __init__(self, trace, handle, expression):
        self.trace = trace
        self.handle = handle
        self.expression = expression
        Expression.__init__(self, "void", False)

    def generate(self):
        instructions = self.handle.generate()
        push(self.trace, instructions, result)
        instructions.extend(self.expression.generate())
        pop(self.trace, instructions, temp)
        instructions.append(
            {"trace": self.trace,
             "op": "write",
             "a": temp,
             "b": result})
        return instructions


class FileWrite(Expression):

    def __init__(self, trace, name, expression):
        self.name = name
        self.trace = trace
        self.expression = expression
        Expression.__init__(
            self,
            "void",
            False)

    def generate(self):
        instructions = self.expression.generate()

        if self.expression.type_() == "double":
            instructions.append(
                {"trace": self.trace,
                 "op": "a_hi",
                 "z": result_hi,
                 "a": result_hi})
            instructions.append(
                {"trace": self.trace,
                 "op": "a_lo",
                 "z": result,
                 "a": result})
            instructions.append(
                {"trace": self.trace,
                 "op": "long_float_file_write",
                 "file_name": self.name})
        elif self.expression.type_() == "float":
            instructions.append(
                {"trace": self.trace,
                 "op": "float_file_write",
                 "a": result,
                 "file_name": self.name})
        elif self.expression.type_() == "long":
            instructions.append(
                {"trace": self.trace,
                 "op": "a_hi",
                 "z": result_hi,
                 "a": result_hi})
            instructions.append(
                {"trace": self.trace,
                 "op": "a_lo",
                 "z": result,
                 "a": result})
            instructions.append(
                {"trace": self.trace,
                 "op": "long_file_write",
                 "file_name": self.name})
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": "file_write",
                 "a": result,
                 "file_name": self.name})

        return instructions


class Input(Expression):

    def __init__(self, trace, handle):
        self.handle = handle
        self.trace = trace
        Expression.__init__(self, "int", False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append(
            {"trace": self.trace,
             "op": "read",
             "z": result,
             "a": result})
        return instructions


class FileRead(Expression):

    def __init__(self, trace, name):
        self.name = name
        self.trace = trace
        Expression.__init__(self, "int", True)

    def generate(self):
        instructions = []
        instructions.append(
            {"trace": self.trace,
             "op": "file_read",
             "z": result,
             "file_name": self.name})
        return instructions


class Ready(Expression):

    def __init__(self, trace, handle):
        self.handle = handle
        self.trace = trace
        Expression.__init__(self, "int", False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append(
            {"trace": self.trace,
             "op": "ready",
             "z": result,
             "a": result})

        return instructions


class OutputReady(Expression):

    def __init__(self, trace, handle):
        self.handle = handle
        self.trace = trace
        Expression.__init__(self, "int", False)

    def generate(self):
        instructions = self.handle.generate()
        instructions.append(
            {"trace": self.trace,
             "op": "output_ready",
             "z": result,
             "a": result})

        return instructions


class StructMember(Object):

    def __init__(self, trace, struct, member):
        Object.__init__(self, struct)
        self.trace = trace
        self.struct = struct
        self.member = member
        self.struct_offset = struct.type_().member_offset(member)

    def address(self):
        instructions = []
        instructions.extend(self.struct.address())
        instructions.append(
            {"trace": self.trace,
             "op": "addl",
             "z": result,
             "a": result,
             "literal": self.struct_offset})
        return instructions

    def generate(self):
        if is_array_of(self):
            return self.address()
        else:
            instructions = []
            instructions.extend(self.address())
            load_object(
                self.trace,
                instructions,
                n=size_of(self) // 4,
                offset=None,
                local=False)
            return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if size_of(self) == 4:
            push(self.trace, instructions, result)
        elif size_of(self) == 8:
            push(self.trace, instructions, result)
            push(self.trace, instructions, result_hi)
        instructions.extend(self.address())
        instructions.append(
            {"trace": self.trace,
             "op": "addl",
             "z": address,
             "a": result,
             "literal": 0})
        if size_of(self) == 4:
            pop(self.trace, instructions, result)
        elif size_of(self) == 8:
            pop(self.trace, instructions, result_hi)
            pop(self.trace, instructions, result)
        store_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=False,
            leave_on_stack=leave_on_stack)
        return instructions

    def type_(self):
        return self.struct.type_().member_type(self.member)


class ArrayIndex(Object):

    def __init__(self, trace, array, index_expression):
        self.trace = trace
        self.array = array
        self.index_expression = index_expression

    def address(self):
        instructions = []
        if isinstance(self.array, ArrayIndex):
            instructions.extend(self.array.address())
        else:
            instructions.extend(self.array.generate())
        push(self.trace, instructions, result)
        instructions.extend(self.index_expression.generate())
        pop(self.trace, instructions, address)
        if size_of(self) > 4:
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": temp,
                 "literal": size_of(self) // 4})
            instructions.append(
                {"trace": self.trace,
                 "op": "multiply",
                 "z": result,
                 "a": result,
                 "b": temp})
        instructions.append(
            {"trace": self.trace,
             "op": "add",
             "z": result,
             "a": result,
             "b": address})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        load_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=False)
        return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if size_of(self) == 4:
            push(self.trace, instructions, result)
        elif size_of(self) == 8:
            push(self.trace, instructions, result)
            push(self.trace, instructions, result_hi)
        instructions.extend(self.address())
        instructions.append(
            {"trace": self.trace,
             "op": "addl",
             "z": address,
             "a": result,
             "literal": 0})
        if size_of(self) == 4:
            pop(self.trace, instructions, result)
        elif size_of(self) == 8:
            pop(self.trace, instructions, result_hi)
            pop(self.trace, instructions, result)
        store_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=False,
            leave_on_stack=leave_on_stack)
        return instructions

    def type_(self):
        return self.array.type_().base_type()

    def signed(self):
        # This needs work
        return True


class Variable(Object):

    def __init__(self, trace, instance):
        Object.__init__(self, instance)
        self.trace = trace

    def address(self):
        instructions = []
        # if is_array_of(self) and self.instance.argument:
        #    instructions.append(
        #        {"trace": self.trace,
        #         "op": "addl",
        #         "z": result,
        #         "a": frame,
        #         "literal": self.instance.offset})
        #    instructions.append(
        #        {"trace": self.trace,
        #         "op": "load",
        #         "z": result,
        #         "a": result})
        if self.instance.local:
            instructions.append({
                "trace": self.trace,
                "op": "addl",
                "z": result,
                "a": frame,
                "literal": self.instance.offset})
        else:
            instructions.append({
                "trace": self.trace,
                "op": "literal",
                "z": result,
                "literal": self.instance.offset})
        return instructions

    def generate(self):
        instructions = []
        instructions.extend(self.address())
        if is_array_of(self) and not self.instance.argument:
            return instructions
        else:
            load_object(
                self.trace,
                instructions,
                n=size_of(self) // 4,
                offset=None,
                local=True)
            return instructions

    def copy(self, expression, leave_on_stack=True):
        instructions = []
        instructions.extend(expression.generate())
        if self.instance.local:
            instructions.append(
                {"trace": self.trace,
                 "op": "addl",
                 "z": address,
                 "a": frame,
                 "literal": self.instance.offset})
        else:
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": address,
                 "literal": self.instance.offset})
        store_object(
            self.trace,
            instructions,
            n=size_of(self) // 4,
            offset=None,
            local=True)
        return instructions

    def const(self):
        return self.instance.const()

    def value(self):
        if self.const():
            return self.instance.initializer.value()
        else:
            raise NotConstant


class Assignment(Expression):

    def __init__(self, trace, lvalue, expression):
        Expression.__init__(self, lvalue.type_(), lvalue.signed())
        self.trace = trace
        self.lvalue = lvalue
        self.expression = expression

    def discard(self):
        return self.lvalue.copy(self.expression, False)

    def generate(self):
        return self.lvalue.copy(self.expression, True)


class Constant(Expression):

    def __init__(self, trace, value, type_="int", signed=True):
        self.trace = trace
        self._value = value
        Expression.__init__(self, type_, signed)

    def generate(self):

        int_value = self.int_value()
        instructions = []
        if size_of(self) == 4:
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": result,
                 "literal": int_value & 0xffffffff})
        elif size_of(self) == 8:
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": result,
                 "literal": int_value & 0xffffffff})
            instructions.append(
                {"trace": self.trace,
                 "op": "literal",
                 "z": result_hi,
                 "literal": (int_value >> 32) & 0xffffffff})
        else:
            for i in self._value:
                push(self.trace, instructions, i)
        return instructions

    def value(self):
        return self._value


def select_binary_instruction(type_, left_signed, right_signed, operation):
    operation_names = {
        "+": ("add", False, False),
        "-": ("subtract", False, False),
        "/": ("divide", False, True),
        "*": ("multiply", False, False),
        "%": ("modulo", False, False),
        ">": ("greater", False, True),
        ">=": ("greater_equal", False, True),
        "<": ("greater", True, True),
        "<=": ("greater_equal", True, True),
        ">>": ("shift_right", False, True),
        "<<": ("shift_left", False, False),
        "&": ("and", False, False),
        "|": ("or", False, False),
        "^": ("xor", False, False),
        "==": ("equal", False, False),
        "!=": ("not_equal", False, False)
    }

    name, reverse_operands, sign_sensitive = operation_names[operation]

    if type_ == "float":
        name = "float_" + name

    if type_ == "double":
        name = "long_float_" + name

    if type_ == "long":
        name = "long_" + name

    if sign_sensitive and not (left_signed and right_signed):
        name = "unsigned_" + name

    return name, reverse_operands


def select_increment_instruction(type_, signed, operation):
    operation_names = {
        "+": "add",
        "-": "subtract"}

    name = operation_names[operation]

    if type_ == "float":
        name = "float_" + name

    if type_ == "double":
        name = "long_float_" + name

    if type_ == "long":
        name = "long_" + name

    return name
