--name: fifo_test
--source_file: fifo_test.sch
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity fifo_test is
end entity fifo_test;

architecture RTL of fifo_test is

--dependency: bend
  component bend is
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector(15 downto 0);
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component bend;

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

--dependency: counter
  component counter is
    generic(
    start : integer := 0;
    step : integer := 1;
    stop : integer := 10    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component counter;

--dependency: fifo
  component fifo is
    generic(
    depth : integer := 1024    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    in1 : in std_logic_vector(15 downto 0);
    in1_STB : in std_logic;
    in1_ACK : out std_logic;
    out1 : out std_logic_vector(15 downto 0);
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component fifo;

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

  bend_inst_11 : bend
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_3,
    in1_STB => signal_3_STB,
    in1_ACK => signal_3_ACK,
    out1 => signal_4,
    out1_STB => signal_4_STB,
    out1_ACK => signal_4_ACK
  );

  bend_inst_10 : bend
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_2,
    out1_STB => signal_2_STB,
    out1_ACK => signal_2_ACK,
    in1 => signal_4,
    in1_STB => signal_4_STB,
    in1_ACK => signal_4_ACK
  );

  bend_inst_9 : bend
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_1,
    in1_STB => signal_1_STB,
    in1_ACK => signal_1_ACK,
    out1 => signal_5,
    out1_STB => signal_5_STB,
    out1_ACK => signal_5_ACK
  );

  bend_inst_8 : bend
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_0,
    in1_STB => signal_0_STB,
    in1_ACK => signal_0_ACK,
    out1 => signal_1,
    out1_STB => signal_1_STB,
    out1_ACK => signal_1_ACK
  );

  console_output_inst_0 : console_output
  port map (
    CLK => CLK,
    RST => RST,
    in1 => signal_2,
    in1_STB => signal_2_STB,
    in1_ACK => signal_2_ACK
  );

  counter_inst_7 : counter
  generic map(
    start => 0,
    step => 1,
    stop => 10
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_0,
    out1_STB => signal_0_STB,
    out1_ACK => signal_0_ACK
  );

  fifo_inst_6 : fifo
  generic map(
    depth => 1024
  )
  port map (
    CLK => CLK,
    RST => RST,
    out1 => signal_3,
    out1_STB => signal_3_STB,
    out1_ACK => signal_3_ACK,
    in1 => signal_5,
    in1_STB => signal_5_STB,
    in1_ACK => signal_5_ACK
  );

end architecture RTL;
