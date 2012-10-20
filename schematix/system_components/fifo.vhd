--name: fifo
--tag: memory
--input: in1
--output: out1
--source_file: built_in
--parameter:depth:1024

---FIFO
---====
---Store up to *depth* data items.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity FIFO is
    generic(
        DEPTH : integer
    );
    port(
        CLK      : in std_logic;
        RST      : in std_logic;
        IN1      : in std_logic_vector(15 downto 0);
        IN1_STB  : in std_logic;
        IN1_ACK  : out std_logic;
        OUT1     : out std_logic_vector(15 downto 0);
        OUT1_STB : out std_logic;
        OUT1_ACK : in std_logic
    );
end entity FIFO;

architecture RTL of FIFO is

    type MEMORY_TYPE is array (0 to DEPTH - 1) of std_logic_vector(15 downto 0);
    signal MEMORY : MEMORY_TYPE;

    signal FILL : integer range 0 to DEPTH;
    signal INPOINTER, OUTPOINTER : integer range 0 to DEPTH -1;
    signal FULL, EMPTY : std_logic;
    signal WRITE, READ : std_logic;

begin

  EMPTY <= '1' when
    FILL = 0 else
      '0';

  FULL <= '1' when
    FILL = DEPTH else
      '0';

  WRITE <= '1' when
    IN1_STB = '1' and FULL = '0' else
     '0';

  READ <= '1' when 
    OUT1_ACK = '1' else
     '0';


  ACCESS_MEMORY : process(CLK)
  begin
    if rising_edge(CLK) then
      if WRITE = '1' then
        MEMORY(INPOINTER) <= IN1;
      end if;
      OUT1 <= MEMORY(OUTPOINTER);
    end if;
  end process ACCESS_MEMORY;

  FIFO_CONTROL : process
  begin

    wait until rising_edge(CLK);

    IN1_ACK <= '0';
    if WRITE = '1' then
      if INPOINTER = DEPTH - 1 then
        INPOINTER <= 0;
      else
        INPOINTER <= INPOINTER + 1;
      end if;
      IN1_ACK <= '1';
    end if;

    if EMPTY = '0' then
      OUT1_STB <= '1';
    end if;

    if READ = '1' then
      if OUTPOINTER = DEPTH - 1 then
        OUTPOINTER <= 0;
      else
        OUTPOINTER <= OUTPOINTER + 1;
      end if;
      --The memory will take a clock cycle to read the new data
      --so disable the strobe for now.
      OUT1_STB <= '0';
    end if;

    if WRITE = '1' and READ = '0' then
      FILL <= FILL + 1;
    elsif READ = '1' and WRITE = '0' then
      FILL <= FILL - 1;
    end if;

    if RST = '1' then
      INPOINTER <= 0;
      OUTPOINTER <= 0;
      FILL <= 0;
      OUT1_STB <= '0';
    end if;
  end process FIFO_CONTROL;

end architecture RTL;
