--name: asserter
--tag: sinks
--input: in1
--source_file: built_in

---Asserter
---========
---Raise an exception if *in1* is 0.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;

entity asserter is

  port(
    CLK     : in std_logic;
    RST     : in std_logic;
   
    IN1     : in std_logic_vector(15 downto 0);
    IN1_STB : in std_logic;
    IN1_ACK : out std_logic
  );

end entity asserter;

architecture RTL of asserter is
  signal S_IN1_ACK : std_logic;
begin

  process
    variable OUTPUT_LINE : line;
    variable INT  : integer;
  begin
    wait until rising_edge(CLK);
    S_IN1_ACK <= IN1_STB;
    if IN1_STB = '1' and S_IN1_ACK = '1' then
      assert IN1 \= "000000000000000000";
    end if;
  end process;
  IN1_ACK <= S_IN1_ACK;

end RTL;
