--name: console_output
--tag: sinks
--input: in1
--source_file: built_in

---16-bit Console Output
---=====================
---Write a stream of data to the console.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;

entity console_output is

  port(
    CLK     : in std_logic;
    RST     : in std_logic;
   
    IN1     : in std_logic_vector(15 downto 0);
    IN1_STB : in std_logic;
    IN1_ACK : out std_logic
  );

end entity console_output;

architecture RTL of console_output is
  signal S_IN1_ACK : std_logic;
begin

  process
    variable OUTPUT_LINE : line;
    variable INT  : integer;
  begin
    wait until rising_edge(CLK);
    S_IN1_ACK <= IN1_STB;
    if IN1_STB = '1' and S_IN1_ACK = '1' then
      INT := to_integer(signed(IN1));
      report integer'image(INT);
      write(OUTPUT_LINE, INT);
      writeline(output, OUTPUT_LINE);
      S_IN1_ACK <= '1';
    end if;
  end process;
  IN1_ACK <= S_IN1_ACK;

end RTL;
