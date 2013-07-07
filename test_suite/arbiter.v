//name : arbiter
//tag : c components
//input : input_a:16
//input : input_b:16
//output : output_z:16
//source_file : test.c
///Arbiter
///=======
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module arbiter(input_a,input_b,input_a_stb,input_b_stb,output_z_ack,clk,rst,output_z,output_z_stb,input_a_ack,input_b_ack);
  input     [15:0] input_a;
  input     [15:0] input_b;
  input     input_a_stb;
  input     input_b_stb;
  input     output_z_ack;
  input     clk;
  input     rst;
  output    [15:0] output_z;
  output    output_z_stb;
  output    input_a_ack;
  output    input_b_ack;
  reg       [15:0] timer;
  reg       [13:0] program_counter;
  reg       [15:0] address;
  reg       [15:0] data_out;
  reg       [15:0] data_in;
  reg       write_enable;
  reg       [15:0] register_0;
  reg       [15:0] register_1;
  reg       [15:0] register_2;
  reg       [15:0] s_output_z_stb;
  reg       [15:0] s_output_z;
  reg       [15:0] s_input_a_ack;
  reg       [15:0] s_input_b_ack;
  reg       [15:0] a;
  reg       [15:0] b;
  reg       [15:0] z;
  reg       [15:0] divisor;
  reg       [15:0] dividend;
  reg       [15:0] quotient;
  reg       [15:0] remainder;
  reg       [15:0] modulo;
  reg       mod_sign;
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
  reg [15:0] memory [-1:0];

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
        program_counter <= 16'd2;
        register_0 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_2 <= 16'd0;
        register_2[0] <= input_a_stb;
      end

      16'd3:
      begin
        if (register_2 == 16'h0000)
          program_counter <= 7;
      end

      16'd4:
      begin
        register_2 <= input_a;
        program_counter <= 4;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd5;
        end
      end

      16'd5:
      begin
        s_output_z <= register_2;
        program_counter <= 5;
        s_output_z_stb <= 1'b1;
        if (s_output_z_stb == 1'b1 && output_z_ack == 1'b1) begin
          s_output_z_stb <= 1'b0;
          program_counter <= 6;
        end
      end

      16'd6:
      begin
        program_counter <= 16'd7;
      end

      16'd7:
      begin
        register_2 <= 16'd0;
        register_2[0] <= input_b_stb;
      end

      16'd8:
      begin
        if (register_2 == 16'h0000)
          program_counter <= 12;
      end

      16'd9:
      begin
        register_2 <= input_b;
        program_counter <= 9;
        s_input_b_ack <= 1'b1;
       if (s_input_b_ack == 1'b1 && input_b_stb == 1'b1) begin
          s_input_b_ack <= 1'b0;
          program_counter <= 16'd10;
        end
      end

      16'd10:
      begin
        s_output_z <= register_2;
        program_counter <= 10;
        s_output_z_stb <= 1'b1;
        if (s_output_z_stb == 1'b1 && output_z_ack == 1'b1) begin
          s_output_z_stb <= 1'b0;
          program_counter <= 11;
        end
      end

      16'd11:
      begin
        program_counter <= 16'd12;
      end

      16'd12:
      begin
        program_counter <= 16'd2;
      end

      16'd13:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
      stb <= 1'b0;
    end
  end
  assign input_a_ack = s_input_a_ack;
  assign input_b_ack = s_input_b_ack;
  assign output_z_stb = s_output_z_stb;
  assign output_z = s_output_z;

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
        mod_sign  <= divisor[15];
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
        modulo <= mod_sign?-(remainder/2):(remainder/2);
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
