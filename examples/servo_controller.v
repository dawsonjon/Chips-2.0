//////////////////////////////////////////////////////////////////////////////
//name : servo_controller
//input : input_control:16
//output : output_servos:16
//source_file : servo_controller.c
///================
///
///Created by C2CHIP

//////////////////////////////////////////////////////////////////////////////
// Register Allocation
// ===================
//         Register                 Name                   Size          
//            0               variable pulses               2            
//            1              temporary_register             2            
//            2              temporary_register             2            
//            3              temporary_register             2            
//            4              temporary_register             4            
//            5              temporary_register             4            
//            6              temporary_register             4            
//            7              temporary_register             2            
//            8              temporary_register             2            
//            9             wait_us return address            2            
//            10                variable us                 4            
//            11                 variable i                 2            
//            12            servo_controller return address            2            
//            13                   array                    2            
//            14               variable servo               2            
//            15             variable position              2            
module servo_controller(input_control,input_control_stb,output_servos_ack,clk,rst,output_servos,output_servos_stb,input_control_ack);
  integer file_count;
  real fp_value;
  input [15:0] input_control;
  input input_control_stb;
  input output_servos_ack;
  input clk;
  input rst;
  output [15:0] output_servos;
  output output_servos_stb;
  output input_control_ack;
  reg [15:0] timer;
  reg timer_enable;
  reg stage_0_enable;
  reg stage_1_enable;
  reg stage_2_enable;
  reg [7:0] program_counter;
  reg [7:0] program_counter_0;
  reg [44:0] instruction_0;
  reg [4:0] opcode_0;
  reg [3:0] dest_0;
  reg [3:0] src_0;
  reg [3:0] srcb_0;
  reg [31:0] literal_0;
  reg [7:0] program_counter_1;
  reg [4:0] opcode_1;
  reg [3:0] dest_1;
  reg [31:0] register_1;
  reg [31:0] registerb_1;
  reg [31:0] literal_1;
  reg [3:0] dest_2;
  reg [31:0] result_2;
  reg write_enable_2;
  reg [15:0] address_2;
  reg [15:0] data_out_2;
  reg [15:0] data_in_2;
  reg memory_enable_2;
  reg [15:0] address_4;
  reg [31:0] data_out_4;
  reg [31:0] data_in_4;
  reg memory_enable_4;
  reg [15:0] s_output_servos_stb;
  reg [15:0] s_output_servos;
  reg [15:0] s_input_control_ack;
  reg [15:0] memory_2 [7:0];
  reg [44:0] instructions [166:0];
  reg [31:0] registers [15:0];

  //////////////////////////////////////////////////////////////////////////////
  // INSTRUCTION INITIALIZATION                                                 
  //                                                                            
  // Initialise the contents of the instruction memory                          
  //
  // Intruction Set
  // ==============
  // 0 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'jmp_and_link'}
  // 1 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'stop'}
  // 2 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'literal'}
  // 3 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'nop'}
  // 4 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'move'}
  // 5 {'float': False, 'literal': False, 'right': False, 'unsigned': True, 'op': '<'}
  // 6 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'jmp_if_false'}
  // 7 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'wait_clocks'}
  // 8 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '+'}
  // 9 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'goto'}
  // 10 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'jmp_to_reg'}
  // 11 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '<'}
  // 12 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': '+'}
  // 13 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_write'}
  // 14 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'input': 'control', 'op': 'ready'}
  // 15 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'input': 'control', 'op': 'read'}
  // 16 {'float': False, 'literal': False, 'right': False, 'unsigned': True, 'op': '+'}
  // 17 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read_request'}
  // 18 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read_wait'}
  // 19 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read'}
  // 20 {'float': False, 'literal': False, 'right': False, 'unsigned': True, 'op': '>='}
  // 21 {'float': False, 'literal': True, 'right': False, 'unsigned': True, 'op': '<<'}
  // 22 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': '~'}
  // 23 {'float': False, 'literal': False, 'right': False, 'unsigned': True, 'op': '&'}
  // 24 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'output': 'servos', 'op': 'write'}
  // Intructions
  // ===========
  
  initial
  begin
    instructions[0] = {5'd0, 4'd12, 4'd0, 32'd25};//{'dest': 12, 'label': 25, 'op': 'jmp_and_link'}
    instructions[1] = {5'd1, 4'd0, 4'd0, 32'd0};//{'op': 'stop'}
    instructions[2] = {5'd2, 4'd11, 4'd0, 32'd0};//{'dest': 11, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[3] = {5'd2, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[4] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[5] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[6] = {5'd4, 4'd11, 4'd1, 32'd0};//{'dest': 11, 'src': 1, 'op': 'move'}
    instructions[7] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[8] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[9] = {5'd4, 4'd5, 4'd11, 32'd0};//{'dest': 5, 'src': 11, 'op': 'move'}
    instructions[10] = {5'd4, 4'd6, 4'd10, 32'd0};//{'dest': 6, 'src': 10, 'op': 'move'}
    instructions[11] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[12] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[13] = {5'd5, 4'd4, 4'd5, 32'd6};//{'srcb': 6, 'src': 5, 'dest': 4, 'signed': False, 'op': '<', 'type': 'int', 'size': 4}
    instructions[14] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[15] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[16] = {5'd6, 4'd0, 4'd4, 32'd24};//{'src': 4, 'label': 24, 'op': 'jmp_if_false'}
    instructions[17] = {5'd2, 4'd4, 4'd0, 32'd100};//{'dest': 4, 'literal': 100, 'size': 4, 'signed': 4, 'op': 'literal'}
    instructions[18] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[19] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[20] = {5'd7, 4'd0, 4'd4, 32'd0};//{'src': 4, 'op': 'wait_clocks'}
    instructions[21] = {5'd4, 4'd1, 4'd11, 32'd0};//{'dest': 1, 'src': 11, 'op': 'move'}
    instructions[22] = {5'd8, 4'd11, 4'd11, 32'd1};//{'src': 11, 'right': 1, 'dest': 11, 'signed': False, 'op': '+', 'size': 2}
    instructions[23] = {5'd9, 4'd0, 4'd0, 32'd7};//{'label': 7, 'op': 'goto'}
    instructions[24] = {5'd10, 4'd0, 4'd9, 32'd0};//{'src': 9, 'op': 'jmp_to_reg'}
    instructions[25] = {5'd2, 4'd13, 4'd0, 32'd0};//{'dest': 13, 'literal': 0, 'op': 'literal'}
    instructions[26] = {5'd2, 4'd14, 4'd0, 32'd0};//{'dest': 14, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[27] = {5'd2, 4'd15, 4'd0, 32'd0};//{'dest': 15, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[28] = {5'd2, 4'd0, 4'd0, 32'd0};//{'dest': 0, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[29] = {5'd2, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[30] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[31] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[32] = {5'd4, 4'd14, 4'd1, 32'd0};//{'dest': 14, 'src': 1, 'op': 'move'}
    instructions[33] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[34] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[35] = {5'd4, 4'd2, 4'd14, 32'd0};//{'dest': 2, 'src': 14, 'op': 'move'}
    instructions[36] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[37] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[38] = {5'd11, 4'd1, 4'd2, 32'd8};//{'src': 2, 'right': 8, 'dest': 1, 'signed': False, 'op': '<', 'type': 'int', 'size': 2}
    instructions[39] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[40] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[41] = {5'd6, 4'd0, 4'd1, 32'd53};//{'src': 1, 'label': 53, 'op': 'jmp_if_false'}
    instructions[42] = {5'd2, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[43] = {5'd4, 4'd2, 4'd14, 32'd0};//{'dest': 2, 'src': 14, 'op': 'move'}
    instructions[44] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[45] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[46] = {5'd12, 4'd3, 4'd2, 32'd13};//{'dest': 3, 'src': 2, 'srcb': 13, 'signed': True, 'op': '+'}
    instructions[47] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[48] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[49] = {5'd13, 4'd0, 4'd3, 32'd1};//{'srcb': 1, 'src': 3, 'element_size': 2, 'op': 'memory_write'}
    instructions[50] = {5'd4, 4'd1, 4'd14, 32'd0};//{'dest': 1, 'src': 14, 'op': 'move'}
    instructions[51] = {5'd8, 4'd14, 4'd14, 32'd1};//{'src': 14, 'right': 1, 'dest': 14, 'signed': False, 'op': '+', 'size': 2}
    instructions[52] = {5'd9, 4'd0, 4'd0, 32'd33};//{'label': 33, 'op': 'goto'}
    instructions[53] = {5'd14, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'input': 'control', 'op': 'ready'}
    instructions[54] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[55] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[56] = {5'd6, 4'd0, 4'd1, 32'd76};//{'src': 1, 'label': 76, 'op': 'jmp_if_false'}
    instructions[57] = {5'd15, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'input': 'control', 'op': 'read'}
    instructions[58] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[59] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[60] = {5'd4, 4'd14, 4'd1, 32'd0};//{'dest': 14, 'src': 1, 'op': 'move'}
    instructions[61] = {5'd15, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'input': 'control', 'op': 'read'}
    instructions[62] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[63] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[64] = {5'd4, 4'd15, 4'd1, 32'd0};//{'dest': 15, 'src': 1, 'op': 'move'}
    instructions[65] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[66] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[67] = {5'd4, 4'd1, 4'd15, 32'd0};//{'dest': 1, 'src': 15, 'op': 'move'}
    instructions[68] = {5'd4, 4'd2, 4'd14, 32'd0};//{'dest': 2, 'src': 14, 'op': 'move'}
    instructions[69] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[70] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[71] = {5'd16, 4'd3, 4'd2, 32'd13};//{'dest': 3, 'src': 2, 'srcb': 13, 'signed': False, 'op': '+'}
    instructions[72] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[73] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[74] = {5'd13, 4'd0, 4'd3, 32'd1};//{'srcb': 1, 'src': 3, 'element_size': 2, 'op': 'memory_write'}
    instructions[75] = {5'd9, 4'd0, 4'd0, 32'd76};//{'label': 76, 'op': 'goto'}
    instructions[76] = {5'd2, 4'd1, 4'd0, 32'd255};//{'dest': 1, 'literal': 255, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[77] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[78] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[79] = {5'd4, 4'd0, 4'd1, 32'd0};//{'dest': 0, 'src': 1, 'op': 'move'}
    instructions[80] = {5'd2, 4'd2, 4'd0, 32'd1000};//{'dest': 2, 'literal': 1000, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[81] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[82] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[83] = {5'd4, 4'd10, 4'd2, 32'd0};//{'dest': 10, 'src': 2, 'op': 'move'}
    instructions[84] = {5'd0, 4'd9, 4'd0, 32'd2};//{'dest': 9, 'label': 2, 'op': 'jmp_and_link'}
    instructions[85] = {5'd2, 4'd1, 4'd0, -32'd500};//{'dest': 1, 'literal': -500, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[86] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[87] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[88] = {5'd4, 4'd15, 4'd1, 32'd0};//{'dest': 15, 'src': 1, 'op': 'move'}
    instructions[89] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[90] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[91] = {5'd4, 4'd2, 4'd15, 32'd0};//{'dest': 2, 'src': 15, 'op': 'move'}
    instructions[92] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[93] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[94] = {5'd11, 4'd1, 4'd2, 32'd500};//{'src': 2, 'right': 500, 'dest': 1, 'signed': False, 'op': '<', 'type': 'int', 'size': 2}
    instructions[95] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[96] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[97] = {5'd6, 4'd0, 4'd1, 32'd160};//{'src': 1, 'label': 160, 'op': 'jmp_if_false'}
    instructions[98] = {5'd2, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[99] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[100] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[101] = {5'd4, 4'd14, 4'd1, 32'd0};//{'dest': 14, 'src': 1, 'op': 'move'}
    instructions[102] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[103] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[104] = {5'd4, 4'd2, 4'd14, 32'd0};//{'dest': 2, 'src': 14, 'op': 'move'}
    instructions[105] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[106] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[107] = {5'd11, 4'd1, 4'd2, 32'd8};//{'src': 2, 'right': 8, 'dest': 1, 'signed': False, 'op': '<', 'type': 'int', 'size': 2}
    instructions[108] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[109] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[110] = {5'd6, 4'd0, 4'd1, 32'd152};//{'src': 1, 'label': 152, 'op': 'jmp_if_false'}
    instructions[111] = {5'd4, 4'd2, 4'd15, 32'd0};//{'dest': 2, 'src': 15, 'op': 'move'}
    instructions[112] = {5'd4, 4'd7, 4'd14, 32'd0};//{'dest': 7, 'src': 14, 'op': 'move'}
    instructions[113] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[114] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[115] = {5'd16, 4'd8, 4'd7, 32'd13};//{'dest': 8, 'src': 7, 'srcb': 13, 'signed': False, 'op': '+'}
    instructions[116] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[117] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[118] = {5'd17, 4'd0, 4'd8, 32'd0};//{'element_size': 2, 'src': 8, 'sequence': 32296400, 'op': 'memory_read_request'}
    instructions[119] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[120] = {5'd18, 4'd0, 4'd8, 32'd0};//{'element_size': 2, 'src': 8, 'sequence': 32296400, 'op': 'memory_read_wait'}
    instructions[121] = {5'd19, 4'd3, 4'd8, 32'd0};//{'dest': 3, 'src': 8, 'sequence': 32296400, 'element_size': 2, 'op': 'memory_read'}
    instructions[122] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[123] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[124] = {5'd20, 4'd1, 4'd2, 32'd3};//{'srcb': 3, 'src': 2, 'dest': 1, 'signed': False, 'op': '>=', 'type': 'int', 'size': 2}
    instructions[125] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[126] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[127] = {5'd6, 4'd0, 4'd1, 32'd149};//{'src': 1, 'label': 149, 'op': 'jmp_if_false'}
    instructions[128] = {5'd4, 4'd2, 4'd0, 32'd0};//{'dest': 2, 'src': 0, 'op': 'move'}
    instructions[129] = {5'd4, 4'd8, 4'd14, 32'd0};//{'dest': 8, 'src': 14, 'op': 'move'}
    instructions[130] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[131] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[132] = {5'd21, 4'd7, 4'd8, 32'd1};//{'src': 8, 'dest': 7, 'signed': False, 'op': '<<', 'size': 2, 'type': 'int', 'left': 1}
    instructions[133] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[134] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[135] = {5'd22, 4'd3, 4'd7, 32'd0};//{'dest': 3, 'src': 7, 'op': '~'}
    instructions[136] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[137] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[138] = {5'd23, 4'd1, 4'd2, 32'd3};//{'srcb': 3, 'src': 2, 'dest': 1, 'signed': False, 'op': '&', 'type': 'int', 'size': 2}
    instructions[139] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[140] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[141] = {5'd4, 4'd0, 4'd1, 32'd0};//{'dest': 0, 'src': 1, 'op': 'move'}
    instructions[142] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[143] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[144] = {5'd4, 4'd1, 4'd0, 32'd0};//{'dest': 1, 'src': 0, 'op': 'move'}
    instructions[145] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[146] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[147] = {5'd24, 4'd0, 4'd1, 32'd0};//{'src': 1, 'output': 'servos', 'op': 'write'}
    instructions[148] = {5'd9, 4'd0, 4'd0, 32'd149};//{'label': 149, 'op': 'goto'}
    instructions[149] = {5'd4, 4'd1, 4'd14, 32'd0};//{'dest': 1, 'src': 14, 'op': 'move'}
    instructions[150] = {5'd8, 4'd14, 4'd14, 32'd1};//{'src': 14, 'right': 1, 'dest': 14, 'signed': False, 'op': '+', 'size': 2}
    instructions[151] = {5'd9, 4'd0, 4'd0, 32'd102};//{'label': 102, 'op': 'goto'}
    instructions[152] = {5'd2, 4'd2, 4'd0, 32'd1};//{'dest': 2, 'literal': 1, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[153] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[154] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[155] = {5'd4, 4'd10, 4'd2, 32'd0};//{'dest': 10, 'src': 2, 'op': 'move'}
    instructions[156] = {5'd0, 4'd9, 4'd0, 32'd2};//{'dest': 9, 'label': 2, 'op': 'jmp_and_link'}
    instructions[157] = {5'd4, 4'd1, 4'd15, 32'd0};//{'dest': 1, 'src': 15, 'op': 'move'}
    instructions[158] = {5'd8, 4'd15, 4'd15, 32'd1};//{'src': 15, 'right': 1, 'dest': 15, 'signed': False, 'op': '+', 'size': 2}
    instructions[159] = {5'd9, 4'd0, 4'd0, 32'd89};//{'label': 89, 'op': 'goto'}
    instructions[160] = {5'd2, 4'd2, 4'd0, 32'd10000};//{'dest': 2, 'literal': 10000, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[161] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[162] = {5'd3, 4'd0, 4'd0, 32'd0};//{'op': 'nop'}
    instructions[163] = {5'd4, 4'd10, 4'd2, 32'd0};//{'dest': 10, 'src': 2, 'op': 'move'}
    instructions[164] = {5'd0, 4'd9, 4'd0, 32'd2};//{'dest': 9, 'label': 2, 'op': 'jmp_and_link'}
    instructions[165] = {5'd9, 4'd0, 4'd0, 32'd53};//{'label': 53, 'op': 'goto'}
    instructions[166] = {5'd10, 4'd0, 4'd12, 32'd0};//{'src': 12, 'op': 'jmp_to_reg'}
  end


  //////////////////////////////////////////////////////////////////////////////
  // CPU IMPLEMENTAION OF C PROCESS                                             
  //                                                                            
  // This section of the file contains a CPU implementing the C process.        
  
  always @(posedge clk)
  begin

    //implement memory for 2 byte x n arrays
    if (memory_enable_2 == 1'b1) begin
      memory_2[address_2] <= data_in_2;
    end
    data_out_2 <= memory_2[address_2];
    memory_enable_2 <= 1'b0;

    write_enable_2 <= 0;
    //stage 0 instruction fetch
    if (stage_0_enable) begin
      stage_1_enable <= 1;
      instruction_0 <= instructions[program_counter];
      opcode_0 = instruction_0[44:40];
      dest_0 = instruction_0[39:36];
      src_0 = instruction_0[35:32];
      srcb_0 = instruction_0[3:0];
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

        16'd0:
        begin
          program_counter <= literal_1;
          result_2 <= program_counter_1 + 1;
          write_enable_2 <= 1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd1:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd2:
        begin
          result_2 <= literal_1;
          write_enable_2 <= 1;
        end

        16'd4:
        begin
          result_2 <= register_1;
          write_enable_2 <= 1;
        end

        16'd5:
        begin
          result_2 <= $unsigned(register_1) < $unsigned(registerb_1);
          write_enable_2 <= 1;
        end

        16'd6:
        begin
          if (register_1 == 0) begin
            program_counter <= literal_1;
            stage_0_enable <= 1;
            stage_1_enable <= 0;
            stage_2_enable <= 0;
          end
        end

        16'd7:
        begin
          timer <= register_1;
          timer_enable <= 1;
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd8:
        begin
          result_2 <= $unsigned(register_1) + $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd9:
        begin
          program_counter <= literal_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd10:
        begin
          program_counter <= register_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd11:
        begin
          result_2 <= $unsigned(register_1) < $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd12:
        begin
          result_2 <= $signed(register_1) + $signed(registerb_1);
          write_enable_2 <= 1;
        end

        16'd13:
        begin
          address_2 <= register_1;
          data_in_2 <= registerb_1;
          memory_enable_2 <= 1'b1;
        end

        16'd14:
        begin
          result_2 <= 0;
          result_2[0] <= input_control_stb;
          write_enable_2 <= 1;
        end

        16'd15:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          s_input_control_ack <= 1'b1;
        end

        16'd16:
        begin
          result_2 <= $unsigned(register_1) + $unsigned(registerb_1);
          write_enable_2 <= 1;
        end

        16'd17:
        begin
          address_2 <= register_1;
        end

        16'd19:
        begin
          result_2 <= data_out_2;
          write_enable_2 <= 1;
        end

        16'd20:
        begin
          result_2 <= $unsigned(register_1) >= $unsigned(registerb_1);
          write_enable_2 <= 1;
        end

        16'd21:
        begin
          result_2 <= $unsigned(literal_1) << $unsigned(register_1);
          write_enable_2 <= 1;
        end

        16'd22:
        begin
          result_2 <= ~register_1;
          write_enable_2 <= 1;
        end

        16'd23:
        begin
          result_2 <= $unsigned(register_1) & $unsigned(registerb_1);
          write_enable_2 <= 1;
        end

        16'd24:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          s_output_servos_stb <= 1'b1;
          s_output_servos <= register_1;
        end

       endcase
    end
    if (s_input_control_ack == 1'b1 && input_control_stb == 1'b1) begin
       result_2 <= input_control;
       write_enable_2 <= 1;
       s_input_control_ack <= 1'b0;
       stage_0_enable <= 1;
       stage_1_enable <= 1;
       stage_2_enable <= 1;
     end

     if (s_output_servos_stb == 1'b1 && output_servos_ack == 1'b1) begin
       s_output_servos_stb <= 1'b0;
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
      s_input_control_ack <= 0;
      s_output_servos_stb <= 0;
    end
  end
  assign input_control_ack = s_input_control_ack;
  assign output_servos_stb = s_output_servos_stb;
  assign output_servos = s_output_servos;

endmodule
