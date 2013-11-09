__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

from chips.compiler.exceptions import C2CHIPError

operators = [
  "!", "~", "+", "-", "*", "/", "//", "%", "=", "==", "<", ">", "<=", ">=",
  "!=", "|", "&", "^", "||", "&&", "(", ")", "{", "}", "[", "]", ";", "<<", 
  ">>", ",", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "<<=", ">>=", "++", 
  "--", "?", ":", "."
]

class Tokens:

    """Break the input file into a stream of tokens, 
    provide functions to traverse the stream."""

    def __init__(self, filename):
       self.tokens = []
       self.filename = None
       self.lineno = None
       self.scan(filename)

    def scan(self, filename):
  
        """Convert the test file into tokens"""
        self.filename = filename
    
        try:
            input_file = open(self.filename)        
        except IOError:
            raise C2CHIPError("Cannot open file: "+self.filename)
    
    
        token = []
        tokens = []
        self.lineno = 1
        for line in input_file:
    
            #include files
            line = line+" "
            if line.strip().startswith("#include"):
                filename = self.filename
                lineno = self.lineno
                self.tokens.extend(tokens)
                self.filename = line.strip().replace("#include", "").strip(' ><"')
                self.scan(self.filename)
                self.lineno = lineno
                self.filename = filename
                tokens = []
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
                        tokens.append((self.filename, self.lineno, token))
                        token = char
    
                #number
                elif token[0].isdigit():
                    if char.isdigit() or char.upper() in ".XABCDEF":
                        token += char
                    else:
                        tokens.append((self.filename, self.lineno, token))
                        token = char

                #string literal
                elif token.startswith('"'):
                    if char == '"':
                        token += char
                        tokens.append((self.filename, self.lineno, token))
                        token = ""
                    else:
                        token += char

                #character literal
                elif token.startswith("'"):
                    if char == "'":
                        token += char
                        tokens.append((self.filename, self.lineno, token))
                        token = ""
                    else:
                        token += char
    
                #operator
                elif token in operators:
                    if token + char in operators:
                        token += char
                    else:
                        tokens.append((self.filename, self.lineno, token))
                        token = char
    
                else:
                    token = char
  
                newline = False
            self.lineno += 1
  
        self.tokens.extend(tokens)

    def error(self, string):
  
        """Generate an error message (including the filename and line number)"""
  
        raise C2CHIPError(string + "\n", self.filename, self.lineno)
  
    def peek(self):
  
        """Return the next token in the stream, but don't consume it"""
  
        if self.tokens:
            return self.tokens[0][2]
        else:
            return ""
  
    def get(self):
  
        """Return the next token in the stream, and consume it"""
  
        if self.tokens:
            self.lineno = self.tokens[0][1]
            self.filename = self.tokens[0][0]
        filename, lineno, token = self.tokens.pop(0)
        return token
  
    def end(self):
  
        """Return True if all the tokens have been consumed"""
  
        return not self.tokens
  
    def expect(self, expected):
  
        """Consume the next token in the stream, 
        generate an error if it is not as expected."""
  
        filename, lineno, actual = self.tokens.pop(0)
        if self.tokens:
            self.lineno = self.tokens[0][1]
            self.filename = self.tokens[0][0]
        if actual == expected:
            return
        else:
            self.error("Expected: %s, got: %s"%(expected, actual))
