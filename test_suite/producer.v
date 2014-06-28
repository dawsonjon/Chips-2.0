//////////////////////////////////////////////////////////////////////////////
//name : producer
//output : output_z:16
//source_file : test_suite/producer.c
///========
///
///Created by C2CHIP

//////////////////////////////////////////////////////////////////////////////
// Register Allocation
// ===================
//         Register                 Name                   Size          
//            0             producer return address            4            
//            1                  variable z                 4            
//            2              temporary_register             4            
//            3              temporary_register             4            
module producer(output_z_ack,clk,rst,output_z,output_z_stb);
  integer file_count;
  real fp_value;
  input output_z_ack;
  input clk;
  input rst;
  output [31:0] output_z;
  output output_z_stb;
  reg [15:0] timer;
  reg timer_enable;
  reg stage_0_enable;
  reg stage_1_enable;
  reg stage_2_enable;
  reg [5:0] program_counter;
  reg [5:0] program_counter_0;
  reg [38:0] instruction_0;
  reg [2:0] opcode_0;
  reg [1:0] dest_0;
  reg [1:0] src_0;
  reg [1:0] srcb_0;
  reg [31:0] literal_0;
  reg [5:0] program_counter_1;
  reg [2:0] opcode_1;
  reg [1:0] dest_1;
  reg [31:0] register_1;
  reg [31:0] registerb_1;
  reg [31:0] register_hi_1;
  reg [31:0] registerb_hi_1;
  reg [31:0] literal_1;
  reg [1:0] dest_2;
  reg [63:0] long_result;
  reg [31:0] result_2;
  reg [31:0] result_hi_2;
  reg write_enable_2;
  reg write_enable_hi_2;
  reg [15:0] address;
  reg [31:0] data_out;
  reg [31:0] data_in;
  reg carry;
  reg [31:0] result_hi;
  reg [31:0] register_hi;
  reg [31:0] registerb_hi;
  reg memory_enable;
  reg [31:0] s_output_z_stb;
  reg [31:0] s_output_z;
  reg [38:0] instructions [55:0];
  reg [31:0] registers [3:0];

  //////////////////////////////////////////////////////////////////////////////
  // INSTRUCTION INITIALIZATION                                                 
  //                                                                            
  // Initialise the contents of the instruction memory                          
  //
  // Intruction Set
  // ==============
  // 0 {'literal': True, 'op': 'jmp_and_link'}
  // 1 {'literal': False, 'op': 'stop'}
  // 2 {'literal': True, 'op': 'literal'}
  // 3 {'literal': False, 'op': 'nop'}
  // 4 {'literal': False, 'op': 'move'}
  // 5 {'literal': False, 'op': 'write'}
  // 6 {'literal': False, 'op': 'jmp_to_reg'}
  // Intructions
  // ===========
  
  initial
  begin
    instructions[0] = {3'd0, 2'd0, 2'd0, 32'd2};//{'dest': 0, 'label': 2, 'op': 'jmp_and_link'}
    instructions[1] = {3'd1, 2'd0, 2'd0, 32'd0};//{'op': 'stop'}
    instructions[2] = {3'd2, 2'd1, 2'd0, 32'd0};//{'dest': 1, 'literal': 0, 'signed': True, 'op': 'literal'}
    instructions[3] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[4] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[5] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[6] = {3'd2, 2'd2, 2'd0, 32'd1};//{'dest': 2, 'literal': 1, 'signed': True, 'op': 'literal'}
    instructions[7] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[8] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[9] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[10] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[11] = {3'd2, 2'd2, 2'd0, 32'd2};//{'dest': 2, 'literal': 2, 'signed': True, 'op': 'literal'}
    instructions[12] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[13] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[14] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[15] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[16] = {3'd2, 2'd2, 2'd0, 32'd3};//{'dest': 2, 'literal': 3, 'signed': True, 'op': 'literal'}
    instructions[17] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[18] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[19] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[20] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[21] = {3'd2, 2'd2, 2'd0, 32'd4};//{'dest': 2, 'literal': 4, 'signed': True, 'op': 'literal'}
    instructions[22] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[23] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[24] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[25] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[26] = {3'd2, 2'd2, 2'd0, 32'd5};//{'dest': 2, 'literal': 5, 'signed': True, 'op': 'literal'}
    instructions[27] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[28] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[29] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[30] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[31] = {3'd2, 2'd2, 2'd0, 32'd6};//{'dest': 2, 'literal': 6, 'signed': True, 'op': 'literal'}
    instructions[32] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[33] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[34] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[35] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[36] = {3'd2, 2'd2, 2'd0, 32'd7};//{'dest': 2, 'literal': 7, 'signed': True, 'op': 'literal'}
    instructions[37] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[38] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[39] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[40] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[41] = {3'd2, 2'd2, 2'd0, 32'd8};//{'dest': 2, 'literal': 8, 'signed': True, 'op': 'literal'}
    instructions[42] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[43] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[44] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[45] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[46] = {3'd2, 2'd2, 2'd0, 32'd9};//{'dest': 2, 'literal': 9, 'signed': True, 'op': 'literal'}
    instructions[47] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[48] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[49] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[50] = {3'd4, 2'd3, 2'd1, 32'd0};//{'dest': 3, 'src': 1, 'op': 'move'}
    instructions[51] = {3'd2, 2'd2, 2'd0, 32'd10};//{'dest': 2, 'literal': 10, 'signed': True, 'op': 'literal'}
    instructions[52] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[53] = {3'd3, 2'd0, 2'd0, 32'd0};//{'op': 'nop'}
    instructions[54] = {3'd5, 2'd0, 2'd3, 32'd2};//{'srcb': 2, 'src': 3, 'op': 'write'}
    instructions[55] = {3'd6, 2'd0, 2'd0, 32'd0};//{'src': 0, 'op': 'jmp_to_reg'}
  end


  //////////////////////////////////////////////////////////////////////////////
  // CPU IMPLEMENTAION OF C PROCESS                                             
  //                                                                            
  // This section of the file contains a CPU implementing the C process.        
  
  always @(posedge clk)
  begin

    write_enable_2 <= 0;
    //stage 0 instruction fetch
    if (stage_0_enable) begin
      stage_1_enable <= 1;
      instruction_0 <= instructions[program_counter];
      opcode_0 = instruction_0[38:36];
      dest_0 = instruction_0[35:34];
      src_0 = instruction_0[33:32];
      srcb_0 = instruction_0[1:0];
      literal_0 = instruction_0[31:0];
      if(write_enable_2) begin
            registers[dest_2] <= result_2;
      end
      program_counter_0 <= program_counter;
      program_counter <= program_counter + 1;
    end

    //stage 1 opcode fetch
    if (stage_1_enable) begin
      stage_2_enable <= 1;
      register_1 <= registers[src_0];
      registerb_1 <= registers[srcb_0];
      dest_1 <= dest_0;
      literal_1 <= literal_0;
      opcode_1 <= opcode_0;
      program_counter_1 <= program_counter_0;
    end

    //stage 2 opcode fetch
    if (stage_2_enable) begin
      dest_2 <= dest_1;
      case(opcode_1)

        //jmp_and_link
        16'd0:
        begin
          program_counter <= literal_1;
          result_2 <= program_counter_1 + 1;
          write_enable_2 <= 1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        //stop
        16'd1:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        //literal
        16'd2:
        begin
          result_2 <= literal_1;
          write_enable_2 <= 1;
        end

        //nop
        16'd3:
        begin
        end

        //move
        16'd4:
        begin
          result_2 <= register_1;
          write_enable_2 <= 1;
        end

        //write
        16'd5:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          case(register_1)

            0:
            begin
              s_output_z_stb <= 1'b1;
            end
          endcase
        end

        //jmp_to_reg
        16'd6:
        begin
          program_counter <= register_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

       endcase
    end
     if (s_output_z_stb == 1'b1 && output_z_ack == 1'b1) begin
       s_output_z_stb <= 1'b0;
       stage_0_enable <= 1;
       stage_1_enable <= 1;
       stage_2_enable <= 1;
     end

    if (timer == 0) begin
      if (timer_enable) begin
         stage_0_enable <= 1;
         stage_1_enable <= 1;
         stage_2_enable <= 1;
         timer_enable <= 0;
      end
    end else begin
      timer <= timer - 1;
    end

    if (rst == 1'b1) begin
      stage_0_enable <= 1;
      stage_1_enable <= 0;
      stage_2_enable <= 0;
      timer <= 0;
      timer_enable <= 0;
      program_counter <= 0;
      s_output_z_stb <= 0;
    end
  end
  assign output_z_stb = s_output_z_stb;
  assign output_z = s_output_z;

endmodule
