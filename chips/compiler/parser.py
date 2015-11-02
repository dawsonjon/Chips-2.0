__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct
from copy import copy, deepcopy
from textwrap import dedent

from parse_tree import *
from tokens import Tokens
from allocator import Allocator
from types import *

types = [
    "double",
    "float",
    "signed",
    "unsigned",
    "short",
    "long",
    "char",
    "int",
    "void"]
numeric_types = [
    "double",
    "float",
    "signed",
    "unsigned",
    "short",
    "long",
    "char",
    "int"]
integer_like = ["long", "int"]
storage_specifiers = ["const", "static", "register"]


class Parser:

    """Turn the C input file into a tree of expressions and statements."""

    def __init__(self, input_file, reuse, initialize_memory, parameters):
        self.scope = {}
        self.global_scope = GlobalScope()
        self.function = self.global_scope
        self.loop = None
        self.tokens = Tokens(input_file, parameters)
        self.allocator = Allocator(reuse)
        self.structs = []
        self.initialize_memory = initialize_memory
        self.statement = 0

    def parse_process(self):
        process = Process(Trace(self))
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

        for function in process.functions:
            if hasattr(function, "name") and function.name == "main":
                self.main = function
                break
        if not hasattr(self, "main"):
            self.tokens.error("Function main has not been defined")

        process.main = self.main
        process.scope = self.scope
        self.main.referenced = True
        return process

    def parse_type_specifier(self):
        type_specifiers = []

        while self.tokens.peek() in types + self.structs + storage_specifiers:
            type_specifiers.append(self.tokens.get())

        type_ = "int"
        signed = True
        if "unsigned" in type_specifiers:
            signed = False
            if "signed" in type_specifiers:
                self.tokens.error("Cannot be signed and unsigned")

        if "long" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Cannot be long and short")
            type_ = "long"

        for i in type_specifiers:
            if i in self.structs:
                type_ = self.scope[i]

        if "float" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Float cannot be short")
            if "long" in type_specifiers:
                self.tokens.error("Float cannot be long (but double can)")
            if "unsigned" in type_specifiers:
                self.tokens.error("Float cannot be unsigned")
            type_ = "float"
            signed = True

        if "double" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Double cannot be short")
            if "unsigned" in type_specifiers:
                self.tokens.error("Double cannot be unsigned")
            type_ = "double"
            signed = True

        const = False
        if "const" in type_specifiers:
            const = True

        if "void" in type_specifiers:
            type_ = "void"
            signed = False

        while self.tokens.peek() == "*":
            self.tokens.expect("*")
            type_ = PointerTo(type_)

        return TypeSpecifier(type_, signed, const)

    def parse_argument(self):
        type_specifier = self.parse_type_specifier()
        if self.tokens.peek() not in [",", ")"]:
            argument = self.tokens.get()
        else:
            argument = None

        if type_specifier.type_ == "void":
            self.tokens.error("argument cannot be void")

        if type_specifier.type_ in self.structs:
            type_ = self.scope[type_].type_

        # Gather dimensions of sub arrays
        if self.tokens.peek() == "[":
            type_specifier.type_ = ArrayOf(type_specifier.type_)
            type_specifier.type_.dimensions = []
            while self.tokens.peek() == "[":
                self.tokens.expect("[")
                if self.tokens.peek() != "]":
                    size_expression = self.parse_ternary_expression()
                    if size_expression.type_() not in integer_like:
                        self.tokens.error(
                            "Array size must be an integer like expression")
                    try:
                        type_specifier.type_.dimensions.append(
                            size_expression.value())
                    except NotConstant:
                        self.tokens.error("Array size must be constant")
                else:
                    type_specifier.type_.dimensions.append(None)
                self.tokens.expect("]")

            # Encapsulate elements in arrays, starting from the right most
            for number_of_elements in type_specifier.type_.dimensions[1:]:
                if number_of_elements is None:
                    self.tokens.error(
                        "Inner array range must be specified")

            # force inner dimension to None so that size is 4 for array args
            type_specifier.type_.dimensions[0] = None
            type_specifier.type_.dimensions.reverse()

        return argument, type_specifier

    def parse_function(self):

        # Check the type specification
        #
        type_specifier = self.parse_type_specifier()
        name = self.tokens.get()

        # create a separate namespace for goto statements in each function
        self.goto_labels = {}

        # At this point we don;t know whether this is a function or a variable
        # check for a ( and make a decision.
        #
        if self.tokens.peek() != "(":
            return self.parse_global_declaration(name, type_specifier)

        msg = [dedent(i) for i in [

               "%s was previously declared, but was not a function.",

               """Function type differs from previous function declaration
        expected: %s got: %s""",

               """Function signedness differs from previous function declaration
        expected: %s got: %s""",

               """Argument constness differs from previous function declaration
        expected: %s got: %s""",

               ]]

        if name in self.scope:
            allready_defined = True
            function = self.scope[name]
            old_type = function.type_()
            old_signed = function.signed()
            old_const = function.const()

            if not isinstance(function, Function):
                self.tokens.error(msg[0] % (name))
            if type_specifier.type_ != old_type:
                self.tokens.error(msg[1] % (type_specifier.type_, old_type))
            if type_specifier.signed != old_signed:
                self.tokens.error(msg[2] % (type_specifier.signed, old_signed))
            if type_specifier.const != old_const:
                self.tokens.error(msg[3] % (type_specifier.const, old_const))
        else:
            allready_defined = False
            function = Function(
                Trace(self),
                name,
                type_specifier,
            )
            function.has_definition = False
            self.scope[function.name] = function

        # store the scope so that we can put it back when we are done
        stored_scope = copy(self.scope)
        self.function = function

        arguments = []
        self.tokens.expect("(")
        while self.tokens.peek() != ")":
            arguments.append(self.parse_argument())
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")

        # arguments have offsets before the frame pointer
        # for every argument decrease the offset by the size of the
        # argument so that the offsets are correctly assigned later.
        #
        # Exception - arrays are passed as references not copies
        # argument_size returns the size of an array reference
        # in this case, but in all other cases returns the size of an object.
        for argument, argument_declaration in arguments:
            function.offset -= type_arg_size(argument_declaration.type_) // 4

        msg = [dedent(i) for i in [

               """Function has a different number of arguments to previous
        declaration""",

               """Argument type differs from previous function declaration
        expected: %s got: %s""",

               """Argument signedness differs from previous function declaration
        expected: %s got: %s""",

               """Argument constness differs from previous function declaration
        expected: %s got: %s""",

               ]]

        # arguments look like a series of declarations, for each argument
        # create an instance - like a local variable.
        # Exception - arrays are passed as references not copies
        # argument instance returns an instance of a reference to an array
        # in this case, but in all other cases returns an instance of an
        # object.
        if allready_defined:
            old_arguments = iter(function.arguments)
            if len(function.arguments) != len(arguments):
                self.tokens.error(msg[0])

        function.arguments = []
        for argument, argument_declaration in arguments:
            # The name of an argument may differ from a previous declaration
            # The type may not
            if allready_defined:
                old_argument = next(old_arguments)
                old_type = old_argument.type_()
                old_signed = old_argument.signed()
                old_const = old_argument.const()
                if argument_declaration.type_ != old_type:
                    self.tokens.error(msg[1] % (
                        argument_declaration.type_,
                        old_type
                    ))
                if argument_declaration.signed != old_signed:
                    self.tokens.error(msg[2] % (
                        argument_declaration.signed,
                        old_signed,
                    ))
                if argument_declaration.const != old_const:
                    self.tokens.error(msg[3] % (
                        argument_declaration.const,
                        old_const,
                    ))
            instance = Argument(
                Trace(self),
                argument_declaration,
                self.function)
            self.scope[argument] = instance
            function.arguments.append(instance.reference(Trace(self)))
            function.local_variables[argument] = instance

        # A function declaration is distinct from a function definition
        # a function may be declared many times, but defined only once.
        if self.tokens.peek() == ";":
            self.tokens.expect(";")
        else:
            if function.has_definition:
                self.tokens.error(
                    "Function %s has already been defined" % name
                )
            function.has_definition = True
            function.statement = self.parse_statement()
            if type_specifier.type_ != "void" and not hasattr(function, "return_statement"):
                self.tokens.error(
                    "Non-void function must have a return statement")

        # Put back the scope as it was
        #
        self.function = self.global_scope
        self.scope = stored_scope

        return function

    def parse_break(self):
        break_ = Break(Trace(self))
        break_.loop = self.loop
        self.tokens.expect("break")
        self.tokens.expect(";")
        return break_

    def parse_continue(self):
        continue_ = Continue(Trace(self))
        continue_.loop = self.loop
        self.tokens.expect("continue")
        self.tokens.expect(";")
        return continue_

    def parse_return(self):
        return_ = Return(Trace(self))
        return_.function = self.function
        self.function.return_statement = return_
        self.tokens.expect("return")

        if self.function.type_() != "void":
            expression = self.parse_expression()

            if self.function.type_() == "double":
                expression = self.to_double(expression)
            elif self.function.type_() == "float":
                expression = self.to_float(expression)
            elif self.function.type_() == "long":
                expression = self.to_long(expression)
            elif self.function.type_() == "int":
                expression = self.to_int(expression)
            elif not self.function.type_() == expression.type_():
                self.tokens.error(
                    "type mismatch in return statement expected: %s actual: %s" % (
                        self.function.type_(),
                        expression.type_()))

            return_.expression = expression

        self.tokens.expect(";")
        return return_

    def parse_assert(self):
        assert_ = Assert(Trace(self))
        self.tokens.expect("assert")
        self.tokens.expect("(")
        assert_.expression = self.parse_assignment()
        self.tokens.expect(")")
        self.tokens.expect(";")
        assert_.line = self.tokens.lineno
        assert_.filename = self.tokens.filename
        return assert_

    def parse_report(self):
        report_ = Report(Trace(self))
        self.tokens.expect("report")
        self.tokens.expect("(")
        report_.expression = self.parse_assignment()
        self.tokens.expect(")")
        self.tokens.expect(";")
        report_.line = self.tokens.lineno
        report_.filename = self.tokens.filename
        return report_

    def parse_goto(self):
        self.tokens.expect("goto")
        label_name = self.tokens.get()
        self.tokens.expect(";")
        return Goto(Trace(self), self.goto_labels, label_name)

    def parse_wait_clocks(self):
        wait_clocks = WaitClocks(Trace(self))
        self.tokens.expect("wait_clocks")
        self.tokens.expect("(")
        wait_clocks.expression = self.parse_assignment()
        self.tokens.expect(")")
        self.tokens.expect(";")
        wait_clocks.line = self.tokens.lineno
        return wait_clocks

    def parse_timer_low(self):
        timer = TimerLow(Trace(self))
        self.tokens.expect("(")
        self.tokens.expect(")")
        timer.line = self.tokens.lineno
        return timer

    def parse_timer_high(self):
        timer = TimerHigh(Trace(self))
        self.tokens.expect("(")
        self.tokens.expect(")")
        timer.line = self.tokens.lineno
        return timer

    def parse_statement(self):
        self.statement += 1

        if (self.tokens.peek_next() == ":" and
                self.tokens.peek() not in ["default", "case"]):
            label_name = self.tokens.get()
            self.tokens.expect(":")
            label = Label(Trace(self), self.parse_statement())
            if label_name in self.goto_labels:
                self.tokens.error("label %s is already defined" % label_name)
            self.goto_labels[label_name] = label
            return label
        elif self.tokens.peek() in numeric_types + self.structs + storage_specifiers:
            return self.parse_compound_declaration()
        elif self.tokens.peek() == "struct":
            return self.parse_struct_declaration()
        elif self.tokens.peek() == "if":
            return self.parse_if()
        elif self.tokens.peek() == "while":
            return self.parse_while()
        elif self.tokens.peek() == "do":
            return self.parse_do_while()
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
        elif self.tokens.peek() == "goto":
            return self.parse_goto()
        elif self.tokens.peek() == "wait_clocks":
            return self.parse_wait_clocks()
        else:
            expression = self.parse_discard()
            self.tokens.expect(";")
            return expression

    def parse_discard(self):
        return DiscardExpression(Trace(self), self.parse_expression())

    def parse_assignment(self):
        assignment_operators = [
            "=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="
        ]
        lvalue = self.parse_ternary_expression()
        if self.tokens.peek() in assignment_operators:

            # Check that lvalue is modifiable
            #
            if lvalue.const():
                self.tokens.error(
                    "left hand operand of assignment is not modifiable")
            if not hasattr(lvalue, "copy"):
                self.tokens.error("lvalue is not modifiable in assignment")

            # Create the expression and the lvalue
            #
            operator = self.tokens.get()
            if operator == "=":
                expression = self.parse_assignment()
            else:
                expression = self.parse_assignment()
                expression = self.binary(operator[:-1], lvalue, expression)

            # Promote numeric types
            #
            if is_double(lvalue):
                expression = self.to_double(expression)
            elif is_float(lvalue):
                expression = self.to_float(expression)
            elif is_long(lvalue):
                expression = self.to_long(expression)
            elif is_int(lvalue):
                expression = self.to_int(expression)
            elif is_array_of(lvalue):
                self.tokens.error(
                    "assignment is not permitted for arrays")
            elif not compatible(expression, lvalue):
                self.tokens.error(
                    "type mismatch in assignment expected: %s actual: %s" % (
                        lvalue.type_(),
                        expression.type_()))

            return Assignment(Trace(self), lvalue, expression)
        else:
            return lvalue

    def parse_if(self):
        if_ = If(Trace(self))
        self.tokens.expect("if")
        self.tokens.expect("(")
        if_.expression = self.parse_expression()
        if if_.expression.type_() not in integer_like:
            self.tokens.error(
                "if statement conditional must be an integer like expression")
        self.tokens.expect(")")
        if_.true_statement = self.parse_statement()
        if self.tokens.peek() == "else":
            self.tokens.expect("else")
            if_.false_statement = self.parse_statement()
        else:
            if_.false_statement = None
        return if_

    def parse_switch(self):
        switch = Switch(Trace(self))
        switch.cases = {}
        self.tokens.expect("switch")
        self.tokens.expect("(")
        expression = self.parse_expression()
        if expression.type_() not in integer_like:
            self.tokens.error(
                "switch statement expression must be an integer like expression")
        self.tokens.expect(")")
        stored_loop = self.loop
        self.loop = switch
        statement = self.parse_statement()
        self.loop = stored_loop
        switch.expression = expression
        switch.statement = statement
        return switch

    def parse_case(self):
        self.tokens.expect("case")
        expression = self.parse_ternary_expression()
        if expression.type_() not in integer_like:
            self.tokens.error(
                "case expression must be an integer like expression")
        self.tokens.expect(":")
        try:
            expression = expression.value()
            case = Case(Trace(self))
            self.loop.cases[expression] = case
        except NotConstant:
            self.tokens.error("case expression must be constant")
        except AttributeError:
            self.tokens.error(
                "case statements may only be use inside a switch statment")
        return case

    def parse_default(self):
        self.tokens.expect("default")
        self.tokens.expect(":")
        default = Default(Trace(self))
        if not hasattr(self.loop, "cases"):
            self.tokens.error(
                "default statements may only be used inside a switch statment")
        if hasattr(self.loop, "default"):
            self.tokens.error(
                "A switch statement may only have one default statement")
        self.loop.default = default
        return default

    def parse_while(self):
        loop = Loop(Trace(self))
        self.tokens.expect("while")
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        stored_loop = self.loop
        self.loop = loop
        statement = self.parse_statement()
        self.loop = stored_loop
        if_ = If(Trace(self))
        loop.statement = if_
        break_ = Break(Trace(self))
        break_.loop = loop
        if expression.type_() not in integer_like:
            self.tokens.error(
                "while statement conditional must be an integer like expression")
        if_.expression = expression
        if_.false_statement = break_
        if_.true_statement = statement
        return loop

    def parse_do_while(self):

        # compile the loop
        loop = Loop(Trace(self))
        self.tokens.expect("do")
        stored_loop = self.loop
        self.loop = loop
        self.loop = stored_loop
        statement = self.parse_statement()
        self.tokens.expect("while")
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        self.tokens.expect(";")

        # construct a conditional that will break if false
        # or continue if true
        break_ = Break(Trace(self))
        break_.loop = loop
        continue_ = Continue(Trace(self))
        continue_.loop = loop
        if_ = If(Trace(self))
        if_.expression = expression
        if_.false_statement = break_
        if_.true_statement = continue_

        # form the body of the loop from the compiled loop
        # followed by the conditional statement
        block = Block(Trace(self))
        block.statements = [statement, if_]
        loop.statement = block

        # check that the loop condition is like an integer
        if expression.type_() not in integer_like:
            self.tokens.error(
                "do while statement conditional must be an integer like expression")
        return loop

    def parse_for(self):
        for_ = For(Trace(self))
        self.tokens.expect("for")
        self.tokens.expect("(")
        if self.tokens.peek() != ";":
            for_.statement1 = self.parse_discard()
        self.tokens.expect(";")
        if self.tokens.peek() != ";":
            for_.expression = self.parse_expression()
            if for_.expression.type_() not in integer_like:
                self.tokens.error(
                    "For statement conditional must be an integer like expression")

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
        block = Block(Trace(self))
        stored_scope = copy(self.scope)
        self.tokens.expect("{")
        block.statements = []
        while self.tokens.peek() != "}":
            block.statements.append(self.parse_statement())
        self.tokens.expect("}")
        self.scope = stored_scope
        return block

    def parse_struct_body(self):
        self.tokens.expect("{")
        member_names = []
        member_types = []
        while self.tokens.peek() != "}":
            type_specifier = self.parse_type_specifier()
            name = self.tokens.get()
            name, type_specifier = self.parse_declaration(name, type_specifier)
            member_names.append(name)
            member_types.append(type_specifier.type_)
            self.tokens.expect(";")
        self.tokens.expect("}")
        return StructOf(member_names, member_types)

    def parse_typedef_struct(self):
        self.tokens.expect("typedef")
        self.tokens.expect("struct")
        declaration = self.parse_struct_body()
        name = self.tokens.get()
        self.tokens.expect(";")
        self.scope[name] = declaration
        self.structs.append(name)

    def parse_define_struct(self):
        self.tokens.expect("struct")
        name = self.tokens.get()
        declaration = self.parse_struct_body()
        self.tokens.expect(";")
        self.scope[name] = declaration

    def parse_struct_declaration(self):
        self.tokens.expect("struct")
        struct_name = self.tokens.get()
        name = self.tokens.get()
        self.tokens.expect(";")
        type_ = self.scope[struct_name]
        instance = LocalVariable(
            Trace(self),
            TypeSpecifier(type_, False, False),
            None,
            self.function
        )
        self.function.local_variables[name] = instance
        self.scope[name] = instance
        return instance

    def parse_global_declaration(self, name, type_specifier):
        """global_declaration := "{"
            declaration
            *["," declaration]
            ";"
        """

        instances = []
        while True:

            type_specifier, initializer = self.parse_instance(
                name, type_specifier)
            instance = GlobalVariable(
                Trace(self),
                type_specifier,
                initializer,
                self.function
            )
            self.function.global_variables[name] = instance
            self.scope[name] = instance
            instances.append(instance)
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
            name = self.tokens.get()
        self.tokens.expect(";")
        return CompoundDeclaration(instances)

    def parse_compound_declaration(self):
        """compound_declaration := "{"
            declaration
            *["," declaration]
            ";"
        """

        type_specifier = self.parse_type_specifier()
        instances = []
        while True:
            name = self.tokens.get()
            new_type_specifier, initializer = self.parse_instance(
                name, type_specifier)
            instance = LocalVariable(
                Trace(self),
                new_type_specifier,
                initializer,
                self.function
            )

            self.function.local_variables[name] = instance
            self.scope[name] = instance
            instances.append(instance)
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
            name = None
        self.tokens.expect(";")
        return CompoundDeclaration(instances)

    def parse_array_initializer(self, type_):
        """array_initialiser := "{"
             [array_initializer | variable_initializer]
            *["," [array_initializer | variable_initializer]] "}"
        """

        self.tokens.expect("{")
        elements = []
        while True:
            if self.tokens.peek() == "{":
                elements.append(self.parse_array_initializer(type_))
            else:
                elements.append(
                    self.parse_variable_initializer(type_.root_type()))
            if self.tokens.peek() == "}":
                break
            self.tokens.expect(",")
        self.tokens.expect("}")
        return elements

    def parse_string_initializer(self, type_specifier):
        """string_initialiser := "\"" *[character] "\"" """

        if type_specifier.type_.base_type() not in integer_like:
            self.tokens.error("unsuitable array type for string initializer")
        initializer = self.tokens.get()
        initializer = [
            Constant(
                Trace(self),
                ord(i)
            )
            for i in initializer.strip('"').decode("string_escape")
        ]
        initializer += [Constant(Trace(self), 0)]
        return initializer

    def parse_variable_initializer(self, type_):
        """variable_initialiser := parse_ternary_expression"""

        initializer = self.parse_ternary_expression()
        if type_ == "double":
            initializer = self.to_double(initializer)
        elif type_ == "float":
            initializer = self.to_float(initializer)
        elif type_ == "long":
            initializer = self.to_long(initializer)
        elif type_ == "int":
            initializer = self.to_int(initializer)
        elif type_ != initializer.type_():
            self.tokens.error(
                "type mismatch in initializer expected: %s actual: %s" % (
                    type_,
                    initializer.type_()))

        return initializer

    def parse_declaration(self, name, type_specifier):
        """declaration := type_specifier name
            *["[" ternary_expression "]"]
        """

        type_ = deepcopy(type_specifier.type_)
        signed = type_specifier.signed
        const = type_specifier.const

        if type_ in self.structs:
            type_ = self.scope[type_]

        # Gather dimensions of arrays
        if self.tokens.peek() == "[":
            type_ = ArrayOf(type_)
            type_.dimensions = []

            while self.tokens.peek() == "[":
                self.tokens.expect("[")
                if self.tokens.peek() != "]":
                    size_expression = self.parse_ternary_expression()
                    if size_expression.type_() not in integer_like:
                        self.tokens.error(
                            "Array size must be an integer like expression")
                    try:
                        type_.dimensions.append(size_expression.value())
                    except NotConstant:
                        self.tokens.error("Array size must be constant")
                else:
                    type_.dimensions.append(None)
                self.tokens.expect("]")

            # Encapsulate elements in arrays, starting from the right most
            for number_of_elements in type_.dimensions[1:]:
                if number_of_elements is None:
                    self.tokens.error("Inner array range must be specified")

            type_.dimensions.reverse()

        return name, TypeSpecifier(type_, signed, const)

    def parse_instance(self, name, type_specifier):
        """declaration
        ?["=" [string_initialiser | array_initialiser | variable_initialiser]]
        ]
        """

        name, type_specifier = self.parse_declaration(name, type_specifier)

        # Array Initialiser
        initializer = None
        if self.tokens.peek() == "=":
            self.tokens.expect("=")

            # initialize as a string
            if self.tokens.peek().startswith('"'):
                initializer = self.parse_string_initializer(type_specifier)

                # Not strictly correct initialization behaviour
                if type_specifier.type_.dimensions[-1] is None:
                    type_specifier.type_.dimensions[-1] = len(initializer)
                elif type_specifier.type_.dimensions[-1] != len(initializer):
                    self.tokens.error(
                        "Array initializer does not match array dimensions")

            elif self.tokens.peek() == "{":
                initializer = self.parse_array_initializer(
                    type_specifier.type_)

                # Not strictly correct initialization behaviour
                if type_specifier.type_.dimensions[-1] is None:
                    type_specifier.type_.dimensions[-1] = len(initializer)
                elif type_specifier.type_.dimensions[-1] != len(initializer):
                    self.tokens.error(
                        "Array initializer does not match array dimensions")

            else:
                initializer = self.parse_variable_initializer(
                    type_specifier.type_)

        if hasattr(type_specifier.type_, "dimensions") and type_specifier.type_.dimensions[-1] is None:
            self.tokens.error(
                "Array size must be specified if not initialized")

        return type_specifier, initializer

    def parse_expression(self):
        """expression := assignment"""

        expression = self.parse_assignment()
        while self.tokens.peek() == ",":
            self.tokens.expect(",")
            expression = MultiExpression(
                Trace(self),
                expression,
                [self.parse_assignment()]
            )
        return expression

    def parse_ternary_expression(self):
        """ternary_expression := or_expression "?" or_expression ":" or_expression"""

        expression = constant_fold(Trace(self), self.parse_or_expression())
        while self.tokens.peek() in ["?"]:
            if expression.type_() not in integer_like:
                self.tokens.error(
                    "Condition in ternary expression must be an integer like type")
            self.tokens.expect("?")
            true_expression = constant_fold(
                Trace(self),
                self.parse_or_expression())
            self.tokens.expect(":")
            false_expression = constant_fold(
                Trace(self),
                self.parse_or_expression())
            true_expression, false_expression = self.coerce_types(
                true_expression,
                false_expression,
                ":"
            )
            expression = Ternary(
                Trace(self),
                expression,
                true_expression,
                false_expression)
        return expression

    def parse_or_expression(self):
        """or_expression := and_expression *["||" and_expression]"""

        expression = self.parse_and_expression()
        while self.tokens.peek() in ["||"]:
            self.tokens.expect("||")
            right = self.parse_and_expression()
            expression, right = self.coerce_integer_types(expression, right)
            expression = OR(Trace(self), expression, right)
        return expression

    def parse_and_expression(self):
        """and_expression := binary_expression *["&&" binary_expression]"""

        expression = self.parse_binary_expression(["|"])
        while self.tokens.peek() in ["&&"]:
            self.tokens.expect("&&")
            right = self.parse_binary_expression(["|"])
            expression, right = self.coerce_integer_types(expression, right)
            expression = AND(Trace(self), expression, right)
        return expression

    def substitute_function(self, binary_expression):
        """For some operations are more easily implemented in software.
        This function substitutes a call to the builtin library function.
        """

        functions = {
            # signed,left,right,size,operator
            "False,int,/": "unsigned_divide_xxxx",
            "True,int,/": "divide_xxxx",
            "False,int,%": "unsigned_modulo_xxxx",
            "True,int,%": "modulo_xxxx",

            "True,float,==": "float_equal_xxxx",
            "True,float,!=": "float_ne_xxxx",
            "True,float,<": "float_lt_xxxx",
            "True,float,>": "float_gt_xxxx",
            "True,float,<=": "float_le_xxxx",
            "True,float,>=": "float_ge_xxxx",

            "True,double,==": "long_float_equal_xxxx",
            "True,double,!=": "long_float_ne_xxxx",
            "True,double,<": "long_float_lt_xxxx",
            "True,double,>": "long_float_gt_xxxx",
            "True,double,<=": "long_float_le_xxxx",
            "True,double,>=": "long_float_ge_xxxx",

            "False,long,/": "long_unsigned_divide_xxxx",
            "True,long,/": "long_divide_xxxx",
            "False,long,%": "long_unsigned_modulo_xxxx",
            "True,long,%": "long_modulo_xxxx",
        }

        # select a function that matches the template.
        signature = ",".join([
            str(binary_expression.signed()),
            "%s" % binary_expression.left.type_(),
            binary_expression.operator])

        # Some things can't be implemented in verilog, substitute them with a
        # function
        if signature in functions:
            function = self.scope[functions[signature]]
            function_call = FunctionCall(Trace(self), function)
            self.function.called_functions.append(function)
            function_call.arguments = [
                binary_expression.left,
                binary_expression.right
            ]
            return function_call
        else:
            return binary_expression

    def coerce_types(self, left, right, operation):
        """Convert numeric types in expressions."""

        if is_double(left) or is_double(right):
            right = self.to_double(right)
            left = self.to_double(left)
        elif is_float(left) or is_float(right):
            right = self.to_float(right)
            left = self.to_float(left)
        elif is_long(left) or is_long(right):
            right = self.to_long(right)
            left = self.to_long(left)
        elif is_pointer_to(left) and is_pointer_to(right):
            if operation not in ["-", "!=", "==", "<", ">", ">=", "<="]:
                self.tokens.error("Operation is permitted for two pointers : %s %s" % (
                    left.type_(),
                    right.type_(),
                ))
            if left.type_() != right.type_():
                self.tokens.error("pointer types must be identical : %s %s" % (
                    left.type_(),
                    right.type_(),
                ))

        elif is_pointer_to(left):
            if operation not in ["+", "-"]:
                self.tokens.error("Only addition and subtraction are permitted for pointer arithmetic: %s %s" % (
                    left.type_(),
                    right.type_(),
                ))
            if right.type_() not in integer_like:
                self.tokens.error("Only integer like expressions may be used in pointer arithmetic : %s %s" % (
                    left.type_(),
                    right.type_(),
                ))

        elif is_pointer_to(right):
            if operation not in ["+", "-"]:
                self.tokens.error("Only addition and subtraction are permitted for pointer arithmetic: %s %s" % (
                    left.type_(),
                    right.type_(),
                ))
            if left.type_() not in integer_like:
                self.tokens.error("Only integer like expressions may be used in pointer arithmetic : %s %s" % (
                    left.type_(),
                    right.type_(),
                ))

        elif left.type_() != right.type_():
            self.tokens.error("Incompatible types : %s %s" % (
                left.type_(),
                right.type_(),
            ))

        return left, right

    def coerce_integer_types(self, left, right):
        """Convert integer types in expressions."""

        if is_long(left) or is_long(right):
            right = self.to_long(right)
            left = self.to_long(left)
        elif left.type_() not in ("int", "long"):
            self.tokens.error("Incompatible types : %s %s" % (
                left.type_(),
                right.type_(),
            ))
        elif right.type_() not in ("int", "long"):
            self.tokens.error("Incompatible types : %s %s" % (
                left.type_(),
                right.type_(),
            ))
        elif left.type_() != right.type_():
            self.tokens.error("Incompatible sizes : %s %s" % (
                left.size(),
                right.size(),
            ))

        return left, right

    def parse_binary_expression(self, operators):
        """binary_expression := unary_expression operator
        *unary_expression"""

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
            left = self.parse_unary_expression()
            while self.tokens.peek() in operators:
                operator = self.tokens.get()
                right = self.parse_unary_expression()
                left = self.binary(operator, left, right)
            return left
        else:
            next_operators = operator_precedence[operators[0]]
            left = self.parse_binary_expression(next_operators)
            while self.tokens.peek() in operators:
                operator = self.tokens.get()
                right = self.parse_binary_expression(next_operators)
                left = self.binary(operator, left, right)
            return left

    def parse_unary_expression(self):
        """unary_expression := ?[
            "&" |
            "*" |
            "!" |
            "-" |
            "~" |
            "++" |
            "--" |
            "(" type ")"
        ] postfix_expreession

        """

        if self.tokens.peek() == "!":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()

            if expression.type_() not in integer_like:
                self.tokens.error(
                    "! is only valid for integer like expressions")

            return Binary(Trace(self), "==", expression, Constant(Trace(self), 0))

        elif self.tokens.peek() == "-":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()
            return Binary(
                Trace(self),
                "-",
                Constant(
                    Trace(self),
                    0,
                    expression.type_(),
                    expression.signed()
                ),
                expression
            )

        elif self.tokens.peek() == "&":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()
            return Address(Trace(self), expression)

        elif self.tokens.peek() == "*":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()
            return Dereference(Trace(self), expression)

        elif self.tokens.peek() == "~":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()

            if expression.type_() not in integer_like:
                self.tokens.error(
                    "~ is only valid for integer like expressions")

            return Unary(Trace(self), "~", expression)

        elif self.tokens.peek() in ["++", "--"]:
            operator = self.tokens.get()
            expression = self.parse_unary_expression()
            expression = Assignment(
                Trace(self),
                expression,
                Binary(
                    Trace(self),
                    operator[0],
                    expression,
                    Constant(
                        Trace(self),
                        1,
                        expression.type_(),
                        expression.signed()
                    ),
                ),
            )
            return expression

        elif self.tokens.peek() == "sizeof":
            self.tokens.get()
            expression = self.parse_unary_expression()
            return SizeOf(Trace(self), expression)

        # cast operation
        elif self.tokens.peek() == "(" and self.tokens.peek_next() in numeric_types:
            self.tokens.expect("(")
            type_specifier = self.parse_type_specifier()
            self.tokens.expect(")")
            expression = self.parse_unary_expression()

            if type_specifier.type_ == "double":
                expression = self.to_double(expression)
            elif type_specifier.type_ == "float":
                expression = self.to_float(expression)
            elif type_specifier.type_ == "long":
                expression = self.to_long(expression)
            elif type_specifier.type_ == "int":
                expression = self.to_int(expression)
            elif (hasattr(type_specifier.type_, "is_pointer_to") and
                    hasattr(expression.type_(), "is_pointer_to")):
                expression = self.to_pointer(expression, type_specifier.type_)
            elif (hasattr(type_specifier.type_, "is_pointer_to") and
                    expression.type_() in integer_like):
                expression = self.to_pointer(
                    self.to_int(expression),
                    type_specifier.type_)
            elif type_specifier.type_ != expression.type_():
                self.tokens.error(
                    "cannot cast incompatible types expected: %s actual: %s" % (
                        type_specifier.type_,
                        expression.type_()))

            return expression

        else:
            return self.parse_postfix_expression()

    def parse_postfix_expression(self):
        """postfix_expression := primary_expression *[
                function_call |
                array_index |
                struct_member |
                ++ |
                --
            ]
        """

        expression = self.parse_primary_expression()

        while self.tokens.peek() in ["(", "[", ".", "->", "++", "--"]:

            if self.tokens.peek() == "(":
                expression = self.parse_function_call(expression)
            elif self.tokens.peek() == "[":
                expression = self.parse_array_index(expression)
            elif self.tokens.peek() == ".":
                expression = self.parse_struct_member(expression)
            elif self.tokens.peek() == "->":
                expression = self.parse_struct_pointer_access(expression)
            elif self.tokens.peek() in ["++", "--"]:
                operator = self.tokens.get()
                expression = MultiExpression(
                    Trace(self),
                    expression,
                    [Assignment(
                        Trace(self),
                        expression,
                        Binary(
                            Trace(self),
                            operator[0],
                            expression,
                            Constant(
                                Trace(self),
                                1,
                                expression.type_(),
                                expression.signed()
                            ),
                        ),
                    )],
                )

        return expression

    def parse_primary_expression(self):
        """primary_expression := (expression) | name | literal"""

        if self.tokens.peek() == "(":
            self.tokens.expect("(")
            expression = self.parse_expression()
            self.tokens.expect(")")
        elif self.tokens.peek()[0].isalpha():
            name = self.tokens.get()
            if name == "input":
                expression = self.parse_input()
            elif name == "output":
                expression = self.parse_output()
            elif name == "fgetc":
                expression = self.parse_fgetc()
            elif name == "fputc":
                expression = self.parse_fputc()
            elif name == "ready":
                expression = self.parse_ready()
            elif name == "output_ready":
                expression = self.parse_output_ready()
            elif name == "file_read":
                expression = self.parse_file_read()
            elif name == "file_write":
                expression = self.parse_file_write()
            elif name == "double_to_bits":
                expression = self.parse_double_to_bits()
            elif name == "float_to_bits":
                expression = self.parse_float_to_bits()
            elif name == "bits_to_double":
                expression = self.parse_bits_to_double()
            elif name == "bits_to_float":
                expression = self.parse_bits_to_float()
            elif name == "timer_high":
                expression = self.parse_timer_high()
            elif name == "timer_low":
                expression = self.parse_timer_low()
            else:
                if name not in self.scope:
                    self.tokens.error(
                        "%s is not declared in current scope" % name)
                instance = self.scope[name]
                if not hasattr(instance, "local"):
                    self.tokens.error(
                        "%s is not is not an instance in the current scope" % name)
                # store inside the current function any globals that get
                # referenced if a global isn't referenced it doesn't get
                # compiled
                if not instance.local:
                    self.function.referenced_globals.append(instance)
                expression = instance.reference(Trace(self))
        else:
            expression = self.parse_literal()

        return expression

    def parse_array_index(self, array):
        """parse an index into an array i.e. [] operation"""

        self.tokens.expect("[")
        index_expression = self.parse_expression()
        self.tokens.expect("]")
        if not (is_array_of(array) or is_pointer_to(array)):
            self.tokens.error(
                "Cannot index non-array type %s" % array.type_())
        if index_expression.type_() not in integer_like:
            self.tokens.error(
                "Array indices must be an integer like expression")
        return ArrayIndex(Trace(self), array, index_expression)

    def parse_struct_member(self, struct):
        """parse a member of a struct i.e. . operation"""

        self.tokens.expect(".")

        if not is_struct_of(struct):
            self.tokens.error(
                "Cannot access member of non-struct type %s" % struct.type_())
        member = self.tokens.get()
        if member not in struct.type_().names:
            self.tokens.error("%s is not a member of struct" % member)
        return StructMember(Trace(self), struct, member)

    def parse_struct_pointer_access(self, struct):
        """parse a member of a struct i.e. . operation"""

        self.tokens.expect("->")
        struct = Dereference(Trace(self), struct)

        if not is_struct_of(struct):
            self.tokens.error(
                "Cannot access member of non-struct type %s" % struct.type_())
        member = self.tokens.get()
        if member not in struct.type_().names:
            self.tokens.error("%s is not a member of struct" % member)

        return StructMember(
            Trace(self),
            struct,
            member)

    def parse_file_read(self):
        """parse the built-in function file_read"""

        self.tokens.expect("(")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileRead(Trace(self), file_name)

    def parse_file_write(self):
        """parse the built-in function file_write"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(",")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileWrite(Trace(self), file_name, expression)

    def parse_double_to_bits(self):
        """parse the built-in function double_to_bits"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(")")
        return DoubleToBits(Trace(self), self.to_double(expression))

    def parse_float_to_bits(self):
        """parse the built-in function float_to_bits"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(")")
        return FloatToBits(Trace(self), self.to_float(expression))

    def parse_bits_to_double(self):
        """parse the built-in function bits_to_float"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(")")
        return BitsToDouble(Trace(self), self.to_long(expression))

    def parse_bits_to_float(self):
        """parse the built-in function bits_to_float"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(")")
        return BitsToFloat(Trace(self), self.to_int(expression))

    def parse_input(self):
        """parse the built-in function input"""

        self.tokens.expect("(")
        input_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(Trace(self), self.allocator.new_input(input_name))

    def parse_fgetc(self):
        """parse the built-in function fgetc"""

        self.tokens.expect("(")
        handle = self.parse_assignment()
        self.tokens.expect(")")
        return Input(Trace(self), handle)

    def parse_ready(self):
        """parse the built-in function ready"""

        self.tokens.expect("(")
        handle = self.parse_assignment()
        self.tokens.expect(")")
        return Ready(Trace(self), handle)

    def parse_output_ready(self):
        """parse the built-in function ready"""

        self.tokens.expect("(")
        handle = self.parse_assignment()
        self.tokens.expect(")")
        return OutputReady(Trace(self), handle)

    def parse_output(self):
        """parse the built-in function output"""

        self.tokens.expect("(")
        output_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(Trace(self), self.allocator.new_output(output_name))

    def parse_fputc(self):
        """parse the built-in function fputc"""

        self.tokens.expect("(")
        expression = self.parse_assignment()
        self.tokens.expect(",")
        handle = self.parse_assignment()
        self.tokens.expect(")")
        return Output(Trace(self), handle, expression)

    def parse_function_call(self, function):
        """parse a function call"""

        # Pass the function call
        #
        function_call = FunctionCall(Trace(self), function)
        self.function.called_functions.append(function)
        function_call.arguments = []
        self.tokens.expect("(")
        while self.tokens.peek() != ")":
            function_call.arguments.append(self.parse_assignment())
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")

        # Check that the thing being called is a function
        #
        if not hasattr(function_call.function, "arguments"):
            self.tokens.error(
                "not a function cannot be called")

        # Check that the correct number of arguments has been given
        #
        required_arguments = len(function_call.function.arguments)
        actual_arguments = len(function_call.arguments)
        if required_arguments != actual_arguments:
            self.tokens.error("Function takes %s arguments %s given." % (
                len(function_call.function.arguments),
                len(function_call.arguments)))

        # Check that each argument is of a suitable type for the function
        # being called. Some numerical types may be promoted during function
        # calls
        #
        required_arguments = function_call.function.arguments
        actual_arguments = function_call.arguments
        corrected_arguments = []
        for required, actual in zip(required_arguments, actual_arguments):
            if not compatible(required, actual):

                # attempt to promote numeric types
                if required.type_() == "double":
                    actual = self.to_double(actual)
                elif required.type_() == "float":
                    actual = self.to_float(actual)
                elif required.type_() == "long":
                    actual = self.to_long(actual)
                elif required.type_() == "int":
                    actual = self.to_int(actual)

                # types should match
                elif required.type_() != actual.type_():
                    self.tokens.error(
                        "type mismatch in function_argument expected: %s actual: %s" % (
                            required.type_(),
                            actual.type_()))

            corrected_arguments.append(actual)
        function_call.arguments = corrected_arguments

        return function_call

    def parse_literal(self):
        """parse a literal"""

        token = self.tokens.get()
        if token.startswith("'"):
            return self.parse_character_literal(token)
        elif token.startswith('"'):
            return self.parse_string_literal(token)
        elif "." in token:
            return self.parse_floating_point_literal(token)
        else:
            return self.parse_integer_literal(token)

    def parse_character_literal(self, token):
        """parse a character literal"""

        type_ = "int"
        signed = True
        try:
            token = eval(token)
            value = ord(token)
            return Constant(Trace(self), value, type_, signed)
        except SyntaxError:
            self.tokens.error("%s is not a character literal" % token)
        except TypeError:
            self.tokens.error("%s is not a character literal" % token)

    def parse_string_literal(self, token):
        """parse a string literal"""

        try:
            initializer = [
                Constant(
                    Trace(self),
                    ord(i)
                )
                for i in token.strip('"').decode("string_escape")
            ]
            initializer += [Constant(Trace(self), 0)]
            # initialize_memory = self.initialize_memory
            instance = GlobalVariable(
                Trace(self),
                TypeSpecifier(
                    ArrayOf("int",
                            [len(initializer)]),
                    False,
                    False),
                initializer,
                self.function,
            )
            # since we don't return instance, it doesn't get generated.
            # treat as a global
            self.function.global_variables[
                "const_char_%s" % id(instance)] = instance
            self.function.referenced_globals.append(instance)
            return instance.reference(Trace(self))
        except SyntaxError:
            self.tokens.error("%s is not a character literal" % token)

    def parse_floating_point_literal(self, token):
        """parse a floating point literal"""

        try:
            if "F" in token.upper():
                type_ = "float"
                signed = True
                token = token.upper().replace("F", "")
                value = float(eval(token))
                try:
                    struct.pack(">f", value)
                except OverflowError:
                    self.tokens.error("value too large")
            else:
                type_ = "double"
                signed = True
                value = float(eval(token))
                try:
                    struct.pack(">d", value)
                except OverflowError:
                    self.tokens.error("value too large")
            return Constant(Trace(self), value, type_, signed)
        except SyntaxError:
            self.tokens.error("%s is not a floating point literal" % token)

    def parse_integer_literal(self, token):
        """parse an integer literal"""

        type_ = "int"
        signed = True
        size = 4
        try:
            if "U" in token.upper():
                signed = False
            if "L" in token.upper():
                type_ = "long"
                size = 8
            token = token.upper().replace("U", "")
            value = int(eval(token))
            if signed:
                if value > 2 ** ((size * 8) - 1) - 1:
                    self.tokens.error("value too large")
                if value < -(2 ** ((size * 8) - 1)):
                    self.tokens.error("value too small")
            else:
                if value > 2 ** (size * 8) - 1:
                    self.tokens.error("value too large")
                if value < 0:
                    self.tokens.error("value too small")
            return Constant(Trace(self), value, type_, signed)
        except SyntaxError:
            self.tokens.error("%s is not an integer literal" % token)

    def to_double(self, expression):
        """Convert (any type which can be converted) to a double"""

        if is_double(expression):
            return expression
        elif is_float(expression):
            return FloatToDouble(Trace(self), expression)
        elif is_long(expression):
            return LongToDouble(Trace(self), expression)
        elif is_int(expression):
            return LongToDouble(
                Trace(self),
                IntToLong(Trace(self), expression)
            )
        else:
            self.tokens.error(
                "cannot convert expression with type %s to double" % (
                    expression.type_())
            )

    def to_float(self, expression):
        """Convert (any type which can be converted) to a float"""

        if is_double(expression):
            return DoubleToFloat(Trace(self), expression)
        elif is_float(expression):
            return expression
        elif is_long(expression):
            return DoubleToFloat(
                Trace(self),
                LongToDouble(Trace(self),
                             expression)
            )
        elif is_int(expression):
            return IntToFloat(Trace(self), expression)
        else:
            self.tokens.error(
                "cannot convert expression with type %s to float" % expression.type_())

    def to_long(self, expression):
        """Convert (any type which can be converted) to a long"""

        if is_double(expression):
            return DoubleToLong(Trace(self), expression)
        elif is_float(expression):
            return DoubleToLong(Trace(self), FloatToDouble(Trace(self), expression))
        elif is_long(expression):
            return expression
        elif is_int(expression):
            return IntToLong(Trace(self), expression)
        else:
            self.tokens.error(
                "cannot convert expression with type %s to long" %
                expression.type_())

    def to_int(self, expression):
        """Convert (any type which can be converted) to an int"""

        if is_double(expression):
            return LongToInt(Trace(self), DoubleToLong(Trace(self), expression))
        elif is_float(expression):
            return FloatToInt(Trace(self), expression)
        elif is_long(expression):
            return LongToInt(Trace(self), expression)
        elif is_int(expression):
            return expression
        else:
            self.tokens.error(
                "cannot convert expression with type %s to int" %
                expression.type_())

    def to_pointer(self, expression, type_):
        """Convert pointer to anything or an integer to an pointer to type"""

        return PointerCast(Trace(self), expression, type_)

    def binary(self, operator, left, right):
        """Create a Binary Expression object

        Coerce numeric types following standard promotion rules.
        Where a binary operation is implemented in software substitute a function call.
        """

        left, right = self.coerce_types(left, right, operator)
        expression = Binary(Trace(self), operator, left, right)
        expression = self.substitute_function(expression)
        return expression
