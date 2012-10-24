--name: asserter
--tag: sinks
--input: in1 : bits
--source_file: built_in
--parameter : bits : 16

---Asserter
---========
---Raise an exception if *in1* is 0.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;

entity asserter is

  generic(
    BITS : integer
  );
  port(
    CLK     : in std_logic;
    RST     : in std_logic;
   
    IN1     : in std_logic_vector(BITS-1 downto 0);
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
      assert to_integer(signed(IN1)) /= 0;
    end if;
  end process;
  IN1_ACK <= S_IN1_ACK;

end RTL;
