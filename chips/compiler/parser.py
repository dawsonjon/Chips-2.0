__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct
from copy import copy

from parse_tree import *
from tokens import Tokens
from allocator import Allocator

types = ["double", "float", "signed", "unsigned", "short", "long", "char", "int", "void"]
numeric_types = ["double", "float", "signed", "unsigned", "short", "long", "char", "int"]
storage_specifiers = ["const"]

class GlobalScope:
    def __init__(self):
        self.offset = 0
        self.is_global = True


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
        process.scope = self.scope
        self.main.referenced = True
        return process

    def parse_type_specifier(self):
        type_specifiers = []

        while self.tokens.peek() in types + self.structs + storage_specifiers:
            type_specifiers.append(self.tokens.get())

        signed = True
        if "unsigned" in type_specifiers:
            signed = False
            if "signed" in type_specifiers:
                self.tokens.error("Cannot be signed and unsigned")

        size = 4
        if "long" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Cannot be long and short")
            size = 8

        type_ = "int"
        for i in type_specifiers:
            if i in self.structs:
                type_ = i
                size = 4
                signed = False

        if "float" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Float cannot be short")
            if "long" in type_specifiers:
                self.tokens.error("Float cannot be long (but double can)")
            if "unsigned" in type_specifiers:
                self.tokens.error("Float cannot be unsigned")
            type_ = "float"
            size = 4
            signed = True

        if "double" in type_specifiers:
            if "short" in type_specifiers:
                self.tokens.error("Double cannot be short")
            if "unsigned" in type_specifiers:
                self.tokens.error("Double cannot be unsigned")
            type_ = "float"
            size = 8
            signed = True

        const = False 
        if "const" in type_specifiers:
            const = True

        if "void" in type_specifiers:
            type_ = "void"
            size = 0
            signed = False


        return type_, size, signed, const

    def parse_argument(self):
        type_, size, signed, const = self.parse_type_specifier()

        if type_ in ["void"]:
            self.tokens.error("argument cannot be void")
        else:
            argument = self.tokens.get()
            if type_ in self.structs:
                declaration = self.scope[type_]
            else:
                if self.tokens.peek() == "[":
                    self.tokens.expect("[")
                    self.tokens.expect("]")
                    declaration = ArrayDeclaration(
                        size = 4,
                        type_ = type_+"[]",
                        element_type = type_,
                        element_size = size,
                        element_signed = signed,
                    )
                else:
                    declaration = VariableDeclaration(
                        None,
                        argument,
                        type_,
                        size,
                        signed,
                        const)
        instance = declaration.argument_instance(self.function)
        print instance, self.function
        self.scope[argument] = instance
        return instance.reference()

    def parse_function(self):

        #Check the type specification
        #
        type_, size, signed, const = self.parse_type_specifier()
        name = self.tokens.get()

        #At this point we don;t know whether this is a function or a variable
        #check for a ( and make a decision.
        #
        if self.tokens.peek() != "(":
            return self.parse_global_declaration(type_, size, signed, const, name)

        #parse the function argument list
        #
        self.tokens.expect("(")
        #store the scope so that we can put it back when we are done
        stored_scope = copy(self.scope)
        function = Function(name, type_, size, signed)
        self.function = function
        function.arguments = []
        while self.tokens.peek() != ")":
            function.arguments.append(self.parse_argument())
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")
        function.statement = self.parse_statement()
        
        if type_ != "void" and not hasattr(function, "return_statement"):
            self.tokens.error("Non-void function must have a return statement")

        #Put back the scope as it was
        #
        self.function = self.global_scope
        self.scope = stored_scope
        #remember to add the funcion we have just defined to the global scope
        self.scope[function.name] = function
        #the last function to be compiled is considered the main function
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

        if self.function.type_() != "void":
            expression = self.parse_expression()

            if self.function.type_() == "float" and self.function.size() == 8:
                expression = self.to_double(expression)
            elif self.function.type_() == "float" and self.function.size() == 4:
                expression = self.to_float(expression)
            elif self.function.type_() == "int" and self.function.size() == 8:
                expression = self.to_long(expression)
            elif self.function.type_() == "int" and self.function.size() == 4:
                expression = self.to_int(expression)
            elif self.function.type_() != expression.type_():
                self.tokens.error(
                    "type mismatch in return statement expected: %s actual: %s"%(
                        self.function.type_(),
                        expression.type_()))
            elif self.function.size() != expression.size():
                self.tokens.error(
                    "type mismatch in return statement expected: %s actual: %s"%(
                        self.function.size(),
                        expression.size()))

            return_.expression = expression

        self.tokens.expect(";")
        return return_

    def parse_assert(self):
        assert_ = Assert()
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
        self.tokens.expect("wait_clocks")
        self.tokens.expect("(")
        wait_clocks.expression = self.parse_expression()
        self.tokens.expect(")")
        self.tokens.expect(";")
        wait_clocks.line = self.tokens.lineno
        return wait_clocks

    def parse_statement(self):
        if self.tokens.peek() in numeric_types + self.structs + storage_specifiers:
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
        return DiscardExpression(self.parse_expression())

    def parse_assignment(self):
        assignment_operators = [
            "=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="
        ]
        lvalue = self.parse_ternary_expression()
        if self.tokens.peek() in assignment_operators:
            if lvalue.const():
                self.tokens.error(
                    "left hand operand of assignment is not modifiable")

            operator = self.tokens.get()
            if operator == "=":
                expression = self.parse_ternary_expression()
            else:
                expression = self.parse_ternary_expression()
                left = lvalue
                left, expression = self.coerce_types(left, expression)
                expression = Binary(operator[:-1], left, expression)
                expression = self.substitute_function(expression)

            if is_double(lvalue):
                expression = self.to_double(expression)
            elif is_float(lvalue):
                expression = self.to_float(expression)
            elif is_long(lvalue):
                expression = self.to_long(expression)
            elif is_int(lvalue):
                expression = self.to_int(expression)
            elif expression.type_() != lvalue.type_():
                self.tokens.error(
                    "type mismatch in assignment expected: %s actual: %s"%(
                        lvalue.type_(),
                        expression.type_()))
            elif expression.size() != lvalue.size():
                self.tokens.error(
                    "size mismatch in assignment expected: %s actual: %s"%(
                        lvalue.size(),
                        expression.size()))

            if not hasattr(lvalue, "copy"):
                self.tokens.error("lvalue is not modifiable in assignment")

            return Assignment(lvalue, expression)
        else:
            return lvalue

    def parse_if(self):
        if_ = If()
        self.tokens.expect("if")
        self.tokens.expect("(")
        if_.expression = self.parse_expression()
        if if_.expression.type_() not in ["unsigned", "int", "short", "long", "char"]:
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
        switch = Switch()
        switch.cases = {}
        self.tokens.expect("switch")
        self.tokens.expect("(")
        expression = self.parse_expression()
        if expression.type_() not in ["int"]:
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
        expression = self.parse_expression()
        if expression.type_() not in ["int"]:
            self.tokens.error(
                "case expression must be an integer like expression")
        self.tokens.expect(":")
        try:
            expression = expression.value()
            case = Case()
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
        default = Default()
        if not hasattr(self.loop, "cases"):
            self.tokens.error(
                "default statements may only be used inside a switch statment")
        if hasattr(self.loop, "default"):
            self.tokens.error(
                "A switch statement may only have one default statement")
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
        if expression.type_() not in ["int"]:
            self.tokens.error(
                "while statement conditional must be an integer like expression")
        if_.expression = expression
        if_.false_statement = break_
        if_.true_statement = statement

        return loop

    def parse_for(self):
        for_ = For()
        self.tokens.expect("for")
        self.tokens.expect("(")
        if self.tokens.peek() != ";":
            for_.statement1 = self.parse_discard()
        self.tokens.expect(";")
        if self.tokens.peek() != ";":
            for_.expression = self.parse_expression()
            if for_.expression.type_() not in [
                "unsigned", 
                "int", 
                "short", 
                "long", 
                "char"]:

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
        block = Block()
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
        members = {}
        while self.tokens.peek() != "}":
            type_, size, signed, const = self.parse_type_specifier()
            name = self.tokens.get()

            members[name] = self.parse_declaration(
                type_, 
                size, 
                signed, 
                const,
                name)

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
        instance = self.scope[struct_name].instance(self.function)
        self.scope[name] = instance
        return instance

    def parse_global_declaration(self, type_, size, signed, const, name):
        instances = []
        while True:

            instance = self.parse_declaration(
                type_, 
                size, 
                signed, 
                const,
                name).instance(self.function)

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
        type_, size, signed, const = self.parse_type_specifier()
        instances = []
        while True:
            name = self.tokens.get()

            instance = self.parse_declaration(
                type_, 
                size, 
                signed, 
                const,
                name).instance(self.function)

            self.scope[name] = instance
            instances.append(instance)
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
            name = None
        self.tokens.expect(";")
        return CompoundDeclaration(instances)

    def parse_declaration(self, type_, size, signed, const, name):
        #struct declaration
        if type_ in self.structs:
            declaration = self.scope[type_]
        elif type_ in ["int", "float"]:
            #array declaration
            if self.tokens.peek() == "[":
                array_size = None
                self.tokens.expect("[")
                if self.tokens.peek() != "]":
                    size_expression = self.parse_ternary_expression()
                    if size_expression.type_() != "int":
                        self.tokens.error("Array size must be an integer like expression")
                    try:
                        array_size = size_expression.value()
                    except NotConstant:
                        self.tokens.error("Array size must be constant")

                self.tokens.expect("]")
                initializer = None
                if self.tokens.peek() == "=":
                    self.tokens.expect("=")
                    initializer = self.tokens.get()
                    initializer = [ord(i) for i in initializer.strip('"').decode("string_escape")] + [0]
                    array_size = len(initializer)
                if array_size is None:

                    self.tokens.error(
                        "array size must be specified if not initialized")

                array_type=type_+"[]"
                declaration = ArrayDeclaration(
                    size = array_size,
                    type_ = array_type,
                    element_type = type_,
                    element_size = size,
                    element_signed = signed,
                    initializer = initializer,
                )

            #simple variable declaration
            else:
                if self.tokens.peek() == "=":
                    self.tokens.expect("=")
                    initializer = self.parse_ternary_expression()
                else:
                    initializer = Constant(0, type_, size, signed)


                if type_ == "float" and size == 8:
                    initializer = self.to_double(initializer)
                elif type_ == "float" and size == 4:
                    initializer = self.to_float(initializer)
                elif type_ == "int" and size == 8:
                    initializer = self.to_long(initializer)
                elif type_ == "int" and size == 4:
                    initializer = self.to_int(initializer)
                elif type_ != initializer.type_():
                    self.tokens.error(
                        "type mismatch in intializer expected: %s actual: %s"%(
                            type_,
                            initializer.type_()))
                elif size != initializer.size():
                    self.tokens.error(
                        "size mismatch in intializer expected: %s actual: %s"%(
                            size,
                            initializer.size()))

                declaration = VariableDeclaration(
                    initializer,
                    name,
                    type_,
                    size,
                    signed,
                    const
                )

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
            expression, true_expression = self.coerce_integer_types(expression, true_expression)
            true_expression, false_expression = self.coerce_integer_types(true_expression, false_expression)
            expression = OR(AND(expression, true_expression), false_expression)
        return expression

    def parse_or_expression(self):
        expression = self.parse_and_expression()
        while self.tokens.peek() in ["||"]:
            self.tokens.expect("||")
            right = self.parse_and_expression()
            expression, right = self.coerce_integer_types(expression, right)
            expression = OR(expression, right)
        return expression

    def parse_and_expression(self):
        expression = self.parse_binary_expression(["|"])
        while self.tokens.peek() in ["&&"]:
            self.tokens.expect("&&")
            right = self.parse_binary_expression(["|"])
            expression, right = self.coerce_integer_types(expression, right)
            expression = AND(expression, right)
        return expression

    def substitute_function(self, binary_expression):

        """
        For some operations are more easily implemented in software.
        This function substitutes a call to the builtin library function.
        """

        functions = {
           #signed,left,right,size,operator
           "False,int,int,4,/" : "unsigned_divide_xxxx",
           "True,int,int,4,/" : "divide_xxxx",
           "False,int,int,4,%" : "unsigned_modulo_xxxx",
           "True,int,int,4,%" : "modulo_xxxx",

           "True,float,float,4,==" : "float_equal_xxxx",
           "True,float,float,4,!=" : "float_ne_xxxx",
           "True,float,float,4,<" : "float_lt_xxxx",
           "True,float,float,4,>" : "float_gt_xxxx",
           "True,float,float,4,<=" : "float_le_xxxx",
           "True,float,float,4,>=" : "float_ge_xxxx",

           "True,float,float,8,==" : "long_float_equal_xxxx",
           "True,float,float,8,!=" : "long_float_ne_xxxx",
           "True,float,float,8,<" : "long_float_lt_xxxx",
           "True,float,float,8,>" : "long_float_gt_xxxx",
           "True,float,float,8,<=" : "long_float_le_xxxx",
           "True,float,float,8,>=" : "long_float_ge_xxxx",

           "False,int,int,8,/" : "long_unsigned_divide_xxxx",
           "True,int,int,8,/" : "long_divide_xxxx",
           "False,int,int,8,%" : "long_unsigned_modulo_xxxx",
           "True,int,int,8,%" : "long_modulo_xxxx",
        }

        #select a function that matches the template.
        signature = ",".join([
            str(binary_expression.signed()), 
            binary_expression.left.type_(), 
            binary_expression.right.type_(), 
            str(binary_expression.left.size()), 
            binary_expression.operator])

        #Some things can't be implemented in verilog, substitute them with a function
        if signature in functions:
            function = self.scope[functions[signature]]
            function_call = FunctionCall(function)
            self.function.called_functions.append(function)
            function_call.arguments = [binary_expression.left, binary_expression.right]
            return function_call
        else:
            return binary_expression

    def coerce_types(self, left, right):

        """
        Convert numeric types in expressions.
        """

        if is_double(left) or is_double(right):
            right = self.to_double(right)
            left = self.to_double(left)
        elif is_float(left) or is_float(right):
            right = self.to_float(right)
            left = self.to_float(left)
        elif is_long(left) or is_long(right):
            right = self.to_long(right)
            left = self.to_long(left)
        elif left.type_() != right.type_():
            self.tokens.error("Incompatible types : %s %s"%(
                left.type_(),
                right.type_(),
                ))
        elif left.size() != right.size():
            self.tokens.error("Incompatible sizes : %s %s"%(
                left.size(),
                right.size(),
                ))

        return left, right

    def coerce_integer_types(self, left, right):

        """
        Convert integer types in expressions.
        """

        if is_long(left) or is_long(right):
            right = self.to_long(right)
            left = self.to_long(left)
        elif left.type_() != "int":
            self.tokens.error("Incompatible types : %s %s"%(
                left.type_(),
                right.type_(),
                ))
        elif right.type_() != "int":
            self.tokens.error("Incompatible types : %s %s"%(
                left.type_(),
                right.type_(),
                ))
        elif left.size() != right.size():
            self.tokens.error("Incompatible sizes : %s %s"%(
                left.size(),
                right.size(),
                ))

        return left, right

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
            left = self.parse_unary_expression()
            while self.tokens.peek() in operators:
                operator = self.tokens.get()
                right = self.parse_unary_expression()
                left, right = self.coerce_types(left, right)
                left = Binary(operator, left, right)
                left = self.substitute_function(left)
            return left
        else:
            next_operators = operator_precedence[operators[0]]
            left = self.parse_binary_expression(next_operators)
            while self.tokens.peek() in operators:
                operator = self.tokens.get()
                right = self.parse_binary_expression(next_operators)
                left, right = self.coerce_types(left, right)
                left = Binary(operator, left, right)
                left = self.substitute_function(left)
            return left

    def parse_unary_expression(self):

        if self.tokens.peek() == "!":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()

            if expression.type_() not in ["int"]:
                self.tokens.error(
                    "! is only valid for integer like expressions")

            return Binary("==", expression, Constant(0))

        elif self.tokens.peek() == "-":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()
            return Binary("-", Constant(0, 
                expression.type_(), 
                expression.size(), 
                expression.signed()), 
                expression)

        elif self.tokens.peek() == "~":
            operator = self.tokens.get()
            expression = self.parse_postfix_expression()

            if expression.type_() not in ["int"]:
                self.tokens.error(
                    "~ is only valid for integer like expressions")

            return Unary("~", expression)

        elif self.tokens.peek() == "sizeof":
            operator = self.tokens.get()
            expression = self.parse_unary_expression()
            return SizeOf(expression)

        #cast operation
        elif self.tokens.peek() == "(" and self.tokens.peek_next() in numeric_types:
            self.tokens.expect("(")
            type_, size, signed, const = self.parse_type_specifier()
            self.tokens.expect(")")
            expression = self.parse_unary_expression()

            if type_ == "float" and size == 8:
                expression = self.to_double(expression)
            elif type_ == "float" and size == 4:
                expression = self.to_float(expression)
            elif type_ == "int" and size == 8:
                expression = self.to_long(expression)
            elif type_ == "int" and size == 4:
                expression = self.to_int(expression)
            elif type_ != expression.type_():
                self.tokens.error(
                    "cannot cast incompatible types expected: %s actual: %s"%(
                        type_,
                        expression.type_()))
            elif size != expression.size():
                self.tokens.error(
                    "cannot cast incompatible types expected: %s actual: %s"%(
                        size,
                        expression.size()))
            
            return expression

        else:
            return self.parse_postfix_expression()

    def parse_postfix_expression(self):
        expression = self.parse_paren_expression()
        while self.tokens.peek() in ["++", "--"]:
            operator = self.tokens.get()
            expression = PostIncrement(
                operator[:-1],
                expression,
            )
        return expression

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

    def parse_file_read(self):
        self.tokens.expect("(")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileRead(file_name)

    def parse_file_write(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(",")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileWrite(file_name, expression)

    def parse_double_to_bits(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return DoubleToBits(self.to_double(expression))

    def parse_float_to_bits(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return FloatToBits(self.to_float(expression))

    def parse_bits_to_double(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return BitsToDouble(self.to_long(expression))

    def parse_bits_to_float(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return BitsToFloat(self.to_int(expression))

    def parse_input(self):
        self.tokens.expect("(")
        input_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(self.allocator.new_input(input_name))

    def parse_fgetc(self):
        self.tokens.expect("(")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Input(handle)

    def parse_ready(self):
        self.tokens.expect("(")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Ready(handle)

    def parse_output(self):
        self.tokens.expect("(")
        output_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(self.allocator.new_output(output_name))

    def parse_fputc(self):
        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(",")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Output(handle, expression)

    def parse_function_call(self, name):

        #First filter out built-in "functions"
        #
        if name == "input":
            return self.parse_input()
        if name == "output":
            return self.parse_output()
        if name == "fgetc":
            return self.parse_fgetc()
        if name == "fputc":
            return self.parse_fputc()
        if name == "ready":
            return self.parse_ready()
        if name == "file_read":
            return self.parse_file_read()
        if name == "file_write":
            return self.parse_file_write()
        if name == "double_to_bits":
            return self.parse_double_to_bits()
        if name == "float_to_bits":
            return self.parse_float_to_bits()
        if name == "bits_to_double":
            return self.parse_bits_to_double()
        if name == "bits_to_float":
            return self.parse_bits_to_float()
        if name not in self.scope:
            self.tokens.error("Unknown function: %s"%name)

        #Pass the function call
        #
        function = self.scope[name]
        function_call = FunctionCall(function)
        self.function.called_functions.append(function)
        function_call.arguments = []
        self.tokens.expect("(")
        while self.tokens.peek() != ")":
            function_call.arguments.append(self.parse_expression())
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")

        #Check that the thing being called is a function
        #
        if not hasattr(function_call.function, "arguments"):
            self.tokens.error("%s is not a function and cannot be called"%name)

        #Check that the correct number of arguments has been given
        #
        required_arguments = len(function_call.function.arguments)
        actual_arguments = len(function_call.arguments)
        if required_arguments != actual_arguments:
            self.tokens.error("Function %s takes %s arguments %s given."%(
                name,
                len(function_call.function.arguments),
                len(function_call.arguments)))

        #Check that each argument is of a suitable type for the function being called
        #Some numerical types may be promoted during function calls
        #
        required_arguments = function_call.function.arguments
        actual_arguments = function_call.arguments
        corrected_arguments = []
        for required, actual in zip(required_arguments, actual_arguments):
            if not compatible(required, actual):

                #attempt to promote numeric types
                if required.type_() == "float" and required.size() == 8:
                    actual = self.to_double(actual)
                elif required.type_() == "float" and required.size() == 4:
                    actual = self.to_float(actual)
                elif required.type_() == "int" and required.size() == 8:
                    actual = self.to_long(actual)
                elif required.type_() == "int" and required.size() == 4:
                    actual = self.to_int(actual)

                #types should match
                elif required.type_() != actual.type_():
                    self.tokens.error(
                        "type mismatch in assignment expected: %s actual: %s"%(
                            required.type_(),
                            actual.type_()))

                #size should match for non-arrays
                elif not required.type_().endswith("[]") and required.size() != actual.size():
                    self.tokens.error(
                        "size mismatch in function argument expected: %s actual: %s"%(
                            required.size(),
                            actual.size()))

                #element size should match for arrays
                elif required.type_().endswith("[]") and required.element_size != actual.element_size:
                    self.tokens.error(
                        "element size mismatch in function argument expected: %s actual: %s"%(
                            required.element_size(),
                            actual.element_size()))

            corrected_arguments.append(actual)
        function_call.arguments = corrected_arguments

        return function_call

    def parse_number(self):
        token = self.tokens.get()
        type_ = "int"
        size = 4
        signed = True
        if token.startswith("'"):
            return self.parse_character_literal(token)
        elif token.startswith('"'):
            return self.parse_string_literal(token)
        elif "." in token:
            return self.parse_floating_point_literal(token)
        else:
            return self.parse_integer_literal(token)

    def parse_character_literal(self, token):
        type_ = "int"
        size = 4
        signed = True
        try:
            token = eval(token)
            value = ord(token)
            return Constant(value, type_, size, signed)
        except SyntaxError:
            self.tokens.error("%s is not a character literal"%token)

    def parse_string_literal(self, token): 
        type_ = "int"
        size = 4
        signed = True
        try:
            initializer = [ord(i) for i in token.strip('"').decode("string_escape")] + [0]
            size = len(initializer)
            initialize_memory = self.initialize_memory
            declaration = ArrayDeclaration(
                size = size,
                type_ = "int[]",
                element_type = "int",
                element_size = 4,
                element_signed = False,
                initializer = initializer
            )
            instance = declaration.instance(self.function)
            #since we don't return instance, it doesn't get generated.
            #treat as a global
            instance.local = False
            self.function.referenced_globals.append(instance)
            return instance.reference()
        except SyntaxError:
            self.tokens.error("%s is not a character literal"%token)

    def parse_floating_point_literal(self, token): 
        type_ = "int"
        size = 4
        signed = True
        try:
            if "F" in token.upper():
                type_ = "float"
                signed = True
                size = 4
                token = token.upper().replace("F", "")
                token = token.upper().replace("L", "")
                value = float(eval(token))
                try:
                    byte_value = struct.pack(">f", value)
                except OverflowError:
                    self.tokens.error("value too large")
            else:
                type_ = "float"
                signed = True
                size = 8
                token = token.upper().replace("L", "")
                value = float(eval(token))
                try:
                    byte_value = struct.pack(">d", value)
                except OverflowError:
                    self.tokens.error("value too large")
            return Constant(value, type_, size, signed)
        except SyntaxError:
            self.tokens.error("%s is not a floating point literal"%token)

    def parse_integer_literal(self, token): 
        type_ = "int"
        size = 4
        signed = True
        try:
            if "U" in token.upper():
                signed = False
            if "L" in token.upper():
                size = 8
            token = token.upper().replace("U", "")
            value = int(eval(token))
            if signed:
                if value > 2**((size * 8)-1) - 1:
                    self.tokens.error("value too large")
                if value < -(2**((size * 8)-1)):
                    self.tokens.error("value too small")
            else:
                if value > 2**(size * 8) - 1:
                    self.tokens.error("value too large")
                if value < 0:
                    self.tokens.error("value too small")
            return Constant(value, type_, size, signed)
        except SyntaxError:
            self.tokens.error("%s is not an integer literal"%token)

    def parse_variable(self, name):
        if name not in self.scope:
            self.tokens.error("Unknown variable: %s"%name)
        instance = self.scope[name]
        if not hasattr(instance, "local"):
                self.tokens.error("%s does not name an object"%name)
        return self.parse_variable_array_struct(instance)

    def parse_variable_array_struct(self, instance):

        #store inside the current function any globals that get referenced
        #if a global isn't referenced it doesn't get compiled
        #
        if not instance.local:
            self.function.referenced_globals.append(instance)

        #parse simple numeric variables
        #
        if instance.type_() in numeric_types:
            if not hasattr(instance, "reference"):
                self.tokens.error(
                    "Not an expression")
            return Variable(instance)

        #parse arrays
        #
        elif instance.type_().endswith("[]"):
            array = instance.reference()
            if self.tokens.peek() == "[":
                self.tokens.expect("[")
                index_expression = self.parse_expression()
                self.tokens.expect("]")
                if index_expression.type_() not in ["int"]:
                    self.tokens.error(
                        "Array indices must be an integer like expression")
                return ArrayIndex(array, index_expression)
            else:
                return array

        #parse structs
        #
        elif instance.type_().startswith("struct"):
            if self.tokens.peek() == ".":
                self.tokens.expect(".")
                member = self.tokens.get()
                return self.parse_variable_array_struct(
                    instance.members[member],
                )
            else:
                return Struct(instance)

    def to_double(self, expression):
        if is_double(expression):
            return expression
        elif is_float(expression):
            return FloatToDouble(expression)
        elif is_long(expression):
            return LongToDouble(expression)
        elif is_int(expression):
            return LongToDouble(IntToLong(expression))
        else:
            self.tokens.error(
                "cannot convert expression with type %s to double"%expression.type_())

    def to_float(self, expression):
        if is_double(expression):
            return DoubleToFloat(expression)
        elif is_float(expression):
            return expression
        elif is_long(expression):
            return DoubleToFloat(LongToDouble(expression))
        elif is_int(expression):
            return IntToFloat(expression)
        else:
            self.tokens.error("cannot convert expression with type %s to float"%expression.type_())

    def to_long(self, expression):
        if is_double(expression):
            return DoubleToLong(expression)
        elif is_float(expression):
            return DoubleToLong(FloatToDouble(expression))
        elif is_long(expression):
            return expression
        elif is_int(expression):
            return IntToLong(expression)
        else:
            self.tokens.error("cannot convert expression with type %s to long"%expression.type_())

    def to_int(self, expression):
        if is_double(expression):
            return LongToInt(DoubleToLong(expression))
        elif is_float(expression):
            return FloatToInt(expression)
        elif is_long(expression):
            return LongToInt(expression)
        elif is_int(expression):
            return expression
        else:
            self.tokens.error("cannot convert expression with type %s to int"%expression.type_())

def compatible(left, right):
    return left.type_() == right.type_() and left.size() == right.size()

def is_double(expression):
    return expression.size() == 8 and expression.type_() == "float"

def is_float(expression):
    return expression.size() == 4 and expression.type_() == "float"

def is_long(expression):
    return expression.size() == 8 and expression.type_() == "int"

def is_int(expression):
    return expression.size() == 4 and expression.type_() == "int"


