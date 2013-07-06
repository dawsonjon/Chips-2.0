//name: comparison_test
//source_file: comparison_test.sch
//dependency: constant_value
//dependency: asserter
//dependency: less_than
//dependency: not_equal
//dependency: greater_than
//dependency: equal
//dependency: greater_than_or_equal
`timescale 1ns/1ps
module comparison_test (
    
);



  wire [15 : 0] signal_0;
  wire signal_0_stb;
  wire signal_0_ack;
  wire [15 : 0] signal_1;
  wire signal_1_stb;
  wire signal_1_ack;
  wire [15 : 0] signal_2;
  wire signal_2_stb;
  wire signal_2_ack;
  wire [15 : 0] signal_3;
  wire signal_3_stb;
  wire signal_3_ack;
  wire [15 : 0] signal_4;
  wire signal_4_stb;
  wire signal_4_ack;
  wire [15 : 0] signal_5;
  wire signal_5_stb;
  wire signal_5_ack;
  wire [15 : 0] signal_6;
  wire signal_6_stb;
  wire signal_6_ack;
  wire [15 : 0] signal_7;
  wire signal_7_stb;
  wire signal_7_ack;
  wire [15 : 0] signal_8;
  wire signal_8_stb;
  wire signal_8_ack;
  wire [15 : 0] signal_9;
  wire signal_9_stb;
  wire signal_9_ack;
  wire [15 : 0] signal_10;
  wire signal_10_stb;
  wire signal_10_ack;
  wire [15 : 0] signal_11;
  wire signal_11_stb;
  wire signal_11_ack;
  wire [15 : 0] signal_12;
  wire signal_12_stb;
  wire signal_12_ack;
  wire [15 : 0] signal_13;
  wire signal_13_stb;
  wire signal_13_ack;
  wire [15 : 0] signal_14;
  wire signal_14_stb;
  wire signal_14_ack;

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
    .value (1)
  )
 constant_value_inst_12
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_2),
    .out1_stb (signal_2_stb),
    .out1_ack (signal_2_ack)
  );

  constant_value #(
    .bits (16),
    .value (-1)
  )
 constant_value_inst_11
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_3),
    .out1_stb (signal_3_stb),
    .out1_ack (signal_3_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_29
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_14),
    .in1_stb (signal_14_stb),
    .in1_ack (signal_14_ack)
  );

  constant_value #(
    .bits (16),
    .value (0)
  )
 constant_value_inst_17
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_6),
    .out1_stb (signal_6_stb),
    .out1_ack (signal_6_ack)
  );

  constant_value #(
    .bits (16),
    .value (10)
  )
 constant_value_inst_16
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_7),
    .out1_stb (signal_7_stb),
    .out1_ack (signal_7_ack)
  );

  constant_value #(
    .bits (16),
    .value (0)
  )
 constant_value_inst_15
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_5),
    .out1_stb (signal_5_stb),
    .out1_ack (signal_5_ack)
  );

  constant_value #(
    .bits (16),
    .value (0)
  )
 constant_value_inst_14
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_4),
    .out1_stb (signal_4_stb),
    .out1_ack (signal_4_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_23
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_11),
    .in1_stb (signal_11_stb),
    .in1_ack (signal_11_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_19
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_9),
    .in1_stb (signal_9_stb),
    .in1_ack (signal_9_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_21
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_10),
    .in1_stb (signal_10_stb),
    .in1_ack (signal_10_ack)
  );

  constant_value #(
    .bits (16),
    .value (-1)
  )
 constant_value_inst_26
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_13),
    .out1_stb (signal_13_stb),
    .out1_ack (signal_13_ack)
  );

  constant_value #(
    .bits (16),
    .value (2)
  )
 constant_value_inst_27
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_12),
    .out1_stb (signal_12_stb),
    .out1_ack (signal_12_ack)
  );

  less_than #(
    .bits (16)
  )
 less_than_inst_25
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_12),
    .in2_stb (signal_12_stb),
    .in2_ack (signal_12_ack),
    .in1 (signal_13),
    .in1_stb (signal_13_stb),
    .in1_ack (signal_13_ack),
    .out1 (signal_14),
    .out1_stb (signal_14_stb),
    .out1_ack (signal_14_ack)
  );

  not_equal #(
    .bits (16)
  )
 not_equal_inst_3
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_2),
    .in2_stb (signal_2_stb),
    .in2_ack (signal_2_ack),
    .in1 (signal_3),
    .in1_stb (signal_3_stb),
    .in1_ack (signal_3_ack),
    .out1 (signal_10),
    .out1_stb (signal_10_stb),
    .out1_ack (signal_10_ack)
  );

  constant_value #(
    .bits (16),
    .value (1)
  )
 constant_value_inst_7
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_1),
    .out1_stb (signal_1_stb),
    .out1_ack (signal_1_ack)
  );

  greater_than #(
    .bits (16)
  )
 greater_than_inst_1
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_6),
    .in2_stb (signal_6_stb),
    .in2_ack (signal_6_ack),
    .in1 (signal_7),
    .in1_stb (signal_7_stb),
    .in1_ack (signal_7_ack),
    .out1 (signal_8),
    .out1_stb (signal_8_stb),
    .out1_ack (signal_8_ack)
  );

  equal #(
    .bits (16)
  )
 equal_inst_0
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_0),
    .in1_stb (signal_0_stb),
    .in1_ack (signal_0_ack),
    .in2 (signal_1),
    .in2_stb (signal_1_stb),
    .in2_ack (signal_1_ack),
    .out1 (signal_9),
    .out1_stb (signal_9_stb),
    .out1_ack (signal_9_ack)
  );

  asserter #(
    .bits (16)
  )
 asserter_inst_18
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_8),
    .in1_stb (signal_8_stb),
    .in1_ack (signal_8_ack)
  );

  constant_value #(
    .bits (16),
    .value (1)
  )
 constant_value_inst_6
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_0),
    .out1_stb (signal_0_stb),
    .out1_ack (signal_0_ack)
  );

  greater_than_or_equal #(
    .bits (16)
  )
 greater_than_or_equal_inst_4
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_4),
    .in1_stb (signal_4_stb),
    .in1_ack (signal_4_ack),
    .in2 (signal_5),
    .in2_stb (signal_5_stb),
    .in2_ack (signal_5_ack),
    .out1 (signal_11),
    .out1_stb (signal_11_stb),
    .out1_ack (signal_11_ack)
  );

endmodule
