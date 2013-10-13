library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity CHECKSUM is
  port(
    CLK : in std_logic;
    RST : in std_logic;

    DATA_IN : in std_logic_vector(15 downto 0);
    DATA_IN_STB : in std_logic;
    DATA_IN_ACK : out std_logic;

    DATA_OUT : out std_logic_vector(15 downto 0);
    DATA_OUT_STB : out std_logic;
    DATA_OUT_ACK : in std_logic
  );
end entity CHECKSUM;

architecture RTL of CHECKSUM is

  type STATE_TYPE is (GET_LENGTH, GET_DATA, SEND_DATA);
  signal STATE : STATE_TYPE;

  signal LEN : std_logic_vector(15 downto 0);
  signal COUNT : integer range 0 to 65535;
  signal CHECKSUM : unsigned(31 downto 0);

  signal S_DATA_IN_ACK : std_logic;
  signal S_DATA_OUT_STB : std_logic;

begin

  process
  begin
    wait until rising_edge(CLK);
    case STATE is

      when GET_LENGTH =>

        S_DATA_IN_ACK <= '1';
        if S_DATA_IN_ACK = '1' and DATA_IN_STB = '1' then
          S_DATA_IN_ACK <= '0';
          LEN <= DATA_IN;
          STATE <= GET_DATA;
          COUNT <= 0;
        end if;

      when GET_DATA =>

        S_DATA_IN_ACK <= '1';
        if S_DATA_IN_ACK = '1' and DATA_IN_STB = '1' then
          S_DATA_IN_ACK <= '0';
          CHECKSUM <= CHECKSUM + resize(unsigned(DATA_IN), 32);
          if COUNT = unsigned(LEN) - 1 then
            STATE <= SEND_DATA;
          else
            COUNT <= COUNT + 1;
          end if;
        end if;

      when SEND_DATA =>

        S_DATA_OUT_STB <= '1';
        DATA_OUT <= not std_logic_vector(CHECKSUM(15 downto 0) + CHECKSUM(31 downto 16));
        if S_DATA_OUT_STB = '1' and DATA_OUT_ACk = '1' then
          S_DATA_OUT_STB <= '0';
          STATE <= GET_LENGTH;
        end if;

    end case;

    if RST = '1' then
      STATE <= GET_LENGTH;
      S_DATA_OUT_STB <= '1';
      S_DATA_IN_ACK <= '1';
    end if;

  end process;
  DATA_OUT_STB <= S_DATA_OUT_STB;
  DATA_IN_ACK <= S_DATA_IN_ACK;

end RTL;
