--output: port_2
--input: port_1
--name: blah
--source_file: blah.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity blah is
  port(
    CLK : in std_logic;
    RST : in std_logic;
    port_1 : in std_logic_vector;
    port_1_STB : in std_logic;
    port_1_ACK : out std_logic;
    port_2 : out std_logic_vector;
    port_2_STB : out std_logic;
    port_2_ACK : in std_logic  );
end entity blah;

architecture RTL of blah is

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

  signal signal_0 : std_logic_vector(15 downto 0);
  signal signal_0_STB : std_logic;
  signal signal_0_ACK : std_logic;
  signal signal_1 : std_logic_vector(15 downto 0);
  signal signal_1_STB : std_logic;
  signal signal_1_ACK : std_logic;
begin

  inst_3 : console_output port map (
    CLK => CLK,
    RST => RST,
    in1 => port_1,
    in1_STB => port_1_STB,
    in1_ACK => port_1_ACK
  );
  inst_2 : constant_value generic map(
    value => 10)
port map (
    CLK => CLK,
    RST => RST,
    out1 => port_2,
    out1_STB => port_2_STB,
    out1_ACK => port_2_ACK
  );
end architecture RTL;
