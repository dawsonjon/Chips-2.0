//name: tee
//tag: schematic
//input: in1: bits
//output: out1: bits
//output: out2: bits
//parameter:bits:16
//source_file: built_in

///Tee
///===
///
///Used to represent a tee junction in a schematic wire.
///Duplicates *in1 on *out1* and *out2* item by item.
///
///::
///
///    out1 <= in1
///    out2 <= in1
///
///..
///
/// +--------------------+-------------------------------------+
/// |Language            | Verilog                             |
/// +--------------------+-------------------------------------+
/// |Synthesis           | Yes                                 |
/// +--------------------+-------------------------------------+
/// |License             | MIT                                 |
/// +--------------------+-------------------------------------+
/// |Author              | Jonathan P Dawson                   |
/// +--------------------+-------------------------------------+
/// |Copyright           | Jonathan P Dawson 2013              |
/// +--------------------+-------------------------------------+
///
///Parameters
///----------
///
/// ============= ============== ==============================================
/// Name          Type           Description
/// ============= ============== ==============================================
/// bits          integer        Data width of in1, out1 and out2
/// ============= ============== ==============================================
///
///Inputs
///------
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// in1           bits           Input Stream
/// ============= ============== ==============================================
///
///Outputs
///-------
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// out1          bits           Output Stream
/// out2          bits           Output Stream
/// ============= ============== ==============================================
///

module tee #( parameter bits = 16)(
    input clk,
    input rst,
    
    input  [bits-1 : 0] in1,
    input in1_stb,
    output reg in1_ack,

    output reg [bits-1 : 0] out1,
    output reg out1_stb,
    input out1_ack,

    output reg [bits-1 : 0] out2,
    output reg out2_stb,
    input out2_ack
);
    localparam read_a = 2'd0;
    localparam write_y = 2'd1;
    localparam write_z = 2'd2;
    reg [1:0] state;


    always @(posedge clk)
    begin

      case(state)
        read_a: 
        begin
           in1_ack <= 1'b1;
           if (in1_stb && in1_ack) begin
             out1 <= in1;
             out2 <= in1;
             in1_ack <= 1'b0;
             out1_stb <= 1'b1;
             state <= write_y;
           end
        end

        write_y: 
        begin
          if (out1_ack && out1_stb) begin
            out1_stb <= 1'b0;
            out2_stb <= 1'b1;
            state <= write_z;
          end
        end

        write_z: 
        begin
          if (out2_ack && out2_stb) begin
            out2_stb <= 1'b0;
            in1_ack <= 1'b1;
            state <= read_a;
          end
        end

      endcase
      if (rst == 1'b1) begin
        state  <= read_a;
        in1_ack  <= 1'b0;
        out1_stb <= 1'b0;
        out2_stb <= 1'b0;
      end
  end

endmodule
