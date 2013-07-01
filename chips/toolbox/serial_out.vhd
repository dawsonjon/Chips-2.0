--name: serial_output
--tag: sinks
--input: in1 : 8
--source_file: built_in
--device_out: BIT: TX : port_name : 1
--parameter: clock_frequency : 100000000
--parameter: baud_rate : 115200
--parameter: port_name : "TX"

---Serial Output
---=============
---
---Write a stream of data to a serial UART

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity serial_output is

  generic(
    CLOCK_FREQUENCY : integer;
    BAUD_RATE       : integer;
    PORT_NAME       : string
  );
  port(
    CLK     : in std_logic;
    RST     : in  std_logic;
    TX      : out std_logic;
   
    IN1     : in std_logic_vector(7 downto 0);
    IN1_STB : in std_logic;
    IN1_ACK : out std_logic
  );

end entity serial_output;

architecture RTL of serial_output is

  constant CLOCK_DIVIDER : Unsigned(11 downto 0) := To_unsigned(CLOCK_FREQUENCY/BAUD_RATE, 12);
  signal BAUD_COUNT      : Unsigned(11 downto 0);
  signal DATA            : std_logic_vector(7 downto 0);
  signal X16CLK_EN       : std_logic;
  signal S_IN1_ACK       : std_logic;

  type STATE_TYPE is (IDLE, START, WAIT_EN, TX0, TX1, TX2, TX3, TX4, TX5, TX6, TX7, STOP);
  signal STATE         : STATE_TYPE;

begin

  process
  begin
    wait until rising_edge(CLK);
    if BAUD_COUNT = CLOCK_DIVIDER then
      BAUD_COUNT <= (others => '0');
      X16CLK_EN  <= '1';
    else
      BAUD_COUNT <= BAUD_COUNT + 1;
      X16CLK_EN  <= '0';
    end if;
    if RST = '1' then
      BAUD_COUNT <= (others => '0');
      X16CLK_EN  <= '0';
    end if;
  end process;

  process
  begin
    wait until rising_edge(CLK);
    case STATE is
      when IDLE =>
        if IN1_STB = '1'  then
          DATA <= std_logic_vector(RESIZE(unsigned(IN1), 8));
          STATE     <= WAIT_EN;
        end if;
      when WAIT_EN =>
        if X16CLK_EN = '1' then
          STATE <= START;
        end if;
      when START =>
        if X16CLK_EN = '1' then
          STATE <= TX0;
        end if;
        TX <= '0'; 
      when TX0 =>
        if X16CLK_EN = '1' then
          STATE <= TX1;
        end if;
        TX <= DATA(0);
      when TX1 =>
        if X16CLK_EN = '1' then
          STATE <= TX2;
        end if;
        TX <= DATA(1);
      when TX2 =>
        if X16CLK_EN = '1' then
          STATE <= TX3;
        end if;
        TX <= DATA(2);
      when TX3 =>
        if X16CLK_EN = '1' then
          STATE <= TX4;
        end if;
        TX <= DATA(3);
      when TX4 =>
        if X16CLK_EN = '1' then
          STATE <= TX5;
        end if;
        TX <= DATA(4);
      when TX5 =>
        if X16CLK_EN = '1' then
          STATE <= TX6;
        end if;
        TX <= DATA(5);
      when TX6 =>
        if X16CLK_EN = '1' then
          STATE <= TX7;
        end if;
        TX <= DATA(6);
      when TX7 =>
        if X16CLK_EN = '1' then
          STATE <= STOP;
        end if;
        TX <= DATA(7);
      when STOP =>
        if X16CLK_EN = '1' then
          STATE <= IDLE;
        end if;
        TX <= '1';
      when others =>
        STATE <= IDLE;
      end case;
    if RST = '1' then
      STATE <= IDLE;
      TX <= '0';
    end if; 
  end process;

  IN1_ACK <= '1' when STATE=IDLE else '0';

end architecture RTL;
