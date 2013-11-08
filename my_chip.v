module my_chip;
  input  clk;
  input  rst;
  input  [15:0] a;
  input  [15:0] a_stb;
  output [15:0] a_ack;
  input  [15:0] b;
  input  [15:0] b_stb;
  output [15:0] b_ack;
  output [15:0] z;
  output [15:0] z_stb;
  input  [15:0] z_ack;
  module 139806687686096_adder adder(
    .input_a(a),
    .input_a_stb(a_stb),
    .input_a_ack(a_ack),
    .input_b(b),
    .input_b_stb(b_stb),
    .input_b_ack(b_ack),
    .output_z(z),
    .output_z_stb(z_stb),
    .output_z_ack(z_ack));
endmodule
