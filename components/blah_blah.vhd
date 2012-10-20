--name: blah_blah
--source_file: blah_blah.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity blah_blah is
end entity blah_blah;

architecture RTL of blah_blah is

--dependency: blah
  component blah is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    port_1 : in std_logic_vector;
    port_1_STB : in std_logic;
    port_1_ACK : out std_logic;
    port_2 : out std_logic_vector;
    port_2_STB : out std_logic;
    port_2_ACK : in std_logic
  );
  end component blah;

--dependency: bend
  component bend is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector;
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component bend;

  signal signal_0 : std_logic_vector(15 downto 0);
  signal signal_0_STB : std_logic;
  signal signal_0_ACK : std_logic;
  signal signal_1 : std_logic_vector(15 downto 0);
  signal signal_1_STB : std_logic;
  signal signal_1_ACK : std_logic;
  signal signal_2 : std_logic_vector(15 downto 0);
  signal signal_2_STB : std_logic;
  signal signal_2_ACK : std_logic;
  signal signal_3 : std_logic_vector(15 downto 0);
  signal signal_3_STB : std_logic;
  signal signal_3_ACK : std_logic;
  signal signal_4 : std_logic_vector(15 downto 0);
  signal signal_4_STB : std_logic;
  signal signal_4_ACK : std_logic;
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

  inst_10 : blah port map (
    CLK => CLK,
    RST => RST,
    port_1 => signal_3,
    port_1_STB => signal_3_STB,
    port_1_ACK => signal_3_ACK,
    port_2 => signal_4,
    port_2_STB => signal_4_STB,
    port_2_ACK => signal_4_ACK
  );
  inst_7 : bend port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_1,
    in1_STB => signal_1_STB,
    in1_ACK => signal_1_ACK,
    out1 => signal_2,
    out1_STB => signal_2_STB,
    out1_ACK => signal_2_ACK
  );
  inst_6 : bend port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_0,
    in1_STB => signal_0_STB,
    in1_ACK => signal_0_ACK,
    out1 => signal_1,
    out1_STB => signal_1_STB,
    out1_ACK => signal_1_ACK
  );
  inst_5 : bend port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_0,
    out1_STB => signal_0_STB,
    out1_ACK => signal_0_ACK,
    in1 => signal_4,
    in1_STB => signal_4_STB,
    in1_ACK => signal_4_ACK
  );
  inst_8 : bend port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_2,
    in1_STB => signal_2_STB,
    in1_ACK => signal_2_ACK,
    out1 => signal_3,
    out1_STB => signal_3_STB,
    out1_ACK => signal_3_ACK
  );
end architecture RTL;
