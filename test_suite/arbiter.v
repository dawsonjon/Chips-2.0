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
  reg [15:0] memory [-1:0];

  //////////////////////////////////////////////////////////////////////////////
  // MEMORY INITIALIZATION                                                      
  //                                                                            
  // In order to reduce program size, array contents have been stored into      
  // memory at initialization. In an FPGA, this will result in the memory being 
  // initialized when the FPGA configures.                                      
  // Memory will not be re-initialized at reset.                                
  // Dissable this behaviour using the no_initialize_memory switch              
  
  initial
  begin
  end


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
    end
  end
  assign input_a_ack = s_input_a_ack;
  assign input_b_ack = s_input_b_ack;
  assign output_z_stb = s_output_z_stb;
  assign output_z = s_output_z;

endmodule
