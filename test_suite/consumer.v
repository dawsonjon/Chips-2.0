//////////////////////////////////////////////////////////////////////////////
//name : consumer
//input : input_a:16
//source_file : test_suite/consumer.c
///========
///
///Created by C2CHIP

//////////////////////////////////////////////////////////////////////////////
// Register Allocation
// ===================
//         Register                 Name                   Size          
//            0             consumer return address            4            
//            1                  variable a                 4            
//            2              temporary_register             4            
//            3              temporary_register             4            
//            4              temporary_register             4            
module consumer(input_a,input_a_stb,clk,rst,input_a_ack);
  integer file_count;
  real fp_value;
  input [31:0] input_a;
  input input_a_stb;
  input clk;
  input rst;
  output input_a_ack;
  reg [15:0] timer;
  reg timer_enable;
  reg stage_0_enable;
  reg stage_1_enable;
  reg stage_2_enable;
  reg [6:0] program_counter;
  reg [6:0] program_counter_0;
  reg [42:0] instruction_0;
  reg [4:0] opcode_0;
  reg [2:0] dest_0;
  reg [2:0] src_0;
  reg [2:0] srcb_0;
  reg [31:0] literal_0;
  reg [6:0] program_counter_1;
  reg [4:0] opcode_1;
  reg [2:0] dest_1;
  reg [31:0] register_1;
  reg [31:0] registerb_1;
  reg [31:0] register_hi_1;
  reg [31:0] registerb_hi_1;
  reg [31:0] literal_1;
  reg [2:0] dest_2;
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
  reg [31:0] s_input_a_ack;
  reg [42:0] instructions [119:0];
  reg [31:0] registers [4:0];

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
  // 5 {'literal': False, 'op': 'read'}
  // 6 {'literal': False, 'op': 'equal'}
  // 7 {'literal': False, 'line': 4, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 8 {'literal': False, 'line': 5, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 9 {'literal': False, 'line': 6, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 10 {'literal': False, 'line': 7, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 11 {'literal': False, 'line': 8, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 12 {'literal': False, 'line': 9, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 13 {'literal': False, 'line': 10, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 14 {'literal': False, 'line': 11, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 15 {'literal': False, 'line': 12, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 16 {'literal': False, 'line': 13, 'file': 'test_suite/consumer.c', 'op': 'assert'}
  // 17 {'literal': False, 'line': 14, 'file': 'test_suite/consumer.c', 'op': 'unsigned_report'}
  // 18 {'literal': False, 'op': 'jmp_to_reg'}
  // Intructions
  // ===========
  
  initial
  begin
    instructions[0] = {5'd0, 3'd0, 3'd0, 32'd2};//{'dest': 0, 'label': 2, 'op': 'jmp_and_link'}
    instructions[1] = {5'd1, 3'd0, 3'd0, 32'd0};//{'op': 'stop'}
    instructions[2] = {5'd2, 3'd1, 3'd0, 32'd0};//{'dest': 1, 'literal': 0, 'signed': True, 'op': 'literal'}
    instructions[3] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[4] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[5] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[6] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[7] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[8] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[9] = {5'd2, 3'd4, 3'd0, 32'd1};//{'dest': 4, 'literal': 1, 'signed': True, 'op': 'literal'}
    instructions[10] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[11] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[12] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[13] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[14] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[15] = {5'd7, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 4, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[16] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[17] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[18] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[19] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[20] = {5'd2, 3'd4, 3'd0, 32'd2};//{'dest': 4, 'literal': 2, 'signed': True, 'op': 'literal'}
    instructions[21] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[22] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[23] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[24] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[25] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[26] = {5'd8, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 5, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[27] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[28] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[29] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[30] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[31] = {5'd2, 3'd4, 3'd0, 32'd3};//{'dest': 4, 'literal': 3, 'signed': True, 'op': 'literal'}
    instructions[32] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[33] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[34] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[35] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[36] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[37] = {5'd9, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 6, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[38] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[39] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[40] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[41] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[42] = {5'd2, 3'd4, 3'd0, 32'd4};//{'dest': 4, 'literal': 4, 'signed': True, 'op': 'literal'}
    instructions[43] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[44] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[45] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[46] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[47] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[48] = {5'd10, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 7, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[49] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[50] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[51] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[52] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[53] = {5'd2, 3'd4, 3'd0, 32'd5};//{'dest': 4, 'literal': 5, 'signed': True, 'op': 'literal'}
    instructions[54] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[55] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[56] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[57] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[58] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[59] = {5'd11, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 8, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[60] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[61] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[62] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[63] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[64] = {5'd2, 3'd4, 3'd0, 32'd6};//{'dest': 4, 'literal': 6, 'signed': True, 'op': 'literal'}
    instructions[65] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[66] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[67] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[68] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[69] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[70] = {5'd12, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 9, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[71] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[72] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[73] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[74] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[75] = {5'd2, 3'd4, 3'd0, 32'd7};//{'dest': 4, 'literal': 7, 'signed': True, 'op': 'literal'}
    instructions[76] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[77] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[78] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[79] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[80] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[81] = {5'd13, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 10, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[82] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[83] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[84] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[85] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[86] = {5'd2, 3'd4, 3'd0, 32'd8};//{'dest': 4, 'literal': 8, 'signed': True, 'op': 'literal'}
    instructions[87] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[88] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[89] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[90] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[91] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[92] = {5'd14, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 11, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[93] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[94] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[95] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[96] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[97] = {5'd2, 3'd4, 3'd0, 32'd9};//{'dest': 4, 'literal': 9, 'signed': True, 'op': 'literal'}
    instructions[98] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[99] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[100] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[101] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[102] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[103] = {5'd15, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 12, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[104] = {5'd4, 3'd4, 3'd1, 32'd0};//{'dest': 4, 'src': 1, 'op': 'move'}
    instructions[105] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[106] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[107] = {5'd5, 3'd3, 3'd4, 32'd0};//{'dest': 3, 'src': 4, 'op': 'read'}
    instructions[108] = {5'd2, 3'd4, 3'd0, 32'd10};//{'dest': 4, 'literal': 10, 'signed': True, 'op': 'literal'}
    instructions[109] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[110] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[111] = {5'd6, 3'd2, 3'd3, 32'd4};//{'dest': 2, 'src': 3, 'srcb': 4, 'op': 'equal'}
    instructions[112] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[113] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[114] = {5'd16, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 13, 'file': 'test_suite/consumer.c', 'op': 'assert'}
    instructions[115] = {5'd2, 3'd2, 3'd0, 32'd1};//{'dest': 2, 'literal': 1, 'signed': True, 'op': 'literal'}
    instructions[116] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[117] = {5'd3, 3'd0, 3'd0, 32'd0};//{'op': 'nop'}
    instructions[118] = {5'd17, 3'd0, 3'd2, 32'd0};//{'src': 2, 'line': 14, 'file': 'test_suite/consumer.c', 'op': 'unsigned_report'}
    instructions[119] = {5'd18, 3'd0, 3'd0, 32'd0};//{'src': 0, 'op': 'jmp_to_reg'}
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
      opcode_0 = instruction_0[42:38];
      dest_0 = instruction_0[37:35];
      src_0 = instruction_0[34:32];
      srcb_0 = instruction_0[2:0];
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

        //read
        16'd5:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          case(register_1)

            0:
            begin
              s_input_a_ack <= 1'b1;
            end
          endcase
        end

        //equal
        16'd6:
        begin
          result_2 <= register_1 == registerb_1;
          write_enable_2 <= 1;
        end

        //assert
        16'd7:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 4 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd8:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 5 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd9:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 6 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd10:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 7 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd11:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 8 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd12:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 9 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd13:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 10 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd14:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 11 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd15:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 12 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //assert
        16'd16:
        begin
          if (register_1 == 0) begin
            $display("Assertion failed at line: 13 in file: test_suite/consumer.c");
            $finish_and_return(1);
          end
        end

        //unsigned_report
        16'd17:
        begin
          $display ("%d (report at line: 14 in file: test_suite/consumer.c)", $unsigned(register_1));
        end

        //jmp_to_reg
        16'd18:
        begin
          program_counter <= register_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

       endcase
    end
    if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
       result_2 <= input_a;
       write_enable_2 <= 1;
       s_input_a_ack <= 1'b0;
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
      s_input_a_ack <= 0;
    end
  end
  assign input_a_ack = s_input_a_ack;

endmodule
