//name : seconds_count
//tag : c components
//output : output_seconds:16
//source_file : seconds.c
///Seconds_Count
///=============
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module seconds_count(output_seconds_ack,clk,rst,output_seconds,output_seconds_stb);
  input     output_seconds_ack;
  input     clk;
  input     rst;
  output    [15:0] output_seconds;
  output    output_seconds_stb;
  reg       [15:0] timer;
  reg       [24:0] program_counter;
  reg       [15:0] address;
  reg       [15:0] data_out;
  reg       [15:0] data_in;
  reg       write_enable;
  reg       [15:0] register_0;
  reg       [15:0] register_1;
  reg       [15:0] register_2;
  reg       [15:0] register_3;
  reg       [15:0] register_4;
  reg       [15:0] s_output_seconds_stb;
  reg       [15:0] s_output_seconds;
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
        register_3 <= 16'd0;
      end

      16'd3:
      begin
        register_4 <= 16'd0;
      end

      16'd4:
      begin
        register_2 <= register_4;
      end

      16'd5:
      begin
        register_4 <= register_2;
      end

      16'd6:
      begin
        register_4 <= $signed(register_4) > $signed(16'd1000);
      end

      16'd7:
      begin
        if (register_4 == 16'h0000)
          program_counter <= 21;
      end

      16'd8:
      begin
        register_4 <= 16'd0;
      end

      16'd9:
      begin
        register_3 <= register_4;
      end

      16'd10:
      begin
        register_4 <= register_3;
      end

      16'd11:
      begin
        register_4 <= $signed(register_4) > $signed(16'd1000);
      end

      16'd12:
      begin
        if (register_4 == 16'h0000)
          program_counter <= 18;
      end

      16'd13:
      begin
        register_4 <= 16'd50;
      end

      16'd14:
      begin
        if (timer < register_4) begin
          program_counter <= program_counter;
          timer <= timer+1;
        end
      end

      16'd15:
      begin
        register_4 <= register_3;
      end

      16'd16:
      begin
        register_4 <= $signed(register_4) + $signed(16'd1);
      end

      16'd17:
      begin
        register_3 <= register_4;
        program_counter <= 16'd10;
      end

      16'd18:
      begin
        register_4 <= register_2;
      end

      16'd19:
      begin
        register_4 <= $signed(register_4) + $signed(16'd1);
      end

      16'd20:
      begin
        register_2 <= register_4;
        program_counter <= 16'd5;
      end

      16'd21:
      begin
        register_4 <= 16'd0;
      end

      16'd22:
      begin
        s_output_seconds <= register_4;
        program_counter <= 22;
        s_output_seconds_stb <= 1'b1;
        if (s_output_seconds_stb == 1'b1 && output_seconds_ack == 1'b1) begin
          s_output_seconds_stb <= 1'b0;
          program_counter <= 23;
        end
      end

      16'd23:
      begin
        program_counter <= 16'd3;
      end

      16'd24:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end
  assign output_seconds_stb = s_output_seconds_stb;
  assign output_seconds = s_output_seconds;

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


endmodule
