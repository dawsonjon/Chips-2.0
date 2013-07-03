//name: modulo
//tag: arithmetic
//input: in1: bits
//input: in2: bits
//output: out1: bits
//parameter: bits: 16
//source_file: built_in


module modulo #( parameter bits=16 )(
    input clk,
    input rst,
    
    input [bits-1:0] in1,
    input in1_stb,
    output reg in1_ack,

    input [bits-1:0] in2,
    input in2_stb,
    output reg in2_ack,

    output reg [bits-1:0] out1,
    output reg out1_stb,
    input out1_ack
  );

  localparam msb = bits-1;
  localparam read_a_b = 2'd0;
  localparam modulo_1 = 2'd1;
  localparam modulo_2 = 2'd2;
  localparam write_z  = 2'd3;

  reg [1:0] state;
  reg [msb:0] a;
  reg [msb:0] b;
  reg [msb:0] modulo;
  reg [msb:0] shifter;
  reg [msb:0] remainder;
  reg count      : integer range 0 to bits;
  reg sign;


begin

  always @(posedge clk)
  begin
    case(state)

        read_a_b:
	begin
	  in1_ack <= 1'b1;
	  in2_ack <= 1'b1;
          if (in1_stb && in2_stb && in1_ack && in2_ack) begin
            a <= abs(in1);
            b <= abs(in2);
            sign <= IN1(MSB-1) xor IN2(MSB-1);
            in1_ack <= '1';
            in1_ack <= '1';
            STATE <= modulo_1;
          end
	end

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
