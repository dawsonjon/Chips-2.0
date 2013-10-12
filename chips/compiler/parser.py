__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

from parse_tree import *
from tokens import Tokens
from allocator import Allocator

class Parser:

    """Turn the C input file into a tree of expressions and statements."""

    def __init__(self, input_file, reuse, initialize_memory):
        self.scope = {}
        self.function = None
        self.loop = None
        self.tokens = Tokens(input_file)
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
        return process

    def parse_function(self):
        function = Function()
        function.allocator = self.allocator
        stored_scope = self.scope
        type_ = self.tokens.get()
        name = self.tokens.get()
        
        #check if it is a global declaration
        if self.tokens.peek() != "(":
            if type_ not in ["int", "short", "long", "char"] + self.structs:
                self.tokens.error("unknown type")
            return self.parse_global_declaration(type_, name)

        #otherwise continue parsing a function
        self.tokens.expect("(")
        function.name = name
        function.type_ = type_
        function.return_address = self.allocator.new(function.name+" return address")
        if type_ not in ["int", "short", "long", "char", "void"]:
            self.tokens.error("unknown type")
        if type_ != "void":
            function.return_value = self.allocator.new(function.name+" return value")
        function.arguments = []
        while self.tokens.peek() != ")":
            type_ = self.tokens.get()
            if type_ not in ["int", "short", "long", "char"]:
                self.tokens.error("unknown type")
            argument = self.tokens.get()
            if self.tokens.peek() == "[":
                self.tokens.expect("[")
                self.tokens.expect("]")
                type_+="[]"
            function.arguments.append(Argument(argument, type_, self))
            if self.tokens.peek() == ",":
                self.tokens.expect(",")
            else:
                break
        self.tokens.expect(")")
        self.function = function
        function.statement = self.parse_statement()
        if type_ != "void" and not hasattr(function, "return_statement"):
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
        if hasattr(self.function, "return_value"):
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
        assignment_operators = [
            "=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "<<=", ">>=", 
            "++", "--"
        ]
        lvalue = self.parse_ternary_expression()
        if self.tokens.peek() in assignment_operators:
            if not hasattr(lvalue, "declaration"):
                self.tokens.error(
                    "left hand operand of assignment is not modifiable"
                )
            operator = self.tokens.get()
            if operator == "=":
                expression = self.parse_ternary_expression()
            elif operator in ["++", "--"]:
                expression = Binary(
                    operator[:-1],
                    lvalue, 
                    Constant(1), 
                    self.allocator
                )
            else:
                expression = Binary(
                    operator[:-1], 
                    lvalue, 
                    self.parse_ternary_expression(), 
                    self.allocator
                )
            if not compatible(lvalue.type_, expression.type_):
                self.tokens.error(
                    "type mismatch in assignment"
                )
            return Assignment(lvalue, expression, self.allocator)
        else:
            return lvalue

    def parse_if(self):
        if_ = If()
        if_.allocator = self.allocator
        self.tokens.expect("if")
        self.tokens.expect("(")
        if_.expression = self.parse_expression()
        if if_.expression.type_ not in ["int", "short", "long", "char"]:
            self.tokens.error(
                "if statement conditional must be an integer like expression"
            )
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
        if expression.type_ not in ["int", "short", "long", "char"]:
            self.tokens.error(
                "switch statement expression must be an integer like expression"
            )
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
        if expression.type_ not in ["int", "short", "long", "char"]:
            self.tokens.error(
                "case expression must be an integer like expression"
            )
        self.tokens.expect(":")
        try:
            expression = value(expression)
            case = Case()
            self.loop.cases[expression] =    case
        except NotConstant:
            self.tokens.error("case expression must be constant")
        except AttributeError:
            self.tokens.error(
                "case statements may only be use inside a switch statment"
            )
        return case

    def parse_default(self):
        self.tokens.expect("default")
        self.tokens.expect(":")
        default = Default()
        if not hasattr(self.loop, "cases"):
            self.tokens.error(
                "default statements may only be used inside a switch statment"
            )
        if hasattr(self.loop, "default"):
            self.tokens.error(
                "A switch statement may only have one default statement"
            )
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
        if expression.type_ not in ["int", "short", "long", "char"]:
            self.tokens.error(
                "if statement conditional must be an integer like expression"
            )
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
            if for_.expression.type_ not in ["int", "short", "long", "char"]:
                self.tokens.error(
                    "for statement conditional must be an integer like expression"
                )
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

    def parse_global_declaration(self, type_, name):
        instances = []
        while True:
            instance = self.parse_declaration(type_, name).instance()
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
            name = None
        self.tokens.expect(";")
        return CompoundDeclaration(instances)

    def parse_declaration(self, type_, name):
        #struct declaration
        if type_ in self.structs:
            declaration = self.scope[type_]
        elif type_ in ["int", "short", "long", "char"]:
            #array declaration 
            if self.tokens.peek() == "[":
                size = None
                self.tokens.expect("[")
                if self.tokens.peek() != "]":
                    size = self.tokens.get()
                self.tokens.expect("]")
                initializer = None
                if self.tokens.peek() == "=":
                    self.tokens.expect("=")
                    initializer = self.tokens.get()
                    initializer = [ord(i) for i in initializer.strip('"')] + [0]
                    size = len(initializer)
                if size is None:
                    self.tokens.error("array size must be specified if not initialized")
                type_+="[]"
                initialize_memory = self.initialize_memory
                declaration = ArrayDeclaration(self.allocator, size, type_, initializer, self.initialize_memory)

            #simple variable declaration 
            else:
                if self.tokens.peek() == "=":
                    self.tokens.expect("=")
                    initializer = self.parse_ternary_expression()
                else:
                    initializer = Constant(0)
                declaration = VariableDeclaration(
                    self.allocator, 
                    initializer, 
                    name,
                    type_
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
                expression = Binary(
                    self.tokens.get(), 
                    expression, 
                    self.parse_unary_expression(), 
                    self.allocator
                )
            return expression
        else:
            next_operators = operator_precedence[operators[0]]
            expression = self.parse_binary_expression(next_operators)
            while self.tokens.peek() in operators:
                expression = Binary(
                    self.tokens.get(), 
                    expression, 
                    self.parse_binary_expression(next_operators), 
                    self.allocator
                )
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
        function_call.type_ = function_call.function.type_
        required_arguments = len(function_call.function.arguments)
        actual_arguments = len(function_call.arguments)
        if required_arguments != actual_arguments:
            self.tokens.error("Function %s takes %s arguments %s given."%(
                name,
                len(function_call.function.arguments),
                len(function_call.arguments)
            ))
        required_arguments = function_call.function.arguments
        actual_arguments = function_call.arguments
        for required, actual in zip(required_arguments, actual_arguments):
            if required.type_ != actual.type_:
                self.tokens.error("Type mismatch expected type : %s got: %s."%(
                    required.type_,
                    actual.type_
                ))


        return function_call

    def parse_number(self):
        token = self.tokens.get()
        if token.startswith("'"):
            try:
                token = eval(token)
                value = ord(token)
            except SyntaxError:
                self.tokens.error("%s is not a character literal"%token)
        elif token.startswith('"'):
            try:
                initializer = [ord(i) for i in token.strip('"')] + [0]
                size = len(initializer)
                initialize_memory = self.initialize_memory
                declaration = ArrayDeclaration(self.allocator, size, "char[]", initializer, self.initialize_memory)
                return declaration.instance()
            except SyntaxError:
                self.tokens.error("%s is not a character literal"%token)
        else:
            try:
                value = int(eval(token))
            except SyntaxError:
                self.tokens.error("%s is not an integer literal"%token)
        return Constant(value)

    def parse_variable(self, name):
        if name not in self.scope:
            self.tokens.error("Unknown variable: %s"%name)
        instance = self.scope[name]
        return self.parse_variable_array_struct(instance)
 
    def parse_variable_array_struct(self, instance):
        if instance.type_ in ["int", "short", "long", "char"]:
            return Variable(instance, self.allocator)
        elif instance.type_.endswith("[]"):
            if self.tokens.peek() == "[":
                self.tokens.expect("[")
                index_expression = self.parse_expression()
                self.tokens.expect("]")
                if index_expression.type_ not in ["int", "short", "long", "char"]:
                    self.tokens.error(
                        "array indices must be an integer like expression"
                    )
                return ArrayIndex(instance, index_expression, self.allocator)
            else:
                return Array(instance, self.allocator)
        elif instance.type_ == "struct":
            self.tokens.expect(".")
            member = self.tokens.get()
            instance = instance.members[member]
            return self.parse_variable_array_struct(instance)

def compatible(left, right):
    if left == right:
        return True
    if left in ["int", "short", "long", "char"] and right in ["int", "short", "long", "char"]:
        return True
    return False

