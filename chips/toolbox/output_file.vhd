--name: file_output
--tag: sinks
--input: in1 : bits
--source_file: built_in
--parameter: bits:16
--parameter: filename:output_file

---File Output
---==============
---Write a stream of data to a text file as an ASCII decimal representation.
---
---:input: in1 - The input data stream
---:parameter: bits - The *width* in bits of the input data stream
---:parameter: filename - The *file name*  of the output file.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;

entity file_output is

  generic(
    FILENAME : string;
    BITS : integer
  );
  port(
    CLK     : in std_logic;
    RST     : in std_logic;
   
    IN1     : in std_logic_vector(BITS-1 downto 0);
    IN1_STB : in std_logic;
    IN1_ACK : out std_logic
  );

end entity file_output;

architecture RTL of file_output is
begin

  process
    variable OUTPUT_LINE : line;
    variable INT  : integer;
    file OUTFILE : text open write_mode is FILENAME;
  begin
    wait until rising_edge(CLK);
    if IN1_STB = '1' then
      INT := to_integer(signed(IN1));
      write(OUTPUT_LINE, INT);
      writeline(OUTFILE, OUTPUT_LINE);
    end if;
  end process;
  IN1_ACK <= '1';

end RTL;
