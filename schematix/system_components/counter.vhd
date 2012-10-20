--name: counter
--tag: sources
--output: out1
--source_file: built_in
--parameter: start: 0
--parameter: stop: 10
--parameter: step: 1

---Counter
---=======
---
---A counter component
---
---+ The first data item in the sequence is defined by the *start* parameter.
---+ Subsequent data item in the sequence are ncremented by the *step* parameter.
---+ The counter may reach, but not exceed the *stop* parameter.
---+ Any count in excess of *stop* will return the counter to the *start* value.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is

  generic(
    START       : integer;
    STOP        : integer;
    STEP        : integer
  );
  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    
    OUT1        : out std_logic_vector(15 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity counter;

architecture RTL of counter is

  signal COUNT : integer range START to STOP;

begin

  OUT1_STB <= '1';
  OUT1 <= std_logic_vector(to_unsigned(COUNT, OUT1'length));
  process
  begin
    wait until rising_edge(CLK);

    if OUT1_ACK = '1' then
      if COUNT + STEP > STOP then
        COUNT <= START;
      else
        COUNT <= COUNT + STEP;
      end if;
    end if;

    if RST = '1' then
      COUNT <= START;
    end if;

  end process;

end architecture RTL;
