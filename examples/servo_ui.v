//////////////////////////////////////////////////////////////////////////////
//name : servo_ui
//input : input_rs232:16
//output : output_control:16
//output : output_rs232:16
//source_file : servo_ui.c
///========
///
///Created by C2CHIP

//////////////////////////////////////////////////////////////////////////////
// Register Allocation
// ===================
//         Register                 Name                   Size          
//            0                    array                    2            
//            1              temporary_register             2            
//            2              temporary_register             2            
//            3              temporary_register             2            
//            4              temporary_register             2            
//            5              temporary_register             36           
//            6              temporary_register             38           
//            7              temporary_register             24           
//            8              temporary_register             42           
//            9              temporary_register             8            
//            10             temporary_register             64           
//            11             temporary_register             58           
//            12             temporary_register             80           
//            13            stdin_get_char return address            2            
//            14            variable stdin_get_char return value            2            
//            15            stdout_put_char return address            2            
//            16             variable character             2            
//            17            print_string return address            2            
//            18                   array                    2            
//            19                 variable i                 2            
//            20            is_num return address            2            
//            21            variable is_num return value            2            
//            22             variable character             2            
//            23            scan return address             2            
//            24            variable scan return value            2            
//            25             variable character             2            
//            26               variable value               2            
//            27            servo_ui return address            2            
//            28               variable servo               2            
//            29             variable position              2            
//            30                   array                    2            
//            31                   array                    2            
//            32                   array                    2            
//            33                   array                    2            
//            34                   array                    2            
//            35                   array                    2            
//            36                   array                    2            
//            37                   array                    2            
module servo_ui(input_rs232,input_rs232_stb,output_control_ack,output_rs232_ack,clk,rst,output_control,output_rs232,output_control_stb,output_rs232_stb,input_rs232_ack);
  integer file_count;
  real fp_value;
  input [15:0] input_rs232;
  input input_rs232_stb;
  input output_control_ack;
  input output_rs232_ack;
  input clk;
  input rst;
  output [15:0] output_control;
  output [15:0] output_rs232;
  output output_control_stb;
  output output_rs232_stb;
  output input_rs232_ack;
  reg [15:0] timer;
  reg timer_enable;
  reg stage_0_enable;
  reg stage_1_enable;
  reg stage_2_enable;
  reg [8:0] program_counter;
  reg [8:0] program_counter_0;
  reg [48:0] instruction_0;
  reg [4:0] opcode_0;
  reg [5:0] dest_0;
  reg [5:0] src_0;
  reg [5:0] srcb_0;
  reg [31:0] literal_0;
  reg [8:0] program_counter_1;
  reg [4:0] opcode_1;
  reg [5:0] dest_1;
  reg [31:0] register_1;
  reg [31:0] registerb_1;
  reg [31:0] literal_1;
  reg [5:0] dest_2;
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
  reg [15:0] s_output_control_stb;
  reg [15:0] s_output_rs232_stb;
  reg [15:0] s_output_control;
  reg [15:0] s_output_rs232;
  reg [15:0] s_input_rs232_ack;
  reg [15:0] memory_2 [180:0];
  reg [48:0] instructions [285:0];
  reg [31:0] registers [37:0];

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
    memory_2[2] = 83;
    memory_2[3] = 101;
    memory_2[4] = 114;
    memory_2[5] = 118;
    memory_2[6] = 111;
    memory_2[7] = 32;
    memory_2[8] = 67;
    memory_2[9] = 111;
    memory_2[10] = 110;
    memory_2[11] = 116;
    memory_2[12] = 114;
    memory_2[13] = 111;
    memory_2[14] = 108;
    memory_2[15] = 108;
    memory_2[16] = 101;
    memory_2[17] = 114;
    memory_2[18] = 10;
    memory_2[19] = 0;
    memory_2[20] = 74;
    memory_2[21] = 111;
    memory_2[22] = 110;
    memory_2[23] = 97;
    memory_2[24] = 116;
    memory_2[25] = 104;
    memory_2[26] = 97;
    memory_2[27] = 110;
    memory_2[28] = 32;
    memory_2[29] = 80;
    memory_2[30] = 32;
    memory_2[31] = 68;
    memory_2[32] = 97;
    memory_2[33] = 119;
    memory_2[34] = 115;
    memory_2[35] = 111;
    memory_2[36] = 110;
    memory_2[37] = 10;
    memory_2[38] = 0;
    memory_2[39] = 50;
    memory_2[40] = 48;
    memory_2[41] = 49;
    memory_2[42] = 51;
    memory_2[43] = 45;
    memory_2[44] = 49;
    memory_2[45] = 50;
    memory_2[46] = 45;
    memory_2[47] = 50;
    memory_2[48] = 52;
    memory_2[49] = 10;
    memory_2[50] = 0;
    memory_2[51] = 69;
    memory_2[52] = 110;
    memory_2[53] = 116;
    memory_2[54] = 101;
    memory_2[55] = 114;
    memory_2[56] = 32;
    memory_2[57] = 83;
    memory_2[58] = 101;
    memory_2[59] = 114;
    memory_2[60] = 118;
    memory_2[61] = 111;
    memory_2[62] = 32;
    memory_2[63] = 48;
    memory_2[64] = 32;
    memory_2[65] = 116;
    memory_2[66] = 111;
    memory_2[67] = 32;
    memory_2[68] = 55;
    memory_2[69] = 58;
    memory_2[70] = 10;
    memory_2[71] = 0;
    memory_2[72] = 126;
    memory_2[73] = 36;
    memory_2[74] = 10;
    memory_2[75] = 0;
    memory_2[76] = 115;
    memory_2[77] = 101;
    memory_2[78] = 114;
    memory_2[79] = 118;
    memory_2[80] = 111;
    memory_2[81] = 32;
    memory_2[82] = 115;
    memory_2[83] = 104;
    memory_2[84] = 111;
    memory_2[85] = 117;
    memory_2[86] = 108;
    memory_2[87] = 100;
    memory_2[88] = 32;
    memory_2[89] = 98;
    memory_2[90] = 101;
    memory_2[91] = 32;
    memory_2[92] = 98;
    memory_2[93] = 101;
    memory_2[94] = 116;
    memory_2[95] = 119;
    memory_2[96] = 101;
    memory_2[97] = 101;
    memory_2[98] = 110;
    memory_2[99] = 32;
    memory_2[100] = 48;
    memory_2[101] = 32;
    memory_2[102] = 97;
    memory_2[103] = 110;
    memory_2[104] = 100;
    memory_2[105] = 32;
    memory_2[106] = 55;
    memory_2[107] = 0;
    memory_2[108] = 69;
    memory_2[109] = 110;
    memory_2[110] = 116;
    memory_2[111] = 101;
    memory_2[112] = 114;
    memory_2[113] = 32;
    memory_2[114] = 80;
    memory_2[115] = 111;
    memory_2[116] = 115;
    memory_2[117] = 105;
    memory_2[118] = 116;
    memory_2[119] = 105;
    memory_2[120] = 111;
    memory_2[121] = 110;
    memory_2[122] = 32;
    memory_2[123] = 45;
    memory_2[124] = 53;
    memory_2[125] = 48;
    memory_2[126] = 48;
    memory_2[127] = 32;
    memory_2[128] = 116;
    memory_2[129] = 111;
    memory_2[130] = 32;
    memory_2[131] = 53;
    memory_2[132] = 48;
    memory_2[133] = 48;
    memory_2[134] = 58;
    memory_2[135] = 10;
    memory_2[136] = 0;
    memory_2[137] = 126;
    memory_2[138] = 36;
    memory_2[139] = 10;
    memory_2[140] = 0;
    memory_2[141] = 112;
    memory_2[142] = 111;
    memory_2[143] = 115;
    memory_2[144] = 105;
    memory_2[145] = 116;
    memory_2[146] = 105;
    memory_2[147] = 111;
    memory_2[148] = 110;
    memory_2[149] = 32;
    memory_2[150] = 115;
    memory_2[151] = 104;
    memory_2[152] = 111;
    memory_2[153] = 117;
    memory_2[154] = 108;
    memory_2[155] = 100;
    memory_2[156] = 32;
    memory_2[157] = 98;
    memory_2[158] = 101;
    memory_2[159] = 32;
    memory_2[160] = 98;
    memory_2[161] = 101;
    memory_2[162] = 116;
    memory_2[163] = 119;
    memory_2[164] = 101;
    memory_2[165] = 101;
    memory_2[166] = 110;
    memory_2[167] = 32;
    memory_2[168] = 45;
    memory_2[169] = 53;
    memory_2[170] = 48;
    memory_2[171] = 48;
    memory_2[172] = 32;
    memory_2[173] = 97;
    memory_2[174] = 110;
    memory_2[175] = 100;
    memory_2[176] = 32;
    memory_2[177] = 53;
    memory_2[178] = 48;
    memory_2[179] = 48;
    memory_2[180] = 0;
  end


  //////////////////////////////////////////////////////////////////////////////
  // INSTRUCTION INITIALIZATION                                                 
  //                                                                            
  // Initialise the contents of the instruction memory                          
  //
  // Intruction Set
  // ==============
  // 0 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'jmp_and_link'}
  // 1 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'stop'}
  // 2 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'input': 'rs232', 'op': 'read'}
  // 3 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'nop'}
  // 4 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'move'}
  // 5 {'float': False, 'literal': False, 'right': False, 'unsigned': False, 'op': 'jmp_to_reg'}
  // 6 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'output': 'rs232', 'op': 'write'}
  // 7 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'literal'}
  // 8 {'float': False, 'literal': False, 'right': False, 'unsigned': True, 'op': '+'}
  // 9 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read_request'}
  // 10 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read_wait'}
  // 11 {'right': False, 'element_size': 2, 'float': False, 'unsigned': False, 'literal': False, 'op': 'memory_read'}
  // 12 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'jmp_if_false'}
  // 13 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '+'}
  // 14 {'float': False, 'literal': True, 'right': False, 'unsigned': False, 'op': 'goto'}
  // 15 {'float': False, 'literal': True, 'right': True, 'unsigned': False, 'op': '>='}
  // 16 {'float': False, 'literal': True, 'right': True, 'unsigned': False, 'op': '<='}
  // 17 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '=='}
  // 18 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '-'}
  // 19 {'float': False, 'literal': True, 'right': True, 'unsigned': False, 'op': '*'}
  // 20 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '>='}
  // 21 {'float': False, 'literal': True, 'right': True, 'unsigned': True, 'op': '<='}
  // 22 {'right': False, 'float': False, 'unsigned': False, 'literal': False, 'output': 'control', 'op': 'write'}
  // Intructions
  // ===========
  
  initial
  begin
    instructions[0] = {5'd0, 6'd27, 6'd0, 32'd161};//{'dest': 27, 'label': 161, 'op': 'jmp_and_link'}
    instructions[1] = {5'd1, 6'd0, 6'd0, 32'd0};//{'op': 'stop'}
    instructions[2] = {5'd2, 6'd1, 6'd0, 32'd0};//{'dest': 1, 'input': 'rs232', 'op': 'read'}
    instructions[3] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[4] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[5] = {5'd4, 6'd14, 6'd1, 32'd0};//{'dest': 14, 'src': 1, 'op': 'move'}
    instructions[6] = {5'd5, 6'd0, 6'd13, 32'd0};//{'src': 13, 'op': 'jmp_to_reg'}
    instructions[7] = {5'd4, 6'd1, 6'd16, 32'd0};//{'dest': 1, 'src': 16, 'op': 'move'}
    instructions[8] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[9] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[10] = {5'd6, 6'd0, 6'd1, 32'd0};//{'src': 1, 'output': 'rs232', 'op': 'write'}
    instructions[11] = {5'd5, 6'd0, 6'd15, 32'd0};//{'src': 15, 'op': 'jmp_to_reg'}
    instructions[12] = {5'd7, 6'd19, 6'd0, 32'd0};//{'dest': 19, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[13] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[14] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[15] = {5'd4, 6'd2, 6'd19, 32'd0};//{'dest': 2, 'src': 19, 'op': 'move'}
    instructions[16] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[17] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[18] = {5'd8, 6'd3, 6'd2, 32'd18};//{'dest': 3, 'src': 2, 'srcb': 18, 'signed': False, 'op': '+'}
    instructions[19] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[20] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[21] = {5'd9, 6'd0, 6'd3, 32'd0};//{'element_size': 2, 'src': 3, 'sequence': 32208080, 'op': 'memory_read_request'}
    instructions[22] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[23] = {5'd10, 6'd0, 6'd3, 32'd0};//{'element_size': 2, 'src': 3, 'sequence': 32208080, 'op': 'memory_read_wait'}
    instructions[24] = {5'd11, 6'd1, 6'd3, 32'd0};//{'dest': 1, 'src': 3, 'sequence': 32208080, 'element_size': 2, 'op': 'memory_read'}
    instructions[25] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[26] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[27] = {5'd12, 6'd0, 6'd1, 32'd45};//{'src': 1, 'label': 45, 'op': 'jmp_if_false'}
    instructions[28] = {5'd4, 6'd3, 6'd19, 32'd0};//{'dest': 3, 'src': 19, 'op': 'move'}
    instructions[29] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[30] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[31] = {5'd8, 6'd4, 6'd3, 32'd18};//{'dest': 4, 'src': 3, 'srcb': 18, 'signed': False, 'op': '+'}
    instructions[32] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[33] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[34] = {5'd9, 6'd0, 6'd4, 32'd0};//{'element_size': 2, 'src': 4, 'sequence': 32212752, 'op': 'memory_read_request'}
    instructions[35] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[36] = {5'd10, 6'd0, 6'd4, 32'd0};//{'element_size': 2, 'src': 4, 'sequence': 32212752, 'op': 'memory_read_wait'}
    instructions[37] = {5'd11, 6'd2, 6'd4, 32'd0};//{'dest': 2, 'src': 4, 'sequence': 32212752, 'element_size': 2, 'op': 'memory_read'}
    instructions[38] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[39] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[40] = {5'd4, 6'd16, 6'd2, 32'd0};//{'dest': 16, 'src': 2, 'op': 'move'}
    instructions[41] = {5'd0, 6'd15, 6'd0, 32'd7};//{'dest': 15, 'label': 7, 'op': 'jmp_and_link'}
    instructions[42] = {5'd4, 6'd1, 6'd19, 32'd0};//{'dest': 1, 'src': 19, 'op': 'move'}
    instructions[43] = {5'd13, 6'd19, 6'd19, 32'd1};//{'src': 19, 'right': 1, 'dest': 19, 'signed': False, 'op': '+', 'size': 2}
    instructions[44] = {5'd14, 6'd0, 6'd0, 32'd46};//{'label': 46, 'op': 'goto'}
    instructions[45] = {5'd14, 6'd0, 6'd0, 32'd47};//{'label': 47, 'op': 'goto'}
    instructions[46] = {5'd14, 6'd0, 6'd0, 32'd13};//{'label': 13, 'op': 'goto'}
    instructions[47] = {5'd5, 6'd0, 6'd17, 32'd0};//{'src': 17, 'op': 'jmp_to_reg'}
    instructions[48] = {5'd4, 6'd2, 6'd22, 32'd0};//{'dest': 2, 'src': 22, 'op': 'move'}
    instructions[49] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[50] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[51] = {5'd15, 6'd1, 6'd2, 32'd48};//{'src': 2, 'right': 48, 'dest': 1, 'signed': True, 'op': '>=', 'type': 'int', 'size': 2}
    instructions[52] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[53] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[54] = {5'd12, 6'd0, 6'd1, 32'd59};//{'src': 1, 'label': 59, 'op': 'jmp_if_false'}
    instructions[55] = {5'd4, 6'd2, 6'd22, 32'd0};//{'dest': 2, 'src': 22, 'op': 'move'}
    instructions[56] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[57] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[58] = {5'd16, 6'd1, 6'd2, 32'd57};//{'src': 2, 'right': 57, 'dest': 1, 'signed': True, 'op': '<=', 'type': 'int', 'size': 2}
    instructions[59] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[60] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[61] = {5'd12, 6'd0, 6'd1, 32'd68};//{'src': 1, 'label': 68, 'op': 'jmp_if_false'}
    instructions[62] = {5'd7, 6'd1, 6'd0, 32'd1};//{'dest': 1, 'literal': 1, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[63] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[64] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[65] = {5'd4, 6'd21, 6'd1, 32'd0};//{'dest': 21, 'src': 1, 'op': 'move'}
    instructions[66] = {5'd5, 6'd0, 6'd20, 32'd0};//{'src': 20, 'op': 'jmp_to_reg'}
    instructions[67] = {5'd14, 6'd0, 6'd0, 32'd68};//{'label': 68, 'op': 'goto'}
    instructions[68] = {5'd7, 6'd1, 6'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[69] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[70] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[71] = {5'd4, 6'd21, 6'd1, 32'd0};//{'dest': 21, 'src': 1, 'op': 'move'}
    instructions[72] = {5'd5, 6'd0, 6'd20, 32'd0};//{'src': 20, 'op': 'jmp_to_reg'}
    instructions[73] = {5'd7, 6'd25, 6'd0, 32'd0};//{'dest': 25, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[74] = {5'd7, 6'd26, 6'd0, 32'd0};//{'dest': 26, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[75] = {5'd0, 6'd13, 6'd0, 32'd2};//{'dest': 13, 'label': 2, 'op': 'jmp_and_link'}
    instructions[76] = {5'd4, 6'd1, 6'd14, 32'd0};//{'dest': 1, 'src': 14, 'op': 'move'}
    instructions[77] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[78] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[79] = {5'd4, 6'd25, 6'd1, 32'd0};//{'dest': 25, 'src': 1, 'op': 'move'}
    instructions[80] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[81] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[82] = {5'd4, 6'd2, 6'd25, 32'd0};//{'dest': 2, 'src': 25, 'op': 'move'}
    instructions[83] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[84] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[85] = {5'd17, 6'd1, 6'd2, 32'd45};//{'src': 2, 'right': 45, 'dest': 1, 'signed': False, 'op': '==', 'type': 'int', 'size': 2}
    instructions[86] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[87] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[88] = {5'd12, 6'd0, 6'd1, 32'd95};//{'src': 1, 'label': 95, 'op': 'jmp_if_false'}
    instructions[89] = {5'd7, 6'd1, 6'd0, -32'd1};//{'dest': 1, 'literal': -1, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[90] = {5'd7, 6'd1, 6'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[91] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[92] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[93] = {5'd4, 6'd26, 6'd1, 32'd0};//{'dest': 26, 'src': 1, 'op': 'move'}
    instructions[94] = {5'd14, 6'd0, 6'd0, 32'd116};//{'label': 116, 'op': 'goto'}
    instructions[95] = {5'd4, 6'd2, 6'd25, 32'd0};//{'dest': 2, 'src': 25, 'op': 'move'}
    instructions[96] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[97] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[98] = {5'd17, 6'd1, 6'd2, 32'd43};//{'src': 2, 'right': 43, 'dest': 1, 'signed': False, 'op': '==', 'type': 'int', 'size': 2}
    instructions[99] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[100] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[101] = {5'd12, 6'd0, 6'd1, 32'd108};//{'src': 1, 'label': 108, 'op': 'jmp_if_false'}
    instructions[102] = {5'd7, 6'd1, 6'd0, 32'd1};//{'dest': 1, 'literal': 1, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[103] = {5'd7, 6'd1, 6'd0, 32'd0};//{'dest': 1, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[104] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[105] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[106] = {5'd4, 6'd26, 6'd1, 32'd0};//{'dest': 26, 'src': 1, 'op': 'move'}
    instructions[107] = {5'd14, 6'd0, 6'd0, 32'd116};//{'label': 116, 'op': 'goto'}
    instructions[108] = {5'd7, 6'd1, 6'd0, 32'd1};//{'dest': 1, 'literal': 1, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[109] = {5'd4, 6'd2, 6'd25, 32'd0};//{'dest': 2, 'src': 25, 'op': 'move'}
    instructions[110] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[111] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[112] = {5'd18, 6'd1, 6'd2, 32'd48};//{'src': 2, 'right': 48, 'dest': 1, 'signed': False, 'op': '-', 'type': 'int', 'size': 2}
    instructions[113] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[114] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[115] = {5'd4, 6'd26, 6'd1, 32'd0};//{'dest': 26, 'src': 1, 'op': 'move'}
    instructions[116] = {5'd0, 6'd13, 6'd0, 32'd2};//{'dest': 13, 'label': 2, 'op': 'jmp_and_link'}
    instructions[117] = {5'd4, 6'd1, 6'd14, 32'd0};//{'dest': 1, 'src': 14, 'op': 'move'}
    instructions[118] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[119] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[120] = {5'd4, 6'd25, 6'd1, 32'd0};//{'dest': 25, 'src': 1, 'op': 'move'}
    instructions[121] = {5'd4, 6'd2, 6'd26, 32'd0};//{'dest': 2, 'src': 26, 'op': 'move'}
    instructions[122] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[123] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[124] = {5'd19, 6'd1, 6'd2, 32'd10};//{'src': 2, 'right': 10, 'dest': 1, 'signed': True, 'op': '*', 'type': 'int', 'size': 2}
    instructions[125] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[126] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[127] = {5'd4, 6'd26, 6'd1, 32'd0};//{'dest': 26, 'src': 1, 'op': 'move'}
    instructions[128] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[129] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[130] = {5'd4, 6'd2, 6'd26, 32'd0};//{'dest': 2, 'src': 26, 'op': 'move'}
    instructions[131] = {5'd4, 6'd4, 6'd25, 32'd0};//{'dest': 4, 'src': 25, 'op': 'move'}
    instructions[132] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[133] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[134] = {5'd18, 6'd3, 6'd4, 32'd48};//{'src': 4, 'right': 48, 'dest': 3, 'signed': False, 'op': '-', 'type': 'int', 'size': 2}
    instructions[135] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[136] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[137] = {5'd8, 6'd1, 6'd2, 32'd3};//{'srcb': 3, 'src': 2, 'dest': 1, 'signed': False, 'op': '+', 'type': 'int', 'size': 2}
    instructions[138] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[139] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[140] = {5'd4, 6'd26, 6'd1, 32'd0};//{'dest': 26, 'src': 1, 'op': 'move'}
    instructions[141] = {5'd4, 6'd3, 6'd25, 32'd0};//{'dest': 3, 'src': 25, 'op': 'move'}
    instructions[142] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[143] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[144] = {5'd4, 6'd22, 6'd3, 32'd0};//{'dest': 22, 'src': 3, 'op': 'move'}
    instructions[145] = {5'd0, 6'd20, 6'd0, 32'd48};//{'dest': 20, 'label': 48, 'op': 'jmp_and_link'}
    instructions[146] = {5'd4, 6'd2, 6'd21, 32'd0};//{'dest': 2, 'src': 21, 'op': 'move'}
    instructions[147] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[148] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[149] = {5'd17, 6'd1, 6'd2, 32'd0};//{'src': 2, 'right': 0, 'dest': 1, 'signed': False, 'op': '==', 'type': 'int', 'size': 2}
    instructions[150] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[151] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[152] = {5'd12, 6'd0, 6'd1, 32'd155};//{'src': 1, 'label': 155, 'op': 'jmp_if_false'}
    instructions[153] = {5'd14, 6'd0, 6'd0, 32'd156};//{'label': 156, 'op': 'goto'}
    instructions[154] = {5'd14, 6'd0, 6'd0, 32'd155};//{'label': 155, 'op': 'goto'}
    instructions[155] = {5'd14, 6'd0, 6'd0, 32'd116};//{'label': 116, 'op': 'goto'}
    instructions[156] = {5'd4, 6'd1, 6'd26, 32'd0};//{'dest': 1, 'src': 26, 'op': 'move'}
    instructions[157] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[158] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[159] = {5'd4, 6'd24, 6'd1, 32'd0};//{'dest': 24, 'src': 1, 'op': 'move'}
    instructions[160] = {5'd5, 6'd0, 6'd23, 32'd0};//{'src': 23, 'op': 'jmp_to_reg'}
    instructions[161] = {5'd7, 6'd28, 6'd0, 32'd0};//{'dest': 28, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[162] = {5'd7, 6'd29, 6'd0, 32'd0};//{'dest': 29, 'literal': 0, 'size': 2, 'signed': 2, 'op': 'literal'}
    instructions[163] = {5'd7, 6'd30, 6'd0, 32'd2};//{'dest': 30, 'literal': 2, 'op': 'literal'}
    instructions[164] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[165] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[166] = {5'd4, 6'd5, 6'd30, 32'd0};//{'dest': 5, 'src': 30, 'op': 'move'}
    instructions[167] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[168] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[169] = {5'd4, 6'd18, 6'd5, 32'd0};//{'dest': 18, 'src': 5, 'op': 'move'}
    instructions[170] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[171] = {5'd7, 6'd31, 6'd0, 32'd20};//{'dest': 31, 'literal': 20, 'op': 'literal'}
    instructions[172] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[173] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[174] = {5'd4, 6'd6, 6'd31, 32'd0};//{'dest': 6, 'src': 31, 'op': 'move'}
    instructions[175] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[176] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[177] = {5'd4, 6'd18, 6'd6, 32'd0};//{'dest': 18, 'src': 6, 'op': 'move'}
    instructions[178] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[179] = {5'd7, 6'd32, 6'd0, 32'd39};//{'dest': 32, 'literal': 39, 'op': 'literal'}
    instructions[180] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[181] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[182] = {5'd4, 6'd7, 6'd32, 32'd0};//{'dest': 7, 'src': 32, 'op': 'move'}
    instructions[183] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[184] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[185] = {5'd4, 6'd18, 6'd7, 32'd0};//{'dest': 18, 'src': 7, 'op': 'move'}
    instructions[186] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[187] = {5'd7, 6'd33, 6'd0, 32'd51};//{'dest': 33, 'literal': 51, 'op': 'literal'}
    instructions[188] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[189] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[190] = {5'd4, 6'd8, 6'd33, 32'd0};//{'dest': 8, 'src': 33, 'op': 'move'}
    instructions[191] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[192] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[193] = {5'd4, 6'd18, 6'd8, 32'd0};//{'dest': 18, 'src': 8, 'op': 'move'}
    instructions[194] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[195] = {5'd7, 6'd34, 6'd0, 32'd72};//{'dest': 34, 'literal': 72, 'op': 'literal'}
    instructions[196] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[197] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[198] = {5'd4, 6'd9, 6'd34, 32'd0};//{'dest': 9, 'src': 34, 'op': 'move'}
    instructions[199] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[200] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[201] = {5'd4, 6'd18, 6'd9, 32'd0};//{'dest': 18, 'src': 9, 'op': 'move'}
    instructions[202] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[203] = {5'd0, 6'd23, 6'd0, 32'd73};//{'dest': 23, 'label': 73, 'op': 'jmp_and_link'}
    instructions[204] = {5'd4, 6'd1, 6'd24, 32'd0};//{'dest': 1, 'src': 24, 'op': 'move'}
    instructions[205] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[206] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[207] = {5'd4, 6'd28, 6'd1, 32'd0};//{'dest': 28, 'src': 1, 'op': 'move'}
    instructions[208] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[209] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[210] = {5'd4, 6'd2, 6'd28, 32'd0};//{'dest': 2, 'src': 28, 'op': 'move'}
    instructions[211] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[212] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[213] = {5'd20, 6'd1, 6'd2, 32'd0};//{'src': 2, 'right': 0, 'dest': 1, 'signed': False, 'op': '>=', 'type': 'int', 'size': 2}
    instructions[214] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[215] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[216] = {5'd12, 6'd0, 6'd1, 32'd221};//{'src': 1, 'label': 221, 'op': 'jmp_if_false'}
    instructions[217] = {5'd4, 6'd2, 6'd28, 32'd0};//{'dest': 2, 'src': 28, 'op': 'move'}
    instructions[218] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[219] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[220] = {5'd21, 6'd1, 6'd2, 32'd7};//{'src': 2, 'right': 7, 'dest': 1, 'signed': False, 'op': '<=', 'type': 'int', 'size': 2}
    instructions[221] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[222] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[223] = {5'd12, 6'd0, 6'd1, 32'd226};//{'src': 1, 'label': 226, 'op': 'jmp_if_false'}
    instructions[224] = {5'd14, 6'd0, 6'd0, 32'd235};//{'label': 235, 'op': 'goto'}
    instructions[225] = {5'd14, 6'd0, 6'd0, 32'd234};//{'label': 234, 'op': 'goto'}
    instructions[226] = {5'd7, 6'd35, 6'd0, 32'd76};//{'dest': 35, 'literal': 76, 'op': 'literal'}
    instructions[227] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[228] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[229] = {5'd4, 6'd10, 6'd35, 32'd0};//{'dest': 10, 'src': 35, 'op': 'move'}
    instructions[230] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[231] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[232] = {5'd4, 6'd18, 6'd10, 32'd0};//{'dest': 18, 'src': 10, 'op': 'move'}
    instructions[233] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[234] = {5'd14, 6'd0, 6'd0, 32'd187};//{'label': 187, 'op': 'goto'}
    instructions[235] = {5'd7, 6'd36, 6'd0, 32'd108};//{'dest': 36, 'literal': 108, 'op': 'literal'}
    instructions[236] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[237] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[238] = {5'd4, 6'd11, 6'd36, 32'd0};//{'dest': 11, 'src': 36, 'op': 'move'}
    instructions[239] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[240] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[241] = {5'd4, 6'd18, 6'd11, 32'd0};//{'dest': 18, 'src': 11, 'op': 'move'}
    instructions[242] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[243] = {5'd7, 6'd37, 6'd0, 32'd137};//{'dest': 37, 'literal': 137, 'op': 'literal'}
    instructions[244] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[245] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[246] = {5'd4, 6'd9, 6'd37, 32'd0};//{'dest': 9, 'src': 37, 'op': 'move'}
    instructions[247] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[248] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[249] = {5'd4, 6'd18, 6'd9, 32'd0};//{'dest': 18, 'src': 9, 'op': 'move'}
    instructions[250] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[251] = {5'd4, 6'd2, 6'd29, 32'd0};//{'dest': 2, 'src': 29, 'op': 'move'}
    instructions[252] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[253] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[254] = {5'd20, 6'd1, 6'd2, 32'd0};//{'src': 2, 'right': 0, 'dest': 1, 'signed': False, 'op': '>=', 'type': 'int', 'size': 2}
    instructions[255] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[256] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[257] = {5'd12, 6'd0, 6'd1, 32'd262};//{'src': 1, 'label': 262, 'op': 'jmp_if_false'}
    instructions[258] = {5'd4, 6'd2, 6'd29, 32'd0};//{'dest': 2, 'src': 29, 'op': 'move'}
    instructions[259] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[260] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[261] = {5'd21, 6'd1, 6'd2, 32'd7};//{'src': 2, 'right': 7, 'dest': 1, 'signed': False, 'op': '<=', 'type': 'int', 'size': 2}
    instructions[262] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[263] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[264] = {5'd12, 6'd0, 6'd1, 32'd267};//{'src': 1, 'label': 267, 'op': 'jmp_if_false'}
    instructions[265] = {5'd14, 6'd0, 6'd0, 32'd276};//{'label': 276, 'op': 'goto'}
    instructions[266] = {5'd14, 6'd0, 6'd0, 32'd275};//{'label': 275, 'op': 'goto'}
    instructions[267] = {5'd7, 6'd0, 6'd0, 32'd141};//{'dest': 0, 'literal': 141, 'op': 'literal'}
    instructions[268] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[269] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[270] = {5'd4, 6'd12, 6'd0, 32'd0};//{'dest': 12, 'src': 0, 'op': 'move'}
    instructions[271] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[272] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[273] = {5'd4, 6'd18, 6'd12, 32'd0};//{'dest': 18, 'src': 12, 'op': 'move'}
    instructions[274] = {5'd0, 6'd17, 6'd0, 32'd12};//{'dest': 17, 'label': 12, 'op': 'jmp_and_link'}
    instructions[275] = {5'd14, 6'd0, 6'd0, 32'd235};//{'label': 235, 'op': 'goto'}
    instructions[276] = {5'd4, 6'd1, 6'd28, 32'd0};//{'dest': 1, 'src': 28, 'op': 'move'}
    instructions[277] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[278] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[279] = {5'd22, 6'd0, 6'd1, 32'd0};//{'src': 1, 'output': 'control', 'op': 'write'}
    instructions[280] = {5'd4, 6'd1, 6'd29, 32'd0};//{'dest': 1, 'src': 29, 'op': 'move'}
    instructions[281] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[282] = {5'd3, 6'd0, 6'd0, 32'd0};//{'op': 'nop'}
    instructions[283] = {5'd22, 6'd0, 6'd1, 32'd0};//{'src': 1, 'output': 'control', 'op': 'write'}
    instructions[284] = {5'd14, 6'd0, 6'd0, 32'd187};//{'label': 187, 'op': 'goto'}
    instructions[285] = {5'd5, 6'd0, 6'd27, 32'd0};//{'src': 27, 'op': 'jmp_to_reg'}
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
      opcode_0 = instruction_0[48:44];
      dest_0 = instruction_0[43:38];
      src_0 = instruction_0[37:32];
      srcb_0 = instruction_0[5:0];
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
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          s_input_rs232_ack <= 1'b1;
        end

        16'd4:
        begin
          result_2 <= register_1;
          write_enable_2 <= 1;
        end

        16'd5:
        begin
          program_counter <= register_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd6:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          s_output_rs232_stb <= 1'b1;
          s_output_rs232 <= register_1;
        end

        16'd7:
        begin
          result_2 <= literal_1;
          write_enable_2 <= 1;
        end

        16'd8:
        begin
          result_2 <= $unsigned(register_1) + $unsigned(registerb_1);
          write_enable_2 <= 1;
        end

        16'd9:
        begin
          address_2 <= register_1;
        end

        16'd11:
        begin
          result_2 <= data_out_2;
          write_enable_2 <= 1;
        end

        16'd12:
        begin
          if (register_1 == 0) begin
            program_counter <= literal_1;
            stage_0_enable <= 1;
            stage_1_enable <= 0;
            stage_2_enable <= 0;
          end
        end

        16'd13:
        begin
          result_2 <= $unsigned(register_1) + $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd14:
        begin
          program_counter <= literal_1;
          stage_0_enable <= 1;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
        end

        16'd15:
        begin
          result_2 <= $signed(register_1) >= $signed(literal_1);
          write_enable_2 <= 1;
        end

        16'd16:
        begin
          result_2 <= $signed(register_1) <= $signed(literal_1);
          write_enable_2 <= 1;
        end

        16'd17:
        begin
          result_2 <= $unsigned(register_1) == $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd18:
        begin
          result_2 <= $unsigned(register_1) - $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd19:
        begin
          result_2 <= $signed(register_1) * $signed(literal_1);
          write_enable_2 <= 1;
        end

        16'd20:
        begin
          result_2 <= $unsigned(register_1) >= $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd21:
        begin
          result_2 <= $unsigned(register_1) <= $unsigned(literal_1);
          write_enable_2 <= 1;
        end

        16'd22:
        begin
          stage_0_enable <= 0;
          stage_1_enable <= 0;
          stage_2_enable <= 0;
          s_output_control_stb <= 1'b1;
          s_output_control <= register_1;
        end

       endcase
    end
    if (s_input_rs232_ack == 1'b1 && input_rs232_stb == 1'b1) begin
       result_2 <= input_rs232;
       write_enable_2 <= 1;
       s_input_rs232_ack <= 1'b0;
       stage_0_enable <= 1;
       stage_1_enable <= 1;
       stage_2_enable <= 1;
     end

     if (s_output_rs232_stb == 1'b1 && output_rs232_ack == 1'b1) begin
       s_output_rs232_stb <= 1'b0;
       stage_0_enable <= 1;
       stage_1_enable <= 1;
       stage_2_enable <= 1;
     end

     if (s_output_control_stb == 1'b1 && output_control_ack == 1'b1) begin
       s_output_control_stb <= 1'b0;
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
      s_input_rs232_ack <= 0;
      s_output_control_stb <= 0;
      s_output_rs232_stb <= 0;
    end
  end
  assign input_rs232_ack = s_input_rs232_ack;
  assign output_control_stb = s_output_control_stb;
  assign output_control = s_output_control;
  assign output_rs232_stb = s_output_rs232_stb;
  assign output_rs232 = s_output_rs232;

endmodule
