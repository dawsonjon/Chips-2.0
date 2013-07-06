//name: constant_value
//tag: sources
//output: out1 : bits
//source_file : built_in
//parameter : value: 0
//parameter : bits: 16

///Constant Value
///==============
///
///Output constant value repeatedly.
///::
///
///    out1 <= constant
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
/// bits          integer        Data width of out1.
/// value         integer        Constant value.
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

module constant_value #(
    parameter bits=16,
    parameter value=16
  ) (
    input clk,
    input rst,
    
    output [bits-1:0] out1,
    output out1_stb,
    input out1_ack
  );

  assign out1 = value;
  assign out1_stb = 1'b1;

endmodule
