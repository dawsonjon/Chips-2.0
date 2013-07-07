//device_in: BUS: input_pins : "input_pins" : 16
//device_out: BUS: output_pins : "output_pins" : 16
//name: test_suite
//source_file: test_suite.sch
//dependency: divider_test
//dependency: divider
//dependency: device_pin_input
//dependency: device_pin_output
//dependency: bend
//dependency: multiplier_test
//dependency: multiplier
//dependency: modulo
//dependency: modulo_test
//dependency: adder_test
//dependency: adder
//dependency: subtractor_test
//dependency: subtractor
`timescale 1ns/1ps
module test_suite (
    input_pins,
    output_pins
);

  input [15 : 0] input_pins;
  output [15 : 0] output_pins;

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
  wire [15 : 0] signal_15;
  wire signal_15_stb;
  wire signal_15_ack;
  wire [15 : 0] signal_16;
  wire signal_16_stb;
  wire signal_16_ack;
  wire [15 : 0] signal_17;
  wire signal_17_stb;
  wire signal_17_ack;
  wire [15 : 0] signal_18;
  wire signal_18_stb;
  wire signal_18_ack;
  wire [15 : 0] signal_19;
  wire signal_19_stb;
  wire signal_19_ack;
  wire [15 : 0] signal_20;
  wire signal_20_stb;
  wire signal_20_ack;
  wire [15 : 0] signal_21;
  wire signal_21_stb;
  wire signal_21_ack;
  wire [15 : 0] signal_22;
  wire signal_22_stb;
  wire signal_22_ack;
  wire [15 : 0] signal_23;
  wire signal_23_stb;
  wire signal_23_ack;
  wire [15 : 0] signal_24;
  wire signal_24_stb;
  wire signal_24_ack;
  wire [15 : 0] signal_25;
  wire signal_25_stb;
  wire signal_25_ack;
  wire [15 : 0] signal_26;
  wire signal_26_stb;
  wire signal_26_ack;
  wire [15 : 0] signal_27;
  wire signal_27_stb;
  wire signal_27_ack;
  wire [15 : 0] signal_28;
  wire signal_28_stb;
  wire signal_28_ack;
  wire [15 : 0] signal_29;
  wire signal_29_stb;
  wire signal_29_ack;
  wire [15 : 0] signal_30;
  wire signal_30_stb;
  wire signal_30_ack;
  wire [15 : 0] signal_31;
  wire signal_31_stb;
  wire signal_31_ack;
  wire [15 : 0] signal_32;
  wire signal_32_stb;
  wire signal_32_ack;
  wire [15 : 0] signal_33;
  wire signal_33_stb;
  wire signal_33_ack;
  wire [15 : 0] signal_34;
  wire signal_34_stb;
  wire signal_34_ack;
  wire [15 : 0] signal_35;
  wire signal_35_stb;
  wire signal_35_ack;

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

  divider_test divider_test_inst_48
  (
    .clk (clk),
    .rst (rst),
    .output_b (signal_22),
    .output_b_stb (signal_22_stb),
    .output_b_ack (signal_22_ack),
    .output_a (signal_23),
    .output_a_stb (signal_23_stb),
    .output_a_ack (signal_23_ack),
    .input_a (signal_28),
    .input_a_stb (signal_28_stb),
    .input_a_ack (signal_28_ack)
  );

  divider #(
    .bits (16)
  )
 divider_inst_49
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_22),
    .in2_stb (signal_22_stb),
    .in2_ack (signal_22_ack),
    .in1 (signal_23),
    .in1_stb (signal_23_stb),
    .in1_ack (signal_23_ack),
    .out1 (signal_24),
    .out1_stb (signal_24_stb),
    .out1_ack (signal_24_ack)
  );

  device_pin_input #(
    .bits (16),
    .port_name ("input_pins")
  )
 device_pin_input_inst_44
  (
    .clk (clk),
    .rst (rst),
    .pins (input_pins),
    .out1 (signal_21),
    .out1_stb (signal_21_stb),
    .out1_ack (signal_21_ack)
  );

  device_pin_output #(
    .bits (16),
    .port_name ("output_pins")
  )
 device_pin_output_inst_45
  (
    .clk (clk),
    .rst (rst),
    .pins (output_pins),
    .in1 (signal_21),
    .in1_stb (signal_21_stb),
    .in1_ack (signal_21_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_40
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_16),
    .in1_stb (signal_16_stb),
    .in1_ack (signal_16_ack),
    .out1 (signal_17),
    .out1_stb (signal_17_stb),
    .out1_ack (signal_17_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_41
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_17),
    .in1_stb (signal_17_stb),
    .in1_ack (signal_17_ack),
    .out1 (signal_18),
    .out1_stb (signal_18_stb),
    .out1_ack (signal_18_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_42
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_18),
    .in1_stb (signal_18_stb),
    .in1_ack (signal_18_ack),
    .out1 (signal_19),
    .out1_stb (signal_19_stb),
    .out1_ack (signal_19_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_43
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_19),
    .in1_stb (signal_19_stb),
    .in1_ack (signal_19_ack),
    .out1 (signal_20),
    .out1_stb (signal_20_stb),
    .out1_ack (signal_20_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_11
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_8),
    .in1_stb (signal_8_stb),
    .in1_ack (signal_8_ack),
    .out1 (signal_9),
    .out1_stb (signal_9_stb),
    .out1_ack (signal_9_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_10
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_7),
    .in1_stb (signal_7_stb),
    .in1_ack (signal_7_ack),
    .out1 (signal_8),
    .out1_stb (signal_8_stb),
    .out1_ack (signal_8_ack)
  );

  multiplier_test multiplier_test_inst_39
  (
    .clk (clk),
    .rst (rst),
    .output_b (signal_14),
    .output_b_stb (signal_14_stb),
    .output_b_ack (signal_14_ack),
    .output_a (signal_15),
    .output_a_stb (signal_15_stb),
    .output_a_ack (signal_15_ack),
    .input_a (signal_20),
    .input_a_stb (signal_20_stb),
    .input_a_ack (signal_20_ack)
  );

  multiplier #(
    .bits (16)
  )
 multiplier_inst_37
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_14),
    .in2_stb (signal_14_stb),
    .in2_ack (signal_14_ack),
    .in1 (signal_15),
    .in1_stb (signal_15_stb),
    .in1_ack (signal_15_ack),
    .out1 (signal_16),
    .out1_stb (signal_16_stb),
    .out1_ack (signal_16_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_59
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_34),
    .in1_stb (signal_34_stb),
    .in1_ack (signal_34_ack),
    .out1 (signal_35),
    .out1_stb (signal_35_stb),
    .out1_ack (signal_35_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_58
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_33),
    .in1_stb (signal_33_stb),
    .in1_ack (signal_33_ack),
    .out1 (signal_34),
    .out1_stb (signal_34_stb),
    .out1_ack (signal_34_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_57
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_32),
    .in1_stb (signal_32_stb),
    .in1_ack (signal_32_ack),
    .out1 (signal_33),
    .out1_stb (signal_33_stb),
    .out1_ack (signal_33_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_56
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_31),
    .in1_stb (signal_31_stb),
    .in1_ack (signal_31_ack),
    .out1 (signal_32),
    .out1_stb (signal_32_stb),
    .out1_ack (signal_32_ack)
  );

  modulo #(
    .bits (16)
  )
 modulo_inst_55
  (
    .clk (clk),
    .rst (rst),
    .in2 (signal_29),
    .in2_stb (signal_29_stb),
    .in2_ack (signal_29_ack),
    .in1 (signal_30),
    .in1_stb (signal_30_stb),
    .in1_ack (signal_30_ack),
    .out1 (signal_31),
    .out1_stb (signal_31_stb),
    .out1_ack (signal_31_ack)
  );

  modulo_test modulo_test_inst_54
  (
    .clk (clk),
    .rst (rst),
    .output_b (signal_29),
    .output_b_stb (signal_29_stb),
    .output_b_ack (signal_29_ack),
    .output_a (signal_30),
    .output_a_stb (signal_30_stb),
    .output_a_ack (signal_30_ack),
    .input_a (signal_35),
    .input_a_stb (signal_35_stb),
    .input_a_ack (signal_35_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_53
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_27),
    .in1_stb (signal_27_stb),
    .in1_ack (signal_27_ack),
    .out1 (signal_28),
    .out1_stb (signal_28_stb),
    .out1_ack (signal_28_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_52
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_26),
    .in1_stb (signal_26_stb),
    .in1_ack (signal_26_ack),
    .out1 (signal_27),
    .out1_stb (signal_27_stb),
    .out1_ack (signal_27_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_51
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_25),
    .in1_stb (signal_25_stb),
    .in1_ack (signal_25_ack),
    .out1 (signal_26),
    .out1_stb (signal_26_stb),
    .out1_ack (signal_26_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_50
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_24),
    .in1_stb (signal_24_stb),
    .in1_ack (signal_24_ack),
    .out1 (signal_25),
    .out1_stb (signal_25_stb),
    .out1_ack (signal_25_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_9
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_6),
    .in1_stb (signal_6_stb),
    .in1_ack (signal_6_ack),
    .out1 (signal_7),
    .out1_stb (signal_7_stb),
    .out1_ack (signal_7_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_8
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_5),
    .in1_stb (signal_5_stb),
    .in1_ack (signal_5_ack),
    .out1 (signal_6),
    .out1_stb (signal_6_stb),
    .out1_ack (signal_6_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_3
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_1),
    .in1_stb (signal_1_stb),
    .in1_ack (signal_1_ack),
    .out1 (signal_2),
    .out1_stb (signal_2_stb),
    .out1_ack (signal_2_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_2
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_0),
    .in1_stb (signal_0_stb),
    .in1_ack (signal_0_ack),
    .out1 (signal_1),
    .out1_stb (signal_1_stb),
    .out1_ack (signal_1_ack)
  );

  adder_test adder_test_inst_1
  (
    .clk (clk),
    .rst (rst),
    .input_a (signal_4),
    .input_a_stb (signal_4_stb),
    .input_a_ack (signal_4_ack),
    .output_a (signal_12),
    .output_a_stb (signal_12_stb),
    .output_a_ack (signal_12_ack),
    .output_b (signal_13),
    .output_b_stb (signal_13_stb),
    .output_b_ack (signal_13_ack)
  );

  adder #(
    .bits (16)
  )
 adder_inst_0
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_0),
    .out1_stb (signal_0_stb),
    .out1_ack (signal_0_ack),
    .in1 (signal_12),
    .in1_stb (signal_12_stb),
    .in1_ack (signal_12_ack),
    .in2 (signal_13),
    .in2_stb (signal_13_stb),
    .in2_ack (signal_13_ack)
  );

  subtractor_test subtractor_test_inst_7
  (
    .clk (clk),
    .rst (rst),
    .input_a (signal_9),
    .input_a_stb (signal_9_stb),
    .input_a_ack (signal_9_ack),
    .output_a (signal_10),
    .output_a_stb (signal_10_stb),
    .output_a_ack (signal_10_ack),
    .output_b (signal_11),
    .output_b_stb (signal_11_stb),
    .output_b_ack (signal_11_ack)
  );

  subtractor #(
    .bits (16)
  )
 subtractor_inst_6
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_5),
    .out1_stb (signal_5_stb),
    .out1_ack (signal_5_ack),
    .in1 (signal_10),
    .in1_stb (signal_10_stb),
    .in1_ack (signal_10_ack),
    .in2 (signal_11),
    .in2_stb (signal_11_stb),
    .in2_ack (signal_11_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_5
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_3),
    .in1_stb (signal_3_stb),
    .in1_ack (signal_3_ack),
    .out1 (signal_4),
    .out1_stb (signal_4_stb),
    .out1_ack (signal_4_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_4
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_2),
    .in1_stb (signal_2_stb),
    .in1_ack (signal_2_ack),
    .out1 (signal_3),
    .out1_stb (signal_3_stb),
    .out1_ack (signal_3_ack)
  );

endmodule
