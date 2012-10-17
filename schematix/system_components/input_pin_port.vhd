--name: input_pin_port
--tag: IO
--output: out1
--source_file: built_in
--device_in: input_port : 8

---Input Pin Port
---==============
---

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity input_pin_port is

  port(
    CLK         : in std_logic;
    RST         : in  std_logic;
    INPUT_PORT  : in std_logic_vector;
   
    OUT1        : out std_logic_vector;
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in std_logic
  );

end entity input_pin_port;

architecture RTL of input_pin_port is

begin

  OUT1 <= INPUT_PORT;
  OUT1_STB <= '1';

end architecture RTL;
