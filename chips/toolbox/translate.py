import sys

input_file = open(sys.argv[1]).read()
input_file = " ".join(input_file.splitlines())
for operator in [")", "(", ";", "=", "<", ":", "+", "-", "/", "*", "."]:
    input_file = (" %s "%operator).join(input_file.split(operator))

input_file = input_file.split()
print input_file
module = {
        "inputs" : [],
        "outputs" : [],
        "parameters" : [],
        
}


def parse_file():
    while input_file[0] != "entity":
        input_file.pop(0)
    parse_entity()

def parse_entity():
    assert input_file[0] == "entity"
    input_file.pop(0)
    module["name"] = input_file[0]
    input_file.pop(0)
    assert input_file[0] == "is"
    input_file.pop(0)
    if input_file[0] == "generic":
        input_file.pop(0)
        assert input_file[0] == "("
        input_file.pop(0)
        while input_file[0] != ")":
            parse_generic()
        assert input_file[0] == ")"
        input_file.pop(0)
        assert input_file[0] == ";"
        input_file.pop(0)
    if input_file[0] == "port":
        input_file.pop(0)
        assert input_file[0] == "("
        input_file.pop(0)
        while input_file[0] != ")":
            parse_port()
        assert input_file[0] == ")"
        input_file.pop(0)
        assert input_file[0] == ";"
        input_file.pop(0)

def parse_generic():
    name = input_file.pop(0)
    assert input_file.pop(0) == ":"
    type_ = input_file.pop(0)
    module["parameters"].append((name, type_))
    if input_file[0] == ";":
        assert input_file.pop(0) == ";"

def parse_port():
    name = input_file.pop(0)
    assert input_file.pop(0) == ":"
    mode = input_file.pop(0)
    type_ = input_file.pop(0)
    if type_ == "std_logic":
        bits = 1
    elif type_ == "std_logic_vector":
        assert input_file.pop(0) == "("
        msb = ""
        while input_file[0] != "downto":
          msb += input_file.pop(0)
        assert input_file.pop(0) == "downto"
        lsb = ""
        while input_file[0] != ")":
          lsb += input_file.pop(0)
        lsb = input_file.pop(0)
        assert input_file.pop(0) == ")"
    if input_file[0] == ";":
        assert input_file.pop(0) == ";"
    if mode == "in":
        module["inputs"].append((name, type_))
    else:
        module["outputs"].append((name, type_))

parse_file()
print module
