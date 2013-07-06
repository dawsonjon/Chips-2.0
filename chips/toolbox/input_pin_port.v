//name: device_pin_input
//tag: sources
//output: out1 : bits
//source_file: built_in
//device_in: BUS : pins : port_name : bits
//parameter: bits:16
//parameter:port_name:"pins"
//source_file: built_in

///Device Pin Input
///=================
///
///Generate a stream of data from device pin(s).
///The input pins are automatically double registered.
///
///::
///
///    out1 <= pins
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
/// bits          integer        Data width of out1 and port.
/// port_name     string         The name of the device pin port.
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
///Device Inputs
///-------------
///
///These inputs will automatically be routed to the top level of the
///device, but will not appear as inputs/outputs on the component symbol.
///The parameter *port_name* determines the name given to the device pins.
///Note that ports names must be unique.
///
/// ============= ============== ==============================================
/// Name          Width          Description
/// ============= ============== ==============================================
/// pins          bits           Input port pins
/// ============= ============== ==============================================
///

module device_pin_input #(
    parameter bits=16,
    parameter port_name="pins"
  ) (
    input clk,
    input rst,
    input [bits-1:0] pins,

    output reg [bits-1:0] out1,
    output reg out1_stb,
    input out1_ack
  );

  reg pins_d, pins_d1;

  always @(posedge clk)
  begin
    pins_d   <= pins;
    pins_d1  <= pins_d;
    out1     <= pins_d1;
    out1_stb <= 1'b1;
  end

endmodule
