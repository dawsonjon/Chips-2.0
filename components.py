components = (
	("Sources", 
        (
            {
                "name": "Repeat Value", 
                "input_ports" : [], 
                "output_ports" : ["out"],           
                "parameters" : {"value":1}, 
                "function" : "Repeater"
            },
            {
                "name": "Input Port",   
                "input_ports" : [], 
                "output_ports" : ["out"],           
                "parameters" : {"name":"input", "bits":8}, 
                "function" : "InPort"
            },
            {
                "name": "Serial Input", 
                "input_ports" : [], 
                "output_ports" : ["out"], 
                "parameters" : {"name":"RX", "clock_speed":50000000, "baud_rate":115200}, 
                "function" : "SerialIn"
            },
            {
                "name": "Counter", 
                "input_ports" : [], 
                "output_ports" : ["out"], 
                "parameters" : {"start":0, "stop":10, "step":1}, 
                "function" : "Counter"
            },
            {
                "name": "Sequence", 
                "input_ports" : [], 
                "output_ports" : ["out"], 
                "parameters" : {"items":(0,)}, 
                "function" : "Sequence"
            },
            {
                "name": "Stimulus", 
                "input_ports" : [], 
                "output_ports" : ["out"], 
                "parameters" : {"bits":8}, 
                "function" : "Stimulus"
            },
        ),
    ),
	("Sinks" , 
       (
           {
               "name": "Asserter",   
               "input_ports" : ["in"],            
               "output_ports" : [], 
               "parameters" : {}, 
               "function" : "Asserter"
           },
           {
                "name": "Console",       
                "input_ports" : ["in"], 
                "output_ports" : [], 
                "parameters" : {}, 
                "function" : "Console"
           },
           {
               "name": "Output Port",   
               "input_ports" : ["in"],            
               "output_ports" : [], 
               "parameters" : {"name":"out"}, 
               "function" : "OutPort"
           },
           {
               "name": "Response", 
               "input_ports" : ["in"],  
               "output_ports" : [], 
                "parameters" : {}, 
               "function" : "Response"
           },
           {
               "name": "Serial Output", 
               "input_ports" : ["in"],  
               "output_ports" : [], 
                "parameters" : {"name":"TX", "clock_speed":50000000, "baud_rate":115200}, 
               "function" : "SerialOut"
           },
       ),
    ),
	("Utilities" , 
       (
           {
               "name": "Decoupler",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Decoupler"
           },
           {
               "name": "HexPrinter",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "HexPrinter"
           },
           {
               "name": "Printer",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Printer"
           },
           {
               "name": "Resizer",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {"bits":8}, 
               "function" : "Resizer"
           },
           {
               "name": "Scanner",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {"bits":8}, 
               "function" : "Scanner"
           },
       ),
    ),
	("Arithmetic", 
       (
           {
               "name": "Multiplier",   
               "input_ports" : ["a", "b"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Mul"
           },
           {
                "name": "Divider",       
                "input_ports" : ["a", "b"], 
                "output_ports" : ["out"], 
                "parameters" : {}, 
                "function" : "Div"
           },
           {
               "name": "Adder",   
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Add"
           },
           {
               "name": "Subtractor", 
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Sub"
           },
       ),
    ),
	("Bitwise Logic", 
       (
           {
               "name": "AND",   
               "input_ports" : ["a", "b"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "AND"
           },
           {
                "name": "OR",       
                "input_ports" : ["a", "b"], 
                "output_ports" : ["out"], 
                "parameters" : {}, 
                "function" : "OR"
           },
           {
               "name": "XOR",   
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "XOR"
           },
           {
               "name": "NOT", 
               "input_ports" : ["in"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "NOT"
           },
       ),
    ),
	("Comparisons", 
       (
           {
               "name": "Equal",   
               "input_ports" : ["a", "b"],            
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Eq"
           },
           {
                "name": "Not Equal",       
                "input_ports" : ["a", "b"], 
                "output_ports" : ["out"], 
                "parameters" : {}, 
                "function" : "Ne"
           },
           {
               "name": "Less Than",   
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Lt"
           },
           {
               "name": "Greater Than", 
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Gt"
           },
           {
               "name": "Less Than or Equal",   
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Le"
           },
           {
               "name": "Greater Than or Equal", 
               "input_ports" : ["a", "b"], 
               "output_ports" : ["out"], 
               "parameters" : {}, 
               "function" : "Ge"
           },
       ),
    ),
	("Memory" , 
       (
           {
               "name": "Array",   
               "input_ports" : ["address_in", "data_in", "address_out"],            
               "output_ports" : ["data_out"], 
               "parameters" : {"depth":1024}, 
               "function" : "Array"
           },
           {
               "name": "Lookup",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {"items":(0,)}, 
               "function" : "Lookup"
           },
           {
               "name": "Fifo",   
               "input_ports" : ["in"],            
               "output_ports" : ["out"], 
               "parameters" : {"depth":1024}, 
               "function" : "Fifo"
           },
       ),
    ),
)
Tee  = {
    "name": "Tee",
    "input_ports" : ["in"],
    "output_ports" : ["out1", "out2"],
    "parameters" : {},
    "function" : "Tee"
}
Bend = {
    "name": "Bend",
    "input_ports" : ["in"],
    "output_ports" : ["out"],
    "parameters" : {},
    "function" : "Bend"
}
