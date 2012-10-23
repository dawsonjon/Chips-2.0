--name: device_pin_input
--tag: sources
--output: out1 : bits
--parameter: bits:16
--source_file: built_in
--device_in: input_port : bits

---Device Pin Input
---================
---

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity device_pin_input is

  generic(
    BITS : integer
  );
  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    INPUT_PORT  : in  std_logic_vector(BITS-1 downto 0);
   
    OUT1        : out std_logic_vector(BITS-1 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity device_pin_input;

architecture RTL of device_pin_input is

  signal REG : std_logic;

begin

  process
  begin
    wait until rising_edge(CLK);
    REG <= INPUT_PORT;
    OUT1 <= REG;
    OUT1_STB <= '1';
  end process;

end architecture RTL;
