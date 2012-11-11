--name: device_pin_output
--tag: sinks
--input: in1 : bits
--source_file: built_in
--device_out: BUS : PINS : port_name : bits
--parameter: bits:16
--parameter:port_name:"PINS"

---Device Pin Output
---=================
---
---Send a stream of data to a device pin(s).

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DEVICE_PIN_OUTPUT is

  generic(
    BITS : integer;
    PORT_NAME : string
  );
  port(
    CLK     : in std_logic;
    RST     : in std_logic;
    PINS    : out std_logic_vector(BITS-1 downto 0);
   
    IN1     : in std_logic_vector(BITS-1 downto 0);
    IN1_STB : in std_logic;
    IN1_ACK : out  std_logic
  );

end entity DEVICE_PIN_OUTPUT;

architecture RTL of DEVICE_PIN_OUTPUT is

begin

  PINS <= IN1;
  IN1_ACK <= '1';

end architecture RTL;
