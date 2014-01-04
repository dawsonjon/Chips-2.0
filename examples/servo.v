module servo(clk, rst, rs232_in, rs232_in_stb, rs232_in_ack, rs232_out, servos, rs232_out_stb, servos_stb, rs232_out_ack, servos_ack);
  input  clk;
  input  rst;
  input  [15:0] rs232_in;
  input  rs232_in_stb;
  output rs232_in_ack;
  output [15:0] rs232_out;
  output rs232_out_stb;
  input  rs232_out_ack;
  output [15:0] servos;
  output servos_stb;
  input  servos_ack;
  wire   [15:0] wire_140036826114168;
  wire   wire_140036826114168_stb;
  wire   wire_140036826114168_ack;
  servo_ui servo_ui_32237832(
    .clk(clk),
    .rst(rst),
    .input_rs232(rs232_in),
    .input_rs232_stb(rs232_in_stb),
    .input_rs232_ack(rs232_in_ack),
    .output_control(wire_140036826114168),
    .output_control_stb(wire_140036826114168_stb),
    .output_control_ack(wire_140036826114168_ack),
    .output_rs232(rs232_out),
    .output_rs232_stb(rs232_out_stb),
    .output_rs232_ack(rs232_out_ack));
  servo_controller servo_controller_32246024(
    .clk(clk),
    .rst(rst),
    .input_control(wire_140036826114168),
    .input_control_stb(wire_140036826114168_stb),
    .input_control_ack(wire_140036826114168_ack),
    .output_servos(servos),
    .output_servos_stb(servos_stb),
    .output_servos_ack(servos_ack));
endmodule
