module my_chip;
  reg  clk;
  reg  rst;
  wire  [15:0] a;
  wire  [15:0] a_stb;
  wire  [15:0] a_ack;
  wire  [15:0] b;
  wire  [15:0] b_stb;
  wire  [15:0] b_ack;
  wire  [15:0] z;
  wire  [15:0] z_stb;
  wire  [15:0] z_ack;
  
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

  module uut my_chip(
    .clk(clk),
    .rst(rst),
    .a(a),
    .a_stb(a_stb),
    .a_ack(a_ack),
    .b(b),
    .b_stb(b_stb),
    .b_ack(b_ack),
    .z(z),
    .z_stb(z_stb),
    .z_ack(z_ack));
endmodule
