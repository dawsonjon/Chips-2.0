--name: tee_16
--tag: schematic
--output: out1 : 16
--output: out2 : 16
--input: in1 : 16
--source_file: built_in

---16-bit Tee
---==========
---
---Used to represent a tee or join in a wire in schematix.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tee_16 is

  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    
    IN1         : in  std_logic_vector(15 downto 0);
    IN1_STB     : in  std_logic;
    IN1_ACK     : out std_logic;

    OUT1        : out std_logic_vector(15 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic;

    OUT2        : out std_logic_vector(15 downto 0);
    OUT2_STB    : out std_logic;
    OUT2_ACK    : in  std_logic
  );

end entity tee_16;

architecture RTL of tee_16 is

  type STATE_TYPE is (READ, WRITE_1, WRITE_2);
  signal STATE : STATE_TYPE;

begin

  process
  begin
    wait until rising_edge(CLK);
    case STATE is
      when READ =>
        if IN1_STB = '1' then
          STATE <= WRITE_1;
        end if;

      when WRITE_1 =>
        if OUT1_ACK = '1' then
          STATE <= WRITE_2;
        end if;

      when WRITE_2 =>
        if OUT2_ACK = '1' then
          STATE <= READ;
        end if;
    end case;
    if RST = '1' then
      STATE <= READ;
    end if;
  end process;

  IN1_ACK  <= '1' when STATE = READ else '0';
  OUT1_STB <= '1' when STATE = WRITE_1 else '0';
  OUT2_STB <= '1' when STATE = WRITE_2 else '0';

end architecture RTL;
