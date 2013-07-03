//name: bend
//tag: schematic
//output: out1 : bits
//input: in1 : bits
//parameter : bits : 16
//source_file: built_in

module bend #(parameter bits=16)(
  input clk,
  input rst,
  input [bits-1:0] in1,
  input in1_stb,
  output in1_ack,
  output [bits-1:0] out1,
  output out1_stb,
  output out1_ack
);
  assign out1 = in1;
  assign out1_stb = in1_stb;
  assign in1_ack = out1_ack;
endmodule
