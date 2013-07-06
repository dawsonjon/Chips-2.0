//name: console_output
//tag: sinks
//input: in1 : bits
//source_file: built_in
//parameter: bits:16

///Console Output
///==============
///Write a stream of data to the console.
///
///::
///
///    console <= in1
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
/// bits          integer        Data width of in1.
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

module console_output #(
  parameter bits=16
) (
  input clk,
  input rst,

  input [bits-1:0] in1,
  input in1_stb,
  output in1_ack
);


  always @(posedge clk)
  begin
    if (in1_stb) begin
      $display(in1);
    end
  end
  assign in1_ack = in1_stb;

endmodule
