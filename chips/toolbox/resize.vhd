--name: resizer
--tag: logic
--input: in1 : input_bits
--output: out1 : output_bits
--parameter:input_bits:16
--parameter:output_bits:16
--source_file: built_in

---Resizer
---=======
---
---Produces a stream of data *out1* by resizing *in1* item by item.
---
---Interface
------------
---:input: in1 - input stream of numbers to be resized
---:output: out1 - output stream containing resized data
---:parameter: input_bits - the width of in1 in *bits*
---:parameter: output_bits - the width of out1 in *bits*
---
---Usage
--------
---Both *in1* is treated as a signed number. If *output_bits* is greater than
---*input_bits* then *in1* will be sign extended. If *input_bits* is greater 
---than *output_bits* then *in1* will be truncated.
---

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity resizer is

  generic(
    INPUT_BITS : integer;
    OUTPUT_BITS : integer
  );
  port(
    CLK         : in  std_logic;
    RST         : in  std_logic;
    
    IN1         : in  std_logic_vector(INPUT_BITS-1 downto 0);
    IN1_STB     : in  std_logic;
    IN1_ACK     : out std_logic;

    OUT1        : out std_logic_vector(OUTPUT_BITS-1 downto 0);
    OUT1_STB    : out std_logic;
    OUT1_ACK    : in  std_logic
  );

end entity resizer;

architecture RTL of resizer is

  type STATE_TYPE is (READ_A, WRITE_Z);
  signal STATE      : STATE_TYPE;

begin

  process
  begin
    wait until rising_edge(CLK);
      case STATE is

      when READ_A =>
        if IN1_STB = '1' then
          IN1_ACK <= '1';
          OUT1_STB <= '1';
          OUT1 <= std_logic_vector(resize(signed(IN1), OUTPUT_BITS));
          STATE <= WRITE_Z;
        end if;

      when WRITE_Z =>
        IN1_ACK <= '0';
        if OUT1_ACK = '1' then
          OUT1_STB <= '0';
          STATE <= READ_A;
        end if;

    end case;
    if RST = '1' then
      STATE <= READ_A;
      IN1_ACK <= '0';
      OUT1_STB <= '0';
    end if;
  end process;

end architecture RTL;
