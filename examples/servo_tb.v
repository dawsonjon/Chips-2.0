module servo_tb;
  reg  clk;
  reg  rst;
  wire  [15:0] rs232_in;
  wire  rs232_in_stb;
  wire  rs232_in_ack;
  wire  [15:0] rs232_out;
  wire  rs232_out_stb;
  wire  rs232_out_ack;
  wire  [15:0] servos;
  wire  servos_stb;
  wire  servos_ack;
  
  initial
  begin
    rst <= 1'b1;
    #50 rst <= 1'b0;
  end

  
  initial
  begin
    #1000000 $finish;
  end

  
  initial
  begin
    clk <= 1'b0;
    while (1) begin
      #5 clk <= ~clk;
    end
  end

  servo uut(
    .clk(clk),
    .rst(rst),
    .rs232_in(rs232_in),
    .rs232_in_stb(rs232_in_stb),
    .rs232_in_ack(rs232_in_ack),
    .rs232_out(rs232_out),
    .rs232_out_stb(rs232_out_stb),
    .rs232_out_ack(rs232_out_ack),
    .servos(servos),
    .servos_stb(servos_stb),
    .servos_ack(servos_ack));
endmodule
