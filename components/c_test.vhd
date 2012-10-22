--name : c_test
--tag : c components
--input : i
--output : z
--source_file : /media/sdb1/Projects/Schematix/components/c_test.c
---C_Test
---======
---
---*Created by C2VHDL*

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity c_test is
  port(
    CLK : in std_logic;
    RST : in std_logic;
    INPUT_I : in std_logic_vector(15 downto 0);
    INPUT_I_STB : in std_logic;
    OUTPUT_Z_ACK : in std_logic;
    OUTPUT_Z : out std_logic_vector(15 downto 0);
    OUTPUT_Z_STB : out std_logic;
    INPUT_I_ACK : out std_logic);
end entity c_test;

architecture RTL of c_test is

  function ADD(A:signed; B:signed) return signed is
  begin
    return resize(A + B, 16);
  end function;

  function LE(A:signed; B:signed) return signed is
  begin
    if A <= B then
      return X"0001";
    else
      return X"0000";
    end if;
  end function;

  signal PROGRAM_COUNTER : integer range 0 to 13;
  signal REGISTER_0: signed(15 downto 0);--c_test return address
  signal REGISTER_1: signed(15 downto 0);--c_test return value
  signal REGISTER_2: signed(15 downto 0);--variable i
  signal REGISTER_3: signed(15 downto 0);--temporary_register
  signal REGISTER_4: signed(15 downto 0);--temporary_register
  signal REGISTER_5: signed(15 downto 0);--temporary_register
  signal REGISTER_6: signed(15 downto 0);--temporary_register
  signal STOP : boolean := False;
  signal TIMER : signed(15 downto 0);
  signal S_OUTPUT_Z_STB : std_logic;
  signal S_INPUT_I_ACK : std_logic;

begin

  EXECUTE : process
  begin
    wait until rising_edge(CLK);
    PROGRAM_COUNTER <= PROGRAM_COUNTER + 1;
    TIMER <= X"0000";
    case PROGRAM_COUNTER is
      when 0 =>
        PROGRAM_COUNTER <= 2;
        REGISTER_0 <= to_signed(1, 16);
      when 1 =>
        STOP <= True;
        PROGRAM_COUNTER <= PROGRAM_COUNTER;
      when 2 =>
        REGISTER_2 <= to_signed(0, 16);
        REGISTER_3 <= to_signed(0, 16);
      when 3 =>
        REGISTER_2 <= REGISTER_3;
      when 4 =>
        REGISTER_4 <= REGISTER_2;
      when 5 =>
        REGISTER_4 <= LE(REGISTER_4, to_signed(10, 16));
      when 6 =>
        if REGISTER_4 = X"0000" then
          PROGRAM_COUNTER <= 12;
        end if;
      when 7 =>
        REGISTER_5 <= signed(INPUT_i);
        PROGRAM_COUNTER <= 7;
        S_INPUT_i_ACK <= '1';
        if S_INPUT_i_ACK = '1' and INPUT_i_STB = '1' then
          S_INPUT_i_ACK <= '0';
          PROGRAM_COUNTER <= 8;
        end if;
      when 8 =>
        OUTPUT_z <= std_logic_vector(REGISTER_5);
        PROGRAM_COUNTER <= 8;
        S_OUTPUT_z_STB <= '1';
        if S_OUTPUT_z_STB = '1' and OUTPUT_z_ACK = '1' then
          S_OUTPUT_z_STB <= '0';
          PROGRAM_COUNTER <= 9;
        end if;
      when 9 =>
        REGISTER_6 <= REGISTER_2;
      when 10 =>
        REGISTER_6 <= ADD(REGISTER_6, to_signed(1, 16));
      when 11 =>
        REGISTER_2 <= REGISTER_6;
        PROGRAM_COUNTER <= 4;
      when 12 =>
        REGISTER_1 <= to_signed(0, 16);
        PROGRAM_COUNTER <= to_integer(REGISTER_0);
      when others => null;
    end case;
    if RST = '1' then
      PROGRAM_COUNTER <= 0;
      S_OUTPUT_Z_STB <= '0';
      S_INPUT_I_ACK <= '0';
    end if;
  end process EXECUTE;
  OUTPUT_Z_STB <= S_OUTPUT_Z_STB;
  INPUT_I_ACK <= S_INPUT_I_ACK;

end RTL;
