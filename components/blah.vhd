--name: blah
--source_file: blah.sch
--output: port_2
--input: port_1
entity blah is
  port(
--device_out: inst_1_tx : 1
--device_in: inst_0_rx : 1
    CLK : in std_logic;
    RST : in std_logic;
    inst_1_tx : out std_logic;
    inst_0_rx : in std_logic;
    port_1 : in std_logic_vector;
    port_1_STB : in std_logic;
    port_1_ACK : out std_logic;
    port_2 : out std_logic_vector;
    port_2_STB : out std_logic;
    port_2_ACK : in std_logic);
end entity blah;

architecture RTL of blah

--dependency: SerialOut
  component SerialOut is
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
  end component SerialOut;

--dependency: SerialIn
  component SerialIn is
    generic(
    baud_rate : integer := 115200;
    clock_frequency : integer := 100000000    );
    port(
    CLK : in std_logic;
    RST : in std_logic;
    rx : in std_logic;
    out1 : out std_logic_vector;
    out1_STB : out std_logic;
    out1_ACK : in std_logic
  );
  end component SerialIn;

  signal signal_0 : std_logic_vector(15 downto 0);
  signal signal_1 : std_logic_vector(15 downto 0);
begin

  inst_1 : SerialOut generic map(
    baud_rate => 115200,
    clock_frequency => 100000000
  ) port map (
    CLK => CLK,
    RST => RST,
    tx => inst_1_tx,
    in1 => port_1,
    in1_STB => port_1_STB,
    in1_ACK => port_1_ACK
  );
  inst_0 : SerialIn generic map(
    baud_rate => 115200,
    clock_frequency => 100000000
  ) port map (
    CLK => CLK,
    RST => RST,
    rx => inst_0_rx,
    out1 => port_2,
    out1_STB => port_2_STB,
    out1_ACK => port_2_ACK
  );
end architecture RTL;
