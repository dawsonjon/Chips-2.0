//name: asserter
//tag: sinks
//input: in1 : bits
//source_file: built_in
//parameter : bits : 16

///Asserter
///========
///
///Raise an exception if *in1* is 0.
///
///::
///
///    assert(in1)
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

module asserter  #(

    parameter bits=16
  )(
    input clk,
    input rst,
    input [bits-1:0] in1,
    input in1_stb,
    output in1_ack
  );

  always @(posedge clk)
  begin
    if (in1_stb) begin
      if (in1 == 0) begin
        $display("Assertion failed");
        $finish_and_return(1);
      end
    end
  end

  assign in1_ack = s_in1_ack;

endmodule 
