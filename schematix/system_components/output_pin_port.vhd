--name: device_pin_output_16
--tag: sinks
--input: in1 : 16
--source_file: built_in
--device_out: output_port : 16

---16-bit Device Pin Output
---========================
---
---Send a stream of data to a device pin(s).

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DEVICE_PIN_OUTPUT_16 is

  port(
    CLK         : in std_logic;
    RST         : in std_logic;
    OUTPUT_PORT : in std_logic_vector(15 downto 0);
   
    IN1        : out std_logic_vector(15 downto 0);
    IN1_STB    : out std_logic;
    IN1_ACK    : in  std_logic
  );

end entity DEVICE_PIN_OUTPUT_16;

architecture RTL of DEVICE_PIN_OUTPUT_16 is

begin

  OUTPUT_PORT <= IN1;
  IN1_ACK <= '1';

end architecture RTL;
