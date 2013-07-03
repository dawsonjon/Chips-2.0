//name: subtractor
//tag: arithmetic
//input: in1: bits
//input: in2: bits
//output: out1: bits
//parameter:bits:16
//source_file: built_in

///Subtractor
///==========
///
///Produces a stream of data *out1* by subtracting *in2* from *in1* item by item.
///
///::
///
///    out1 <= in1 - in2
///
///+--------------------+-------------------------------------+
///|Language            | Verilog                             |
///+--------------------+-------------------------------------+
///|Synthesis           | Yes                                 |
///+--------------------+-------------------------------------+
///|License             | MIT                                 |
///+--------------------+-------------------------------------+
///|Author              | Jonathan P Dawson                   |
///+--------------------+-------------------------------------+
///|Copyright           | Jonathan P Dawson 2013              |
///+--------------------+-------------------------------------+
///
///Parameters
///----------
///
/// ============= ============== ==============================================
/// Name          Type           Description
/// ============= ============== ==============================================
/// bits          integer        Data width of in1, in2 and in3
/// ============= ============== ==============================================
///
///Inputs
///------
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// in1           bit            Input Stream
/// in2           bit            Input Stream
/// ============= ============== ==============================================
///
///Outputs
///-------
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// out1          bits           Output Stream
/// ============= ============== ==============================================
///

module subtractor #( parameter bits = 16)(
    input clk,
    input rst,
    
    input  [bits-1 : 0] in1,
    input in1_stb,
    output reg in1_ack,

    input [bits-1 : 0] in2,
    input in2_stb,
    output reg in2_ack,

    output reg [bits-1 : 0] out1,
    output reg out1_stb,
    input out1_ack
);
    localparam read_a_b = 2'd0;
    localparam read_a = 2'd1;
    localparam read_b = 2'd2;
    localparam write_z = 2'd3;
    reg [1:0] state;
    reg [bits-1:0] a, b;


    always @(posedge clk)
    begin

     case(state)
        read_a_b: 
        begin
           in1_ack <= 1'b1;
           in2_ack <= 1'b1;
           if (in1_stb && in1_ack && in2_stb && in2_ack) begin
             out1 <= $signed(in1) - $signed(in2);
             in1_ack <= 1'b0;
             in2_ack <= 1'b0;
             state <= write_z;
           end else if (in1_stb && in1_ack) begin
             in1_ack <= 1'b0;
             state <= read_b;
             a <= in1;
           end else if (in2_stb && in2_ack) begin
             in2_ack <= 1'b0;
             state <= read_a;
             b <= in2;
           end
        end

        read_a: 
        begin
           if (in1_stb && in1_ack) begin
             in1_ack <= 1'b0;
             out1 <= $signed(in1) - $signed(b);
             state <= write_z;
           end
        end

        read_b: 
        begin
           if (in2_stb && in2_ack) begin
             in2_ack <= 1'b0;
             out1 <= $signed(a) - $signed(in2);
             state <= write_z;
           end
        end

        write_z: 
        begin
          out1_stb <= 1'b1;
          if (out1_ack && out1_stb) begin
            out1_stb <= 1'b0;
            state <= read_a_b;
          end
        end
      endcase
    if (rst == 1'b1) begin
      state  <= read_a_b;
      in1_ack  <= 1'b0;
      in2_ack  <= 1'b0;
      out1_stb <= 1'b0;
    end
  end

endmodule
