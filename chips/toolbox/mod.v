//name:modulo 
//tag: arithmetic
//input: in1: bits
//input: in2: bits
//output: out1 : bits
//parameter: bits: 16
//source_file: built_in

///Modulo
///=======
///
///Produces a stream of data *out1* by performing the modulo of *in1* and *in2* item by item.
///
///::
///
///    out1 <= in1 % in2
///
///..
///
///  +--------------------+-------------------------------------+
///  |Language            | Verilog                             |
///  +--------------------+-------------------------------------+
///  |Synthesis           | Yes                                 |
///  +--------------------+-------------------------------------+
///  |License             | MIT                                 |
///  +--------------------+-------------------------------------+
///  |Author              | Jonathan P Dawson                   |
///  +--------------------+-------------------------------------+
///  |Copyright           | Jonathan P Dawson 2013              |
///  +--------------------+-------------------------------------+
///
///Parameters
///----------
///
/// ============= ============== ==============================================
/// Name          Type           Description
/// ============= ============== ==============================================
/// bits          integer        Data width of in1, in2 and out1
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

module modulo #( parameter bits = 16)(
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

  reg       [15:0] a;
  reg       [15:0] b;
  reg       [15:0] divisor;
  reg       [15:0] dividend;
  reg       [15:0] quotient;
  reg       [15:0] remainder;
  reg       [4:0] count;
  reg       [2:0] state;
  reg       sign;
  wire      [15:0] difference;

  localparam [2:0] read_a_b = 3'd0;
  localparam [2:0] read_a = 3'd1;
  localparam [2:0] read_b = 3'd2;
  localparam [2:0] start = 3'd3;
  localparam [2:0] calculate = 3'd4;
  localparam [2:0] finish = 3'd5;
  localparam [2:0] write_z = 3'd6;

  always @(posedge clk)
  begin

    case (state)

        read_a_b: 
        begin
           in1_ack <= 1'b1;
           in2_ack <= 1'b1;
           if (in1_stb && in1_ack && in2_stb && in2_ack) begin
             divisor <= in1;
             dividend <= in2;
             in1_ack <= 1'b0;
             in2_ack <= 1'b0;
             state <= start;
           end else if (in1_stb && in1_ack) begin
             in1_ack <= 1'b0;
             state <= read_b;
             divisor <= in1;
           end else if (in2_stb && in2_ack) begin
             in2_ack <= 1'b0;
             state <= read_a;
             dividend <= in2;
           end
        end

        read_a: 
        begin
           if (in1_stb && in1_ack) begin
             in1_ack <= 1'b0;
             divisor <= in1;
             state <= start;
           end
        end

        read_b: 
        begin
           if (in2_stb && in2_ack) begin
             in2_ack <= 1'b0;
             dividend <= in2;
             state <= start;
           end
        end

      start: 
      begin

        a <= divisor[15]?-divisor:divisor;
        b <= dividend[15]?-dividend:dividend;
        remainder <= 15'd0;
        quotient <= 15'd0;
        sign  <= divisor[15] ^ dividend[15];
        count <= 5'd16;
        state <= calculate;

      end //start

      calculate: 
      begin

        if( difference[15] == 0 ) begin //if remainder > b
          quotient <= quotient * 2 + 1;
          remainder <= {difference[14:0], a[15]};
        end else begin
          quotient <= quotient * 2;
          remainder <= {remainder[14:0], a[15]};
        end

        a <= a * 2;
        if( count == 5'd0 ) begin
          state <= finish;
        end else begin
          count <= count - 1;
        end

      end //calculate

      finish: 
      begin

        out1     <= divisor[15]?-(remainder/2):remainder/2;
        state    <= write_z;

      end //finish

      write_z: 
      begin

	out1_stb <= 1'b1;
	if (out1_ack & out1_stb) begin
	  out1_stb <= 1'b0;
          state    <= read_a_b;
	end

      end //wait

    endcase

    if( rst ) begin
      in1_ack  <= 1'b0;
      in2_ack  <= 1'b0;
      out1_stb <= 1'b0;
      state <= read_a_b;
    end
  end

  assign difference = remainder - b;

endmodule
