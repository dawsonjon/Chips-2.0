__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

import struct
import sys
from copy import copy
from operator import mul

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
        self.referenced_globals = []


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
                size = self.scope[i].size()
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
        argument = self.tokens.get()

        if type_ in ["void"]:
            self.tokens.error("argument cannot be void")
        elif type_ in self.structs:
            declaration = self.scope[type_]
        else:
            declaration = VariableDeclaration(
                argument,
                type_,
                size,
                signed,
                const
            )

        #Gather dimensions of subarrays
        array_number_of_elements = []
        while self.tokens.peek() == "[":
            self.tokens.expect("[")
            if self.tokens.peek() != "]":
                size_expression = self.parse_ternary_expression()
                if size_expression.type_() != "int":
                    self.tokens.error("Array size must be an integer like expression")
                try:
                    array_number_of_elements.append(size_expression.value())
                except NotConstant:
                    self.tokens.error("Array size must be constant")
            else:
                array_number_of_elements.append(None)
            self.tokens.expect("]")

        array_number_of_elements.reverse()

        #Encapsulate elements in arrays, starting from the right most
        for number_of_elements in array_number_of_elements[:-1]:
            if number_of_elements is None:
                self.tokens.error("Inner array range must be specified")
            declaration = ArrayDeclaration(
                elements = number_of_elements,
                element_declaration = declaration,
            )
        for number_of_elements in array_number_of_elements[-1:]:
            #if number_of_elements is None:
            number_of_elements = 1
            declaration = ArrayDeclaration(
                elements = number_of_elements,
                element_declaration = declaration,
            )

        return argument, declaration

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
        function = Function(name, type_, size, signed)
        #add the function to the scope before starting
        self.scope[function.name] = function
        #store the scope so that we can put it back when we are done
        stored_scope = copy(self.scope)
        self.function = function
        arguments = []
        while self.tokens.peek() != ")":
            arguments.append(self.parse_argument())
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")
        for argument, declaration in arguments:
            function.offset -= declaration.size()//4
        function.arguments = []
        for argument, declaration in arguments:
            instance = declaration.argument_instance(self.function)
            self.scope[argument] = instance
            function.arguments.append(instance.reference())
        function.statement = self.parse_statement()
        if type_ != "void" and not hasattr(function, "return_statement"):
            self.tokens.error("Non-void function must have a return statement")

        #Put back the scope as it was
        #
        self.function = self.global_scope
        self.scope = stored_scope
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
                    "size mismatch in return statement expected: %s actual: %s"%(
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
            
            #Check that lvalue is modifiable
            #
            if lvalue.const():
                self.tokens.error(
                    "left hand operand of assignment is not modifiable")
            if not hasattr(lvalue, "copy"):
                self.tokens.error("lvalue is not modifiable in assignment")

            #Create the expression and the lvalue
            #
            operator = self.tokens.get()
            if operator == "=":
                expression = self.parse_ternary_expression()
            else:
                expression = self.parse_ternary_expression()
                expression = self.binary(operator[:-1], lvalue, expression)

            #Promote numberic types
            #
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

    def parse_do_while(self):

        #compile the loop
        loop = Loop()
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

        #construct a conditional that will break if false
        #or continue if true
        break_ = Break()
        break_.loop = loop
        continue_ = Continue()
        continue_.loop = loop
        if_ = If()
        if_.expression = expression
        if_.false_statement = break_
        if_.true_statement = continue_

        #form the body of the loop from the compiled loop
        #followed by the conditional statement
        block = Block()
        block.statements = [statement, if_]
        loop.statement = block

        #check that the loop condition is like an integer
        if expression.type_() not in ["int"]:
            self.tokens.error(
                "do while statement conditional must be an integer like expression")
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
        member_names = []
        member_declarations = []
        while self.tokens.peek() != "}":
            type_, size, signed, const = self.parse_type_specifier()
            name = self.tokens.get()

            member_names.append(name)
            member_declarations.append(self.parse_declaration(
                type_, 
                size, 
                signed, 
                const,
                name,
            ))

            self.tokens.expect(";")
        self.tokens.expect("}")
        return member_names, member_declarations

    def parse_typedef_struct(self):
        self.tokens.expect("typedef")
        self.tokens.expect("struct")
        declaration = StructDeclaration(*self.parse_struct_body())
        name = self.tokens.get()
        declaration._type= name
        self.tokens.expect(";")
        self.scope[name] = declaration
        self.structs.append(name)

    def parse_define_struct(self):
        self.tokens.expect("struct")
        name = self.tokens.get()
        declaration = StructDeclaration(*self.parse_struct_body())
        declaration._type="struct_"+str(id(declaration))
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

        """global_declaration := "{" 
            declaration 
            *["," declaration] 
            ";"
        """

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

        """compound_declaration := "{" 
            declaration 
            *["," declaration] 
            ";"
        """

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

    def parse_array_initializer(self, type_, size, signed):

        """array_initialiser := "{" 
             [array_initializer | variable_initializer] 
            *["," [array_initializer | variable_initializer]] "}"
        """

        self.tokens.expect("{")
        elements=[]
        while 1:
            if self.tokens.peek() == "{":
                elements.append(self.parse_array_initializer(type_, size, signed))
            else:
                elements.append(self.parse_variable_initializer(type_, size, signed))
            if self.tokens.peek() == "}": break
            self.tokens.expect(",")
        self.tokens.expect("}")
        return elements

    def parse_string_initializer(self, type_, size, signed):

        """string_initialiser := "\"" *[character] "\"" """

        if type_ != "int" or size != 4:
            self.tokens.error("unsuitable array type for string initializer")
        initializer = self.tokens.get()
        initializer = [Constant(ord(i)) for i in initializer.strip('"').decode("string_escape")]
        initializer += [Constant(0)]
        return initializer

    def parse_variable_initializer(self, type_, size, signed):

        """variable_initialiser := parse_ternary_expression"""

        initializer = self.parse_ternary_expression()
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

        return initializer


    def parse_declaration(self, type_, size, signed, const, name):

        """declaration := type_specifier name 
            *["[" ternary_expression "]"] 
            ?["=" 
                [string_initialiser | array_initialiser | variable_initialiser]
            ]
        """

        if type_ in self.structs:
            declaration = self.scope[type_]
        else:
            declaration = VariableDeclaration(
                name,
                type_,
                size,
                signed,
                const
            )

        #Gather dimensions of subarrays
        array_number_of_elements = []
        while self.tokens.peek() == "[":
            self.tokens.expect("[")
            if self.tokens.peek() != "]":
                size_expression = self.parse_ternary_expression()
                if size_expression.type_() != "int":
                    self.tokens.error("Array size must be an integer like expression")
                try:
                    array_number_of_elements.append(size_expression.value())
                except NotConstant:
                    self.tokens.error("Array size must be constant")
            else:
                array_number_of_elements.append(None)
            self.tokens.expect("]")

        array_number_of_elements.reverse()

        #Encapsulate elements in arrays, starting from the right most
        for number_of_elements in array_number_of_elements[:-1]:
            if number_of_elements is None:
                self.tokens.error("Inner array range must be specified")
            declaration = ArrayDeclaration(
                elements = number_of_elements,
                element_declaration = declaration,
            )
        for number_of_elements in array_number_of_elements[-1:]:
            declaration = ArrayDeclaration(
                elements = number_of_elements,
                element_declaration = declaration,
            )

        #Array Initialiser
        initializer = None
        if self.tokens.peek() == "=":
            self.tokens.expect("=")

            #initialize as a string
            if self.tokens.peek().startswith('"'):
                initializer = self.parse_string_initializer(type_, size, signed)

                #Not strictly correct initializastion behaviour
                if declaration.elements is None:
                    declaration.elements = len(initializer)
                elif declaration.elements != len(initializer):
                    self.tokens.error(
                        "Array initializer does not match array dimensions")

            elif self.tokens.peek() == "{":
                initializer = self.parse_array_initializer(type_, size, signed)

                #Not strictly correct initializastion behaviour
                if declaration.elements is None:
                    declaration.elements = len(initializer)
                elif declaration.elements != len(initializer):
                    self.tokens.error(
                        "Array initializer does not match array dimensions")

            else:
                initializer = self.parse_variable_initializer(type_, size, signed)

            declaration.initializer = initializer

        if hasattr(declaration, "elements") and declaration.elements is None:
            self.tokens.error(
                "Array size must be specified if not initialized")

        return declaration

    def parse_expression(self):

        """expression := assignment"""

        expression = self.parse_assignment()
        return expression

    def parse_ternary_expression(self):

        """ternary_expression := or_expression "?" or_expression ":" or_expression"""

        expression = constant_fold(self.parse_or_expression())
        while self.tokens.peek() in ["?"]:
            self.tokens.expect("?")
            true_expression = constant_fold(self.parse_or_expression())
            self.tokens.expect(":")
            false_expression = constant_fold(self.parse_or_expression())
            expression, true_expression = self.coerce_integer_types(
                    expression, 
                    true_expression
            )
            true_expression, false_expression = self.coerce_integer_types(
                    true_expression, 
                    false_expression
            )
            expression = OR(AND(expression, true_expression), false_expression)
        return expression

    def parse_or_expression(self):

        """or_expression := and_expression *["||" and_expression]"""

        expression = self.parse_and_expression()
        while self.tokens.peek() in ["||"]:
            self.tokens.expect("||")
            right = self.parse_and_expression()
            expression, right = self.coerce_integer_types(expression, right)
            expression = OR(expression, right)
        return expression

    def parse_and_expression(self):

        """and_expression := binary_expression *["&&" binary_expression]"""

        expression = self.parse_binary_expression(["|"])
        while self.tokens.peek() in ["&&"]:
            self.tokens.expect("&&")
            right = self.parse_binary_expression(["|"])
            expression, right = self.coerce_integer_types(expression, right)
            expression = AND(expression, right)
        return expression

    def substitute_function(self, binary_expression):

        """For some operations are more easily implemented in software.
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

        #Some things can't be implemented in verilog, substitute them with a
        #function
        if signature in functions:
            function = self.scope[functions[signature]]
            function_call = FunctionCall(function)
            self.function.called_functions.append(function)
            function_call.arguments = [
                    binary_expression.left, 
                    binary_expression.right
            ]
            return function_call
        else:
            return binary_expression

    def coerce_types(self, left, right):

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

        """Convert integer types in expressions."""

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

        """binary_expression := unary_expression operator *unary_expression"""

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

        elif self.tokens.peek() in ["++", "--"]:
            operator = self.tokens.get()
            expression = self.parse_unary_expression()
            expression = Assignment(
                expression,
                Binary(
                    operator[0],
                    expression,
                    Constant(
                        1, 
                        expression.type_(),
                        expression.size(), 
                        expression.signed()
                    ),
                ),
            )
            return expression

        elif self.tokens.peek() == "sizeof":
            self.tokens.get()
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

        """postfix_expression := primary_expreession *[
                function_call | 
                array_index | 
                struct_member | 
                ++ |
                --
            ]
        """

        expression = self.parse_primary_expression()

        while self.tokens.peek() in ["(", "[", ".", "++", "--"]:#, "->"]

            if self.tokens.peek() == "(":
                expression = self.parse_function_call(expression)
            elif self.tokens.peek() == "[":
                expression = self.parse_array_index(expression)
            elif self.tokens.peek() == ".":
                expression = self.parse_struct_member(expression)
            elif self.tokens.peek() in ["++", "--"]:
                operator = self.tokens.get()
                expression = MultiExpression(
                    expression,
                    [Assignment(
                        expression,
                        Binary(
                            operator[0],
                            expression,
                            Constant(
                                1, 
                                expression.type_(),
                                expression.size(), 
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
            else:
                if name not in self.scope:
                    self.tokens.error(
                        "%s is not declared in current scope"%name)
                instance = self.scope[name]
                if not hasattr(instance, "local"):
                    self.tokens.error(
                        "%s is not is not an instance in the current scope"%name)
                #store inside the current function any globals that get
                #referenced if a global isn't referenced it doesn't get
                #compiled
                if not instance.local:
                    self.function.referenced_globals.append(instance)
                expression = instance.reference()
        else:
            expression = self.parse_literal()

        return expression

    def parse_array_index(self, array):

        """parse an index into an array i.e. [] operation"""

        self.tokens.expect("[")
        index_expression = self.parse_expression()
        self.tokens.expect("]")
        if not array.type_().endswith("[]"):
            self.tokens.error(
                "Cannot index non-array type %s"%array.type_())
        if index_expression.type_() not in ["int"]:
            self.tokens.error(
                "Array indices must be an integer like expression")
        return ArrayIndex(array, index_expression)

    def parse_struct_member(self, struct):

        """parse a member of a struct i.e. . operation"""

        self.tokens.expect(".")

        is_a_struct = (
            struct.type_().startswith("struct") or 
            struct.type_() in self.structs
        )

        if not is_a_struct:
            self.tokens.error(
                "Cannot access member of non-struct type %s"%struct.type_())

        member = self.tokens.get()
        if member not in struct.declaration.member_names:
            self.tokens.error("%s is not a member of struct"%member)
        return StructMember(struct, member)

    def parse_file_read(self):

        """parse the built-in function file_read"""

        self.tokens.expect("(")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileRead(file_name)

    def parse_file_write(self):

        """parse the built-in function file_write"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(",")
        file_name = self.tokens.get()
        file_name = file_name.strip('"').decode("string_escape")
        self.tokens.expect(")")
        return FileWrite(file_name, expression)

    def parse_double_to_bits(self):

        """parse the built-in function double_to_bits"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return DoubleToBits(self.to_double(expression))

    def parse_float_to_bits(self):

        """parse the built-in function float_to_bits"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return FloatToBits(self.to_float(expression))

    def parse_bits_to_double(self):

        """parse the built-in function bits_to_float"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return BitsToDouble(self.to_long(expression))

    def parse_bits_to_float(self):

        """parse the built-in function bits_to_float"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(")")
        return BitsToFloat(self.to_int(expression))

    def parse_input(self):

        """parse the built-in function input"""

        self.tokens.expect("(")
        input_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(self.allocator.new_input(input_name))

    def parse_fgetc(self):

        """parse the built-in function fgetc"""

        self.tokens.expect("(")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Input(handle)

    def parse_ready(self):

        """parse the built-in function ready"""

        self.tokens.expect("(")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Ready(handle)

    def parse_output(self):

        """parse the built-in function output"""

        self.tokens.expect("(")
        output_name = self.tokens.get().strip('"').decode("string_escape")
        self.tokens.expect(")")
        return Constant(self.allocator.new_output(output_name))

    def parse_fputc(self):

        """parse the built-in function fputc"""

        self.tokens.expect("(")
        expression = self.parse_expression()
        self.tokens.expect(",")
        handle = self.parse_expression()
        self.tokens.expect(")")
        return Output(handle, expression)

    def parse_function_call(self, function):

        """parse a function call"""

        #Pass the function call
        #
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
            print dir(function_call)
            self.tokens.error(
                "not a function cannot be called")

        #Check that the correct number of arguments has been given
        #
        required_arguments = len(function_call.function.arguments)
        actual_arguments = len(function_call.arguments)
        if required_arguments != actual_arguments:
            self.tokens.error("Function %s takes %s arguments %s given."%(
                name,
                len(function_call.function.arguments),
                len(function_call.arguments)))

        #Check that each argument is of a suitable type for the function 
        #being called. Some numerical types may be promoted during function
        #calls
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
                elif required.type_().endswith("[]") and required.element_declaration.size() != actual.element_declaration.size():
                    self.tokens.error(
                        "element size mismatch in function argument expected: %s actual: %s"%(
                            required.element_size(),
                            actual.element_size()))

            corrected_arguments.append(actual)
        function_call.arguments = corrected_arguments

        return function_call

    def parse_literal(self):

        """parse a literal"""

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

        """parse a character literal"""

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

        """parse a string literal"""

        type_ = "int"
        size = 4
        signed = True
        try:
            initializer = [Constant(ord(i)) for i in token.strip('"').decode("string_escape")] 
            initializer += [Constant(0)]
            initialize_memory = self.initialize_memory
            declaration = ArrayDeclaration(
                elements = len(initializer),
                element_declaration = VariableDeclaration(None, "int", 4, False, True),
            )
            declaration.initializer = initializer
            instance = declaration.instance(self.function)
            #since we don't return instance, it doesn't get generated.
            #treat as a global
            instance.local = False
            self.function.referenced_globals.append(instance)
            return instance.reference()
        except SyntaxError:
            self.tokens.error("%s is not a character literal"%token)

    def parse_floating_point_literal(self, token): 

        """parse a floating point literal"""

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

        """parse an integer literal"""

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

    def to_double(self, expression):

        """Convert (any type which can be converted) to a double"""

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

        """Convert (any type which can be converted) to a float"""

        if is_double(expression):
            return DoubleToFloat(expression)
        elif is_float(expression):
            return expression
        elif is_long(expression):
            return DoubleToFloat(LongToDouble(expression))
        elif is_int(expression):
            return IntToFloat(expression)
        else:
            self.tokens.error(
                "cannot convert expression with type %s to float"%expression.type_())

    def to_long(self, expression):

        """Convert (any type which can be converted) to a long"""

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

        """Convert (any type which can be converted) to an int"""

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

    def binary(self, operator, left, right):

        """Create a Binary Expression object

        Coerce numeric types following standard promotion rules.
        Where a binary opertion is implemented in software substitute a function call.
        """

        left, right = self.coerce_types(left, right)
        expression = Binary(operator, left, right)
        expression = self.substitute_function(expression)
        return expression


def compatible(left, right):

    """ Comare expected and actual type and size in function arguments """

    return left.type_() == right.type_() and left.size() == right.size()

def is_double(expression):

    """ Expression object is of type float and 8 bytes long """

    return expression.size() == 8 and expression.type_() == "float"

def is_float(expression):

    """ Expression object is of type float and 4 bytes long """

    return expression.size() == 4 and expression.type_() == "float"

def is_long(expression):

    """ Expression object is of type int and 8 bytes long """

    return expression.size() == 8 and expression.type_() == "int"

def is_int(expression):

    """ Expression object is of type int and 4 bytes long """

    return expression.size() == 4 and expression.type_() == "int"


