--device_out: inst_1_tx : 1
--name: test_suite
--source_file: test_suite.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity test_suite is
  port(
    inst_1_tx : out std_logic  );
end entity test_suite;

architecture RTL of test_suite is

--dependency: serial_output
  component serial_output is
    generic(
    baud_rate : integer := 115200;
    clock_frequency : integer := 100000000    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    tx : out std_logic;
    in1 : in std_logic_vector;
    in1_STB : in std_logic;
    in1_ACK : out std_logic
  );
  end component serial_output;

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

--dependency: tee
  component tee is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector;
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic;
    out2 : out std_logic_vector;
    out2_STB : out std_logic;
    out2_ACK : in std_logic
  );
  end component tee;

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

  serial_output_inst_1 : serial_output
  generic map(
    baud_rate => 115200,
    clock_frequency => 100000000
  )
  port map (
    CLK => CLK,
    RST => RST,
    tx => inst_1_tx,
    in1 => signal_1,
    in1_STB => signal_1_STB,
    in1_ACK => signal_1_ACK
  );
  bend_inst_21 : bend
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_2,
    in1_STB => signal_2_STB,
    in1_ACK => signal_2_ACK,
    out1 => signal_3,
    out1_STB => signal_3_STB,
    out1_ACK => signal_3_ACK
  );
  console_output_inst_18 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_3,
    in1_STB => signal_3_STB,
    in1_ACK => signal_3_ACK
  );
  constant_value_inst_19 : constant_value
  generic map(
    value => 10
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_0,
    out1_STB => signal_0_STB,
    out1_ACK => signal_0_ACK
  );
  tee_inst_20 : tee
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_0,
    in1_STB => signal_0_STB,
    in1_ACK => signal_0_ACK,
    out1 => signal_1,
    out1_STB => signal_1_STB,
    out1_ACK => signal_1_ACK,
    out2 => signal_2,
    out2_STB => signal_2_STB,
    out2_ACK => signal_2_ACK
  );
end architecture RTL;
