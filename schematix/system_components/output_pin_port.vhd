--name: output_pin_port
--tag: IO
--input: in1
--source_file: built_in
--device_out: output_port : n

---Output Pin Port
---===============
---

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity input_pin_port is

  port(
    CLK         : in std_logic;
    RST         : in std_logic;
    OUTPUT_PORT : in std_logic_vector;
   
    IN1        : out std_logic_vector;
    IN1_STB    : out std_logic;
    IN1_ACK    : in  std_logic
  );

end entity input_pin_port;

architecture RTL of input_pin_port is

begin

  OUTPUT_PORT <= IN1;
  IN1_ACK <= '1';

end architecture RTL;
