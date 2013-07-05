//name : board_test
//tag : c components
//output : OUTPUT_serial:16
//source_file : ./board_test.c
///Board_Test
///==========
///
///*Created by C2CHIP*

module board_test(output_serial_ack,clk,rst,output_serial,output_serial_stb);
  input     [15:0] output_serial_ack;
  input     clk;
  input     rst;
  output    [15:0] output_serial;
  output    [15:0] output_serial_stb;
  reg       [15:0] timer;
  reg       [22:0] program_counter;
  reg       [15:0] address;
  reg       [15:0] data_out;
  reg       [15:0] data_in;
  reg       write_enable;
  reg       [15:0] register_0;
  reg       [15:0] register_1;
  reg       [15:0] register_2;
  reg       [15:0] register_3;
  reg       [15:0] register_4;
  reg       [15:0] register_5;
  reg       [15:0] register_6;
  reg       [15:0] register_7;
  reg       [15:0] s_output_serial_stb;
  reg       [15:0] s_output_serial;
  reg       [15:0] a;
  reg       [15:0] b;
  reg       [15:0] z;
  reg       [15:0] divisor;
  reg       [15:0] dividend;
  reg       [15:0] quotient;
  reg       [15:0] remainder;
  reg       [4:0] count;
  reg       [1:0] state;
  reg       stb;
  reg       ack;
  reg       sign;
  wire      [15:0] difference;
  parameter [1:0] start= 2'd0;
  parameter [1:0] calculate= 2'd1;
  parameter [1:0] finish= 2'd2;
  parameter [1:0] acknowledge= 2'd3;
  reg [15:0] memory [4:0];

  //////////////////////////////////////////////////////////////////////////////
  // FSM IMPLEMENTAION OF C PROCESS                                             
  //                                                                            
  // This section of the file contains a Finite State Machine (FSM) implementing
  // the C process. In general execution is sequential, but the compiler will   
  // attempt to execute instructions in parallel if the instruction dependencies
  // allow. Further concurrency can be achieved by executing multiple C         
  // processes concurrently within the device.                                  
  
  always @(posedge clk)
  begin

    if (write_enable == 1'b1) begin
      memory[address] <= data_in;
    end

    data_out <= memory[address];
    write_enable <= 1'b0;
    program_counter <= program_counter + 1;
    timer <= 16'h0000;

    case(program_counter)

      16'd0:
      begin
        program_counter <= 16'd20;
        register_4 <= 16'd1;
      end

      16'd1:
      begin
        $finish;
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_3 <= 16'd0;
      end

      16'd3:
      begin
        register_7 <= register_3;
      end

      16'd4:
      begin
        register_7 <= $signed(register_7) + $signed(register_2);
      end

      16'd5:
      begin
        address <= register_7;
      end

      16'd6:
      begin
        register_7 <= data_out;
      end

      16'd7:
      begin
        register_7 <= data_out;
      end

      16'd8:
      begin
        if (register_7 == 16'h0000)
          program_counter <= 17;
      end

      16'd9:
      begin
        register_7 <= register_3;
      end

      16'd10:
      begin
        register_7 <= $signed(register_7) + $signed(16'd1);
      end

      16'd11:
      begin
        register_3 <= register_7;
        register_7 <= $signed(register_7) + $signed(register_2);
      end

      16'd12:
      begin
        address <= register_7;
      end

      16'd13:
      begin
        register_7 <= data_out;
      end

      16'd14:
      begin
        register_7 <= data_out;
      end

      16'd15:
      begin
        s_output_serial <= register_7;
        program_counter <= 15;
        s_output_serial_stb <= 1'b1;
        if (s_output_serial_stb == 1'b1 && output_serial_ack == 1'b1) begin
          s_output_serial_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        program_counter <= 16'd18;
      end

      16'd17:
      begin
        program_counter <= 16'd19;
      end

      16'd18:
      begin
        program_counter <= 16'd3;
      end

      16'd19:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

      16'd20:
      begin
        register_6 <= 16'd0;
      end

      16'd21:
      begin
        register_2 <= register_6;
        program_counter <= 16'd2;
        register_0 <= 16'd22;
      end

      16'd22:
      begin
        register_7 <= register_1;
        register_5 <= 16'd0;
        program_counter <= register_4;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
      stb <= 1'b0;
    end
  end
  assign output_serial_stb = s_output_serial_stb;
  assign output_serial = s_output_serial;

  //////////////////////////////////////////////////////////////////////////////
  // SERIAL DIVIDER                                                             
  //                                                                            
  // The C input file uses division.                                            
  // Division is not directly synthesisable in target hardware.                 
  // This section of the file implements a serial divider.                      
  // At present, there is no support for concurrent division at instruction     
  // level. The division operation takes 18 clock cycles. You should consider   
  // re-writing the C source file to avoid division if performance is not       
  // accepteable.                                                               

  always @(posedge clk)
  begin

    ack <= 1'b0;

    case (state)

      start: begin

        a <= divisor[15]?-divisor:divisor;
        b <= dividend[15]?-dividend:dividend;
        remainder <= 15'd0;
        z <= 15'd0;
        sign  <= divisor[15] ^ dividend[15];
        count <= 5'd16;

        if( stb == 1'b1 ) begin
          state <= calculate;
        end

      end //start

      calculate: begin

        if( difference[15] == 0 ) begin //if remainder > b
          z <= z * 2 + 1;
          remainder <= {difference[14:0], a[15]};
        end else begin
          z <= z * 2;
          remainder <= {remainder[14:0], a[15]};
        end

        a <= a * 2;
        if( count == 5'd0 ) begin
          state <= finish;
        end else begin
          count <= count - 1;
        end

      end //calculate

      finish: begin

        quotient <= sign?-z:z;
        ack      <= 1'b1;
        state    <= acknowledge;

      end //finish

      acknowledge: begin

        ack      <= 1'b0;
        state    <= start;

      end //wait

    endcase

    if( rst == 1'b1 ) begin
      ack   <= 1'b0;
      state <= start;
    end //if
  end

  assign difference = remainder - b;


endmodule
