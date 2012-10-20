--name: divider_test
--source_file: divider_test.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity divider_test is
end entity divider_test;

architecture RTL of divider_test is

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

--dependency: constant_value
  component constant_value is
    generic(
    value : integer := 0    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component constant_value;

--dependency: divider
  component divider is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector;
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    in2 : in std_logic_vector;
    in2_STB : in std_logic;
    in2_ACK : out std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component divider;

  signal signal_0 : std_logic_vector(15 downto 0);
  signal signal_0_STB : std_logic;
  signal signal_0_ACK : std_logic;
  signal signal_1 : std_logic_vector(15 downto 0);
  signal signal_1_STB : std_logic;
  signal signal_1_ACK : std_logic;
  signal signal_2 : std_logic_vector(15 downto 0);
  signal signal_2_STB : std_logic;
  signal signal_2_ACK : std_logic;
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

  console_output_inst_3 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_2,
    in1_STB => signal_2_STB,
    in1_ACK => signal_2_ACK
  );
  constant_value_inst_2 : constant_value
  generic map(
    value => 4
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_1,
    out1_STB => signal_1_STB,
    out1_ACK => signal_1_ACK
  );
  constant_value_inst_1 : constant_value
  generic map(
    value => 24
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_0,
    out1_STB => signal_0_STB,
    out1_ACK => signal_0_ACK
  );
  divider_inst_0 : divider
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_0,
    in1_STB => signal_0_STB,
    in1_ACK => signal_0_ACK,
    in2 => signal_1,
    in2_STB => signal_1_STB,
    in2_ACK => signal_1_ACK,
    out1 => signal_2,
    out1_STB => signal_2_STB,
    out1_ACK => signal_2_ACK
  );
end architecture RTL;
