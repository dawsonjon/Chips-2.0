--name: ConsoleOut
--tag: core
--tag: console
--input: in1
--source_file: built_in

---Console out
---===========
---Write a stream of data to the console

entity ConsoleOut is

  port(
    CLK     : std_logic;
    RST     : std_logic;
   
    IN1     : in std_logic_vector;
    IN1_STB : in std_logic;
    IN1_ACK : out std_logic
  );

end entity ConsoleOut;

architecture RTL of ConsoleOut is
  signal S_IN1_ACK;
begin

  process
    variable OUTPUT_LINE : line;
    variable INT  : integer;
    variable CHAR : character;
  begin
    wait until rising_edge(CLK);
    S_IN1_ACK <= '0';
    if IN1_STB = '1' and S_IN1_ACK = '0' then
      INT := (to_integer(unsigned(IN1)));
      CHAR := character'val (INT);
      if INT = 10 then
        writeline(output, OUTPUT_LINE);
      else
        write(OUTPUT_LINE, CHAR);
      end if;
      S_IN1_ACK <= '1';
    end if;
  end process;
  IN1_ACK <= S_IN1_ACK;

end RTL;
