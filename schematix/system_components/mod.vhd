--name: modulo
--tag: arithmetic
--input: in1: bits
--input: in2: bits
--output: out1: bits
--parameter: bits: 16
--source_file: built_in

---modulo
---======
---
---Produces a stream of data *out1* by dividing *in1* by *in2* item by item.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity modulo is

  generic(
    BITS : integer
  );
  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    
    IN1         : in  std_logic_vector(BITS-1 downto 0);
    IN1_STB     : in  std_logic;
    IN1_ACK     : out std_logic;

    IN2         : in  std_logic_vector(BITS-1 downto 0);
    IN2_STB     : in  std_logic;
    IN2_ACK     : out std_logic;

    OUT1        : out std_logic_vector(BITS-1 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity modulo;

architecture RTL of modulo is

  constant MSB : integer := BITS-1;
  type modulo_STATE_TYPE is (READ_A_B, modulo_1, modulo_2, WRITE_Z);

  signal STATE      : modulo_STATE_TYPE;
  signal A          : std_logic_vector(MSB downto 0);
  signal B          : std_logic_vector(MSB downto 0);
  signal MODULO     : std_logic_vector(MSB downto 0);
  signal SHIFTER    : std_logic_vector(MSB downto 0);
  signal REMAINDER  : std_logic_vector(MSB downto 0);
  signal COUNT      : integer range 0 to BITS;
  signal SIGN       : std_logic;


begin

  process
  begin
    wait until rising_edge(CLK);
      case STATE is

        when READ_A_B =>
          if IN1_STB = '1' and IN1_STB = '1' then
            A <= std_logic_vector(abs(resize(signed(IN1), BITS)));
            B <= std_logic_vector(abs(resize(signed(IN2), BITS)));
            SIGN <= IN1(MSB-1) xor IN2(MSB-1);
            IN1_ACK <= '1';
            IN2_ACK <= '1';
            STATE <= modulo_1;
          end if;

        when modulo_1 =>
          IN1_ACK <= '0';
          IN2_ACK <= '0';
          QUOTIENT <= (others => '0');
          SHIFTER <= (others => '0');
          SHIFTER(0) <= A(MSB);
          A <= A(MSB-1 downto 0) & '0';
          COUNT <= BITS;
          STATE <= modulo_2;

        when modulo_2 => --subtract
         --if SHIFTER - B is positive or zero
         if REMAINDER(MSB) = '0' then
           SHIFTER(MSB downto 1) <= REMAINDER(MSB-1 downto 0);
         else
           SHIFTER(MSB downto 1) <= SHIFTER(MSB-1 downto 0);
         end if;
         SHIFTER(0) <= A(MSB);
         A <= A(MSB-1 downto 0) & '0';
         QUOTIENT <= QUOTIENT(MSB-1 downto 0) & not(REMAINDER(MSB));
         if COUNT = 0 then
           STATE <= WRITE_Z;
         else
           COUNT <= COUNT - 1;
         end if;

      when WRITE_Z =>
         MODULO := unsigned(SHIFTER_2)/2;
         if SIGN = '1' then --if negative
           OUT1 <= std_logic_vector( 0 - MODULO);
         else
           OUT1 <= std_logic_vector( MODULO);
         end if;

        OUT1_STB <= '1';
        if OUT1_ACK = '1' then
          OUT1_STB <= '0';
          STATE <= READ_A_B;
        end if;

    end case;
    if RST = '1' then
      STATE <= READ_A_B;
      IN1_ACK <= '0';
      IN2_ACK <= '0';
      OUT1_STB <= '0';
    end if;
  end process;

  --subtractor
  REMAINDER <= std_logic_vector(unsigned(SHIFTER) - resize(unsigned(B), BITS));

end architecture RTL;
