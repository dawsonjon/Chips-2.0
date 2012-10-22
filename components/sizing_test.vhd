--name: sizing_test
--source_file: sizing_test.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sizing_test is
end entity sizing_test;

architecture RTL of sizing_test is

--dependency: console_output
  component console_output is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector(15 downto 0);
    in1_STB : in std_logic;
    in1_ACK : out std_logic
  );
  end component console_output;

--dependency: adder
  component adder is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector(15 downto 0);
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    in2 : in std_logic_vector(15 downto 0);
    in2_STB : in std_logic;
    in2_ACK : out std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component adder;

--dependency: constant_value_8
  component constant_value_8 is
    generic(
    value : integer := 0    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component constant_value_8;

--dependency: constant_value_16
  component constant_value_16 is
    generic(
    value : integer := 0    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component constant_value_16;

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
  signal signal_5 : std_logic_vector(15 downto 0);
  signal signal_5_STB : std_logic;
  signal signal_5_ACK : std_logic;
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

  console_output_inst_12 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_5,
    in1_STB => signal_5_STB,
    in1_ACK => signal_5_ACK
  );

  adder_inst_11 : adder
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_3,
    in1_STB => signal_3_STB,
    in1_ACK => signal_3_ACK,
    in2 => signal_4,
    in2_STB => signal_4_STB,
    in2_ACK => signal_4_ACK,
    out1 => signal_5,
    out1_STB => signal_5_STB,
    out1_ACK => signal_5_ACK
  );

  constant_value_8_inst_10 : constant_value_8
  generic map(
    value => 0
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_4,
    out1_STB => signal_4_STB,
    out1_ACK => signal_4_ACK
  );

  constant_value_8_inst_9 : constant_value_8
  generic map(
    value => 0
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_3,
    out1_STB => signal_3_STB,
    out1_ACK => signal_3_ACK
  );

  adder_inst_2 : adder
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

  constant_value_16_inst_1 : constant_value_16
  generic map(
    value => 10
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_1,
    out1_STB => signal_1_STB,
    out1_ACK => signal_1_ACK
  );

  constant_value_16_inst_0 : constant_value_16
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

  console_output_inst_4 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_2,
    in1_STB => signal_2_STB,
    in1_ACK => signal_2_ACK
  );

end architecture RTL;
