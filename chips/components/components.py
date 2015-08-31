from chips.api.api import Chip, Component, Wire

def async(chip, a):
    async = Component(
    """void asynch(){
        int in = input("in");
        int out = output("out");
        int data;
        while(1){
            if(ready(in)){
                data = fgetc(in);
            }
            if(ready(out)){
                fputc(data, out);
            }
        }
    }""",
    inline=True)
    wire = Wire(chip)
    async(
            chip,
            inputs = {"in":a},
            outputs = {"out":wire},
            parameters = {}
    )
    return wire

def constant(chip, value, type_="int"):
    constant_component = Component("""
    #include <stdio.h>
    int out = output("out");
    void constant(){
        while(1){
            fput_%s(%s, out);
        }
    }"""%(type_, value), inline=True)
    wire = Wire(chip)
    constant_component(
            chip,
            inputs = {},
            outputs = {"out":wire},
            parameters = {},
    )
    return wire

def cycle(chip, args=[], type_="int"):
    cycle_component = Component("""
    #include <stdio.h>
    int out = output("out");
    void cycle(){
        %s list[%i] = {%s};
        int i;
        %s data;
        while(1){
          for(i=0; i<%i; i++){
              data = list[i];
              fput_%s(data, out);
          }
        }
    }"""%(
        type_, 
        len(args),
        ", ".join(["%s"%i for i in args]),
        type_,
        len(args),
        type_), inline=True)
    wire = Wire(chip)
    cycle_component(
            chip,
            inputs = {},
            outputs = {"out":wire},
            parameters = {},
    )
    return wire

def report_all(chip, stream, type_="int"):
    report_all_component = Component("""
    #include <stdio.h>
    int in = input("in");
    void report_all(){
        while(1){
            report(fget_%s(in));
        }
    }"""%type_, inline=True)

    report_all_component(
            chip,
            inputs = {"in":stream},
            outputs = {},
            parameters = {},
    )

def tee(chip, a):
    tee_component = Component("""
        int out1 = output("out1");
        int out2 = output("out2");
        int in = input("in");
        void tee(){
            int data;
            while(1){
                data = fgetc(in);
                fputc(data, out1);
                fputc(data, out2);
            }
        }""", inline=True)
    wire1 = Wire(chip)
    wire2 = Wire(chip)
    tee_component(
            chip,
            inputs = {"in":a},
            outputs = {"out1":wire1, "out2":wire2},
            parameters = {}
    )
    return wire1, wire2

def delay(chip, a, initial = 0, type_="int"):
    delay_component = Component("""
        #include <stdio.h>
        int out = output("out");
        int in = input("in");
        void delay(){
            fput_%s(INITIAL, out);
            while(1){
                fput_%s(fget_%s(in), out);
            }
        }"""%(type_, type_, type_), inline=True)
    wire = Wire(chip)
    delay_component(
            chip,
            inputs = {"in":a},
            outputs = {"out":wire},
            parameters = {"INITIAL":initial}
    )
    return wire

def _arithmetic(chip, a, b, operation, type_="int"):
    arithmetic_component = Component("""
        #include <stdio.h>
        int out = output("out");
        int in = input("in1");
        int in = input("in2");
        void delay(){
            while(1){
                fput_%s(fget_%s(in1) %s fget_%s(in2), out);
            }
        }"""%(type_, type_, operation, type_), inline=True)
    wire = Wire(chip)
    arithmetic_component(
            chip,
            inputs = {"in1":a, "in2":b},
            outputs = {"out":wire},
            parameters = {}
    )
    return wire

def add(chip, a, b, type_="int"):
    return _arithmetic(chip, a, b, "+", type_="int")

def sub(chip, a, b, type_="int"):
    return _arithmetic(chip, a, b, "-", type_="int")

def mul(chip, a, b, type_="int"):
    return _arithmetic(chip, a, b, "*", type_="int")

def div(chip, a, b, type_="int"):
    return _arithmetic(chip, a, b, "/", type_="int")

def _comparison(chip, a, b, operation, type_="int"):
    comparison = Component("""
        #include <stdio.h>
        int out = output("out");
        int in = input("in1");
        int in = input("in2");
        void delay(){
            while(1){
                fput_int(fget_%s(in1) %s fget_%s(in2), out);
            }
        }"""%(type_, operation, type_), inline=True)
    wire = Wire(chip)
    comparison(
            chip,
            inputs = {"in1":a, "in2":b},
            outputs = {"out":wire},
            parameters = {}
    )
    return wire

def eq(chip, a, b, type_="int"):
    return _comparison(chip, a, b, "==", type_="int")

def ne(chip, a, b, type_="int"):
    return _comparison(chip, a, b, "!=", type_="int")

def lt(chip, a, b, type_="int"):
    return _comparison(chip, a, b, "<", type_="int")

def le(chip, a, b, type_="int"):
    return _comparison(chip, a, b, "<=", type_="int")

def gt(chip, a, b, type_="int"):
    return _comparison(chip, a, b, ">", type_="int")

def ge(chip, a, b, type_="int"):
    return _comparison(chip, a, b, ">=", type_="int")

def arbiter(chip, *args):

    """ Merge many streams of data into a single stream giving each stream equal priority

    arguments
    ---------

    chip - the chip
    args - streams of data to combine
    
    returns
    -------

    stream - a stream of data

    """

    arbiter_component = Component("""
        int out = output("out");
        int in1 = input("in1");
        int in2 = input("in2");
        void main(){
            int data;
            while(1){
                if(ready(in1), fputc(fgetc(in1), out);
                if(ready(in2), fputc(fgetc(in2), out);
            }
        }""", 
    inline=True)

    def tree_reduce(function, *args):
        arg_list = list(args)
        if len(arg_list) <= 1:
            return arg_list
        else:
            new_arg_list = []
            while len(arg_list) >= 2:
                new_arg_list.append(function(arg_list.pop(0), arg_list.pop(0)))
            if arg_list:
                new_arg_list.append(arg_list.pop(0))
            return tree_reduce(function, *new_arg_list)

    def combine(a, b):
        wire = Wire(chip)
        arbiter_component(
            chip,
            inputs = {"in1":a, "in2":b},
            outputs = {"out":wire},
            parameters = {}
        )
        return wire

    return tree_reduce(combine, *args)

def discard(chip, a):

    """Discard a stream of data.

    arguments
    ---------

    chip - the chip
    a - the stream of data to discard
    
    returns
    -------

    N/A

    """

    discard_component = Component("""
        int out1 = output("out1");
        int out2 = output("out2");
        int in = input("in");
        void main(){
            int data;
            while(1){
                data = fgetc(in);
                fputc(data, out);
                fputc(data, out1);
            }
        }""", inline=True)

    discard_component(
            chip,
            inputs = {"in":a},
            outputs = {},
            parameters = {}
    )

if __name__ == "__main__":
    from chips.api.gui import GuiChip

    mychip = GuiChip("blah")
    report_all(mychip, async(mychip, cycle(mychip, [0, 1, 2, 3, 4])))
    mychip.debug()

