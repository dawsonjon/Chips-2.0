--name: ram
--tag: memory
--input: write_address: bits
--input: write_data: bits
--input: read_address: bits
--output: read_data: bits
--source_file: built_in
--parameter:depth:1024
--parameter:bits:16

---Memory
---======
---Store up to *depth* data items.
---
---Interface
------------
---:input: write_address - address to write data to
---:input: write_data - data to write
---:input: read_address - address to read from
---:output: read_data - data read from memory
---
---:parameter: depth - The number of memory locations.
---:parameter: bits - The width in of the address and data busses in bits.
---
---Usage
--------
---
---To write data to a location in memory, first write the address via the
---*write_address* input, then write data via the *write_data* input.
---
---To read data from a location in memory, first write the address via the
---*read_address* input, then read data from the *read_data* output.
---
---Notes:
---
---+ *read_data* will block until an address is provided via *read_address*.
---+ *write_data* will block until an address is provided via *write_address*.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity RAM is
    generic(
        BITS  : integer;
        DEPTH : integer
    );
    port(
        CLK      : in std_logic;
        RST      : in std_logic;

        WRITE_ADDRESS      : in std_logic_vector(BITS-1 downto 0);
        WRITE_ADDRESS_STB  : in std_logic;
        WRITE_ADDRESS_ACK  : out std_logic;

        WRITE_DATA         : in std_logic_vector(BITS-1 downto 0);
        WRITE_DATA_STB     : in std_logic;
        WRITE_DATA_ACK     : out std_logic;

        READ_ADDRESS       : in std_logic_vector(BITS-1 downto 0);
        READ_ADDRESS_STB   : in std_logic;
        READ_ADDRESS_ACK   : out std_logic;

        READ_DATA          : out std_logic_vector(BITS-1 downto 0);
        READ_DATA_STB      : out std_logic;
        READ_DATA_ACK      : in std_logic
    );
end entity RAM;

architecture RTL of RAM is

  type READ_STATE_TYPE is (GET_ADDRESS, WAIT_READ, PUT_DATA);
  signal READ_STATE : READ_STATE_TYPE;
  type WRITE_STATE_TYPE is (GET_ADDRESS, GET_DATA);
  signal WRITE_STATE : WRITE_STATE_TYPE;

  type MEMORY_TYPE is array (0 to DEPTH - 1) of std_logic_vector(BITS-1 downto 0);
  signal MEMORY : MEMORY_TYPE;

begin

  WRITE_MEMORY : process
  begin
    wait until rising_edge(CLK);
    case WRITE_STATE is

      when GET_ADDRESS =>
        if WRITE_ADDRESS_STB = '1' then
          S_WRITE_ADDRESS <= WRITE_ADDRESS;
          WRITE_STATE <= GET_DATA;
        end if;

      when GET_DATA =>
        if WRITE_DATA_STB = '1' then
          MEMORY(to_integer(unsigned(S_WRITE_ADDRESS)) mod DEPTH) := WRITE_DATA;
          WRITE_STATE <= GET_ADDRESS;
        end if;

    end case;
    if RST = '1' then
      STATE <= GET_ADDRESS;
    end if;
  end process WRITE_MEMORY;
  WRITE_ADDRESS_ACK <= '1' when WRITE_STATE = GET_ADDRESS else '0';
  WRITE_DATA_ACK <= '1' when WRITE_STATE = GET_DATA else '0';

  READ_MEMORY : process
  begin
    wait until rising_edge(CLK);

    S_READ_DATA <= MEMORY(to_integer(unsigned(S_READ_ADDRESS) mod DEPTH);

    case READ_STATE is

      when GET_ADDRESS =>
        if READ_ADDRESS_STB = '1' then
          S_READ_ADDRESS <= READ_ADDRESS;
          READ_STATE <= WAIT_READ;
        end if;

      when WAIT_READ =>
        READ_STATE <= PUT_DATA;

      when PUT_DATA =>
        READ_DATA <= S_READ_DATA;
        if READ_DATA_ACK = '1' then
          READ_STATE <= GET_ADDRESS;
        end if;

    end case;
    if RST = '1' then
      STATE <= GET_ADDRESS;
    end if;
  end process READ_MEMORY;
  READ_ADDRESS_ACK <= '1' when READ_STATE = GET_ADDRESS else '0';
  READ_DATA_STB <= '1' when READ_STATE = PUT_DATA else '0';

end architecture RTL;
