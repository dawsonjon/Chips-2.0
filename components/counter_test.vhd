--name: counter_test
--source_file: counter_test.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter_test is
end entity counter_test;

architecture RTL of counter_test is

--dependency: console_output
  component console_output is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector;
    in1_STB : in std_logic;
    in1_ACK : out std_logic
  );
  end component console_output;

--dependency: counter
  component counter is
    generic(
    start : integer := 0;
    step : integer := 1;
    stop : integer := 10    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component counter;

  signal signal_0 : std_logic_vector(15 downto 0);
  signal signal_0_STB : std_logic;
  signal signal_0_ACK : std_logic;
  signal CLK : std_logic;
  signal RST : std_logic;
begin

GENERATE_CLK : process
begin
  while True loop
    CLK <= '0';
    wait for 5 ns;
    CLK <= '1';
    wait for 5 ns;
  end loop;
  wait;
end process GENERATE_CLK;

GENERATE_RST : process
begin
  RST <= '1';
  wait for 50 ns;
  RST <= '0';
  wait;
end process GENERATE_RST;

  console_output_inst_1 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_0,
    in1_STB => signal_0_STB,
    in1_ACK => signal_0_ACK
  );
  counter_inst_0 : counter
  generic map(
    start => 0,
    step => 2,
    stop => 20
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_0,
    out1_STB => signal_0_STB,
    out1_ACK => signal_0_ACK
  );
end architecture RTL;
