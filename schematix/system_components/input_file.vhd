--name: file_input
--tag: sources
--output: out1 : bits
--parameter: bits:16
--parameter: filename:input_file
--source_file: built_in

---File Input
---================
---Read a stream of data from a text file in ASCII decimal representation.
---
---:output: out1 - The output data stream
---:parameter: bits - The *width* in bits of the output data stream
---:parameter: filename - The *file name*  of the input file.
---

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;

entity file_input is

  generic(
    FILENAME : string;
    BITS : integer
  );
  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
   
    OUT1        : out std_logic_vector(BITS-1 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity file_input;

architecture RTL of file_input is

begin

  process

    file INFILE : text open read_mode is FILENAME;
    variable INLINE : LINE;
    variable VALUE : integer;

  begin

    if not ENDFILE(INFILE) then
      OUT1_STB <= '1';
      readline(INFILE, INLINE);
      read(INLINE, VALUE);
      OUT1 <= std_logic_vector(to_signed(VALUE, BITS));    
    end if;
  
    while true loop
      wait until rising_edge(CLK);
      if OUT1_ACK = '1' and RST = '0' then
        if not ENDFILE(INFILE) then
          readline(INFILE, INLINE);
          read(INLINE, VALUE);
          OUT1 <= std_logic_vector(to_signed(VALUE, BITS));
        else
          OUT1_STB <= '0';
          exit;
        end if;
      end if;
    end loop;
    wait;
  end process;

end architecture RTL;
