--name: bend
--tag: schematic
--output: out1
--input: in1
--source_file: built_in

---Bend
---====
---
---Used to represent a bend or corner in a wire in schematix.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity BEND is

  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    
    IN1         : in  std_logic_vector;
    IN1_STB     : in  std_logic;
    IN1_ACK     : out std_logic;

    OUT1        : out std_logic_vector;
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity BEND;

architecture RTL of BEND is

begin

 OUT1 <= IN1;
 OUT1_STB <= IN1_STB;
 IN1_ACK <= OUT1_ACK;

end architecture RTL;
