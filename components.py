components = (
	("Sources", 
        (
            {
                "name": "Repeat Value", 
                "input_ports" : [], 
                "output_ports" : ["z"],           
                "parameters" : {"value":1}, 
                "function" : "Repeater"
            },
            {
                "name": "Input Port",   
                "input_ports" : [], 
                "output_ports" : ["z"],           
                "parameters" : {"name":"input", "bits":8}, 
                "function" : "InPort"
            },
            {
                "name": "Serial Input", 
                "input_ports" : [], 
                "output_ports" : ["serial data"], 
                "parameters" : {"name":"RX", "clock_speed":50000000, "baud_rate":115200}, 
                "function" : "SerialIn"
            },
        ),
    ),
	("Sinks" , 
       (
           {
               "name": "Output Port",   
               "input_ports" : ["a"],            
               "output_ports" : [], 
               "parameters" : {"name":"out"}, 
               "function" : "OutPort"
           },
           {
               "name": "Serial Output", 
               "input_ports" : ["serial data"],  
               "output_ports" : [], 
                "parameters" : {"name":"TX", "clock_speed":50000000, "baud_rate":115200}, 
               "function" : "SerialOut"
           },
           {
                "name": "Console",       
                "input_ports" : ["console data"], 
                "output_ports" : [], 
                "parameters" : {}, 
                "function" : "Console"
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
