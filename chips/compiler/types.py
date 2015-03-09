"""Classes to represent C types, and functions to query and manipulate them"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2012, Jonathan P Dawson"
__version__ = "0.1"

def is_double(expression):

    """ Expression object is of type double """

    return expression.type_() == "double"

def is_float(expression):

    """ Expression object is of type float """

    return expression.type_() == "float"

def is_long(expression):

    """ Expression object is of type long """

    return expression.type_() == "long"

def is_int(expression):

    """ Expression object is of type int """

    return expression.type_() == "int"

class ArrayOf():

    """ Class to represent Arrays of types """
    
    def __init__(self, type_, dimensions=[]):
        self.type_ = type_
        self.dimensions = dimensions
        self.is_array_of = True

    def base_type(self):
        if len(self.dimensions) > 1:
            return ArrayOf(self.type_, self.dimensions[:-1])
        else:
            return self.type_

    def root_type(self):
        return self.type_

    def __eq__(self, other):
        if hasattr(other, "is_array_of"):
            if self.type_ == other.type_:
                if self.dimensions[:-1] == other.dimensions[:-1]:
                    if None in [self.dimensions[-1], self.dimensions[-1]]:
                        return True
                    if self.dimensions[-1] == self.dimensions[-1]:
                        return True
        if hasattr(other, "is_pointer_to"):
            if self.type_ == other.type_:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        string = repr(self.type_)
        for i in self.dimensions:
            string += "[%s]"%i
        return string


    def _size_(self):
        size = type_size(self.type_)
        for i in self.dimensions:
            size *= i
        return size

    def _arg_size_(self):
        return 4

def is_array_of(thing):

    """ Is thing an Array? """

    return hasattr(thing.type_(), "is_array_of")

class PointerTo():

    """ Class to represent pointers to types """
    
    def __init__(self, type_):
        self.type_ = type_
        self.is_pointer_to = True

    def base_type(self):
        return self.type_

    def __eq__(self, other):
        if hasattr(other, "is_pointer_to"):
            if self.type_ == other.type_:
                return True
        if hasattr(other, "is_array_of"):
            if self.type_ == other.type_:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        string = repr(self.type_)
        string += "*"
        return string

    def _size_(self):
        return 4

    def _arg_size_(self):
        return 4

def is_pointer_to(thing):

    """ Is thing a Pointer? """

    return hasattr(thing.type_(), "is_pointer_to")

class StructOf():

    """ Class to represent structs of types """

    def __init__(self, names, types):
        self.names = names
        self.types = types
        self.is_struct_of = True

    def __eq__(self, other):
        if hasattr(other, "is_struct_of"):
            if self.types == other.types:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        string = "struct {"
        for i in self.types:
            string += repr(i) + ";"
        string += "}"
        return string

    def member_type(self, name):
        return self.types[self.names.index(name)]

    def member_offset(self, member):
        offset = 0
        for name, type_ in zip(self.names, self.types):
            if name == member:
                break
            offset += type_size(type_)//4
        return offset

    def _size_(self):
        size = 0
        for i in self.types:
            size += type_size(i)
        return size

    def _arg_size_(self):
        return self._size_()

def is_struct_of(thing):

    """ Is thing a Struct? """

    return hasattr(thing.type_(), "is_struct_of")

def type_size(type_):

    """ Given a type object, return the size """

    if type_ in ["void"]:
        return 0
    if type_ in ["int", "float"]:
        return 4
    if type_ in ["long", "double"]:
        return 8
    return type_._size_()

def type_arg_size(type_):

    """ Given a type object, return the size """

    if type_ in ["void"]:
        return 0
    if type_ in ["int", "float"]:
        return 4
    if type_ in ["long", "double"]:
        return 8

    return type_._arg_size_()

def size_of(thing):

    """ Given on object that supports the "type_" method return the size """

    type_ = thing.type_()
    return type_size(type_)

def arg_size_of(thing):

    """ Given on object that supports the "type_" method return the size """

    type_ = thing.type_()
    return type_arg_size(type_)

