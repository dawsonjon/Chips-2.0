//name: device_pin_output
//tag: sinks
//input: in1 : bits
//source_file: built_in
//device_out: BUS : pins : port_name : bits
//parameter: bits:16
//parameter:port_name:"pins"
//source_file: built_in

///Device Pin Output
///=================
///
///Send a stream of data to a device pin(s).
///Produces a stream of data *out1* by adding *in2* to *in1* item by item.
///
///::
///
///    pins <= in1
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
/// bits          integer        Data width of in1, in2 and out1
/// port_name     string         The name of the device pin port.
/// ============= ============== ==============================================
///
///Inputs
///------
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// in1           bit            Input Stream
/// ============= ============== ==============================================
///

module device_pin_output #(
    parameter bits=16,
    parameter port_name="pins"
  ) (
    input clk,
    input rst,
    output reg [bits-1:0] pins,
    input [bits-1:0] in1,
    input in1_stb,
    output reg in1_ack
  );

  always @(posedge clk)
  begin
    if (in1_stb) begin
      pins <= in1;
    end
    in1_ack <= 1'b1;
  end

endmodule
