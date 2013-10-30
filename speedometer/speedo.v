//device_out: BUS: digit_select : "digit_select" : 4
//device_in: BUS: sensor : "sensor" : 1
//device_out: BUS: seven_segment : "seven_segment" : 7
//name: speedo
//source_file: speedo.sch
//dependency: bend
//dependency: resizer
//dependency: device_pin_output
//dependency: device_pin_input
//dependency: display_driver
//dependency: count_revs
//dependency: seconds
`timescale 1ns/1ps
module speedo (
    digit_select,
    sensor,
    seven_segment
);

  output [3 : 0] digit_select;
  input [0 : 0] sensor;
  output [6 : 0] seven_segment;

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
  wire signal_4 : std_logic;
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
  wire [3 : 0] signal_8;
  wire signal_8_stb;
  wire signal_8_ack;
  wire [15 : 0] signal_9;
  wire signal_9_stb;
  wire signal_9_ack;
  wire [15 : 0] signal_10;
  wire signal_10_stb;
  wire signal_10_ack;
  wire [6 : 0] signal_11;
  wire signal_11_stb;
  wire signal_11_ack;

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

  bend #(
    .bits (16)
  )
 bend_inst_13
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

  resizer #(
    .output_bits (16),
    .input_bits (1)
  )
 resizer_inst_12
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_4),
    .in1_stb (signal_4_stb),
    .in1_ack (signal_4_ack),
    .out1 (signal_5),
    .out1_stb (signal_5_stb),
    .out1_ack (signal_5_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_10
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_3),
    .in1_stb (signal_3_stb),
    .in1_ack (signal_3_ack),
    .out1 (signal_9),
    .out1_stb (signal_9_stb),
    .out1_ack (signal_9_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_16
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_9),
    .in1_stb (signal_9_stb),
    .in1_ack (signal_9_ack),
    .out1 (signal_10),
    .out1_stb (signal_10_stb),
    .out1_ack (signal_10_ack)
  );

  resizer #(
    .output_bits (4),
    .input_bits (16)
  )
 resizer_inst_15
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

  resizer #(
    .output_bits (7),
    .input_bits (16)
  )
 resizer_inst_14
  (
    .clk (clk),
    .rst (rst),
    .in1 (signal_10),
    .in1_stb (signal_10_stb),
    .in1_ack (signal_10_ack),
    .out1 (signal_11),
    .out1_stb (signal_11_stb),
    .out1_ack (signal_11_ack)
  );

  device_pin_output #(
    .port_name ("digit_select"),
    .bits (4)
  )
 device_pin_output_inst_8
  (
    .clk (clk),
    .rst (rst),
    .pins (digit_select),
    .in1 (signal_8),
    .in1_stb (signal_8_stb),
    .in1_ack (signal_8_ack)
  );

  device_pin_input #(
    .port_name ("sensor"),
    .bits (1)
  )
 device_pin_input_inst_3
  (
    .clk (clk),
    .rst (rst),
    .pins (sensor),
    .out1 (signal_4),
    .out1_stb (signal_4_stb),
    .out1_ack (signal_4_ack)
  );

  display_driver display_driver_inst_2
  (
    .clk (clk),
    .rst (rst),
    .input_speed (signal_1),
    .input_speed_stb (signal_1_stb),
    .input_speed_ack (signal_1_ack),
    .output_digit (signal_3),
    .output_digit_stb (signal_3_stb),
    .output_digit_ack (signal_3_ack),
    .output_digit_select (signal_7),
    .output_digit_select_stb (signal_7_stb),
    .output_digit_select_ack (signal_7_ack)
  );

  count_revs count_revs_inst_1
  (
    .clk (clk),
    .rst (rst),
    .input_seconds (signal_0),
    .input_seconds_stb (signal_0_stb),
    .input_seconds_ack (signal_0_ack),
    .output_speed (signal_1),
    .output_speed_stb (signal_1_stb),
    .output_speed_ack (signal_1_ack),
    .input_sensor (signal_2),
    .input_sensor_stb (signal_2_stb),
    .input_sensor_ack (signal_2_ack)
  );

  seconds seconds_inst_0
  (
    .clk (clk),
    .rst (rst),
    .output_tick (signal_0),
    .output_tick_stb (signal_0_stb),
    .output_tick_ack (signal_0_ack)
  );

  device_pin_output #(
    .port_name ("seven_segment"),
    .bits (7)
  )
 device_pin_output_inst_7
  (
    .clk (clk),
    .rst (rst),
    .pins (seven_segment),
    .in1 (signal_11),
    .in1_stb (signal_11_stb),
    .in1_ack (signal_11_ack)
  );

  bend #(
    .bits (16)
  )
 bend_inst_5
  (
    .clk (clk),
    .rst (rst),
    .out1 (signal_2),
    .out1_stb (signal_2_stb),
    .out1_ack (signal_2_ack),
    .in1 (signal_6),
    .in1_stb (signal_6_stb),
    .in1_ack (signal_6_ack)
  );

endmodule
