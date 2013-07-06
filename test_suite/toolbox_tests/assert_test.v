//name: assert_test
//source_file: assert_test.sch
//dependency: constant_value
//dependency: asserter
`timescale 1ns/1ps
module assert_test (
    
);



  wire [15 : 0] signal_0;
  wire signal_0_stb;
  wire signal_0_ack;

  reg clk;
  reg rst;
  
initial
  begin
    rst <= 1'b1;
    #50 rst <= 1'b0;
  end

  
initial
  begin
    clk <= 1'b0;
    while (1) begin
      #5 clk <= ~clk;
    end
  end

  constant_value #(
    .bits (16),
    .value (0)
  )
 constant_value_inst_1
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_0),
    .out1_stb (signal_0_stb),
    .out1_ack (signal_0_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_0
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_0),
    .in1_stb (signal_0_stb),
    .in1_ack (signal_0_ack)
  );

endmodule
