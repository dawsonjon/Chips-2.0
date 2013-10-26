//name : user_design
//tag : c components
//input : input_checksum:16
//input : input_eth_rx:16
//input : input_rs232_rx:16
//output : output_rs232_tx:16
//output : output_leds:16
//output : output_eth_tx:16
//output : output_checksum:16
//source_file : source/user_design.c
///User_Design
///===========
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module user_design(input_checksum,input_eth_rx,input_rs232_rx,input_checksum_stb,input_eth_rx_stb,input_rs232_rx_stb,output_rs232_tx_ack,output_leds_ack,output_eth_tx_ack,output_checksum_ack,clk,rst,output_rs232_tx,output_leds,output_eth_tx,output_checksum,output_rs232_tx_stb,output_leds_stb,output_eth_tx_stb,output_checksum_stb,input_checksum_ack,input_eth_rx_ack,input_rs232_rx_ack);
  input     [15:0] input_checksum;
  input     [15:0] input_eth_rx;
  input     [15:0] input_rs232_rx;
  input     input_checksum_stb;
  input     input_eth_rx_stb;
  input     input_rs232_rx_stb;
  input     output_rs232_tx_ack;
  input     output_leds_ack;
  input     output_eth_tx_ack;
  input     output_checksum_ack;
  input     clk;
  input     rst;
  output    [15:0] output_rs232_tx;
  output    [15:0] output_leds;
  output    [15:0] output_eth_tx;
  output    [15:0] output_checksum;
  output    output_rs232_tx_stb;
  output    output_leds_stb;
  output    output_eth_tx_stb;
  output    output_checksum_stb;
  output    input_checksum_ack;
  output    input_eth_rx_ack;
  output    input_rs232_rx_ack;
  reg       [15:0] timer;
  reg       [9:0] program_counter;
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
  reg       [15:0] register_8;
  reg       [15:0] register_9;
  reg       [15:0] register_10;
  reg       [15:0] register_11;
  reg       [15:0] register_12;
  reg       [15:0] register_13;
  reg       [15:0] register_14;
  reg       [15:0] register_15;
  reg       [15:0] register_16;
  reg       [15:0] register_17;
  reg       [15:0] register_18;
  reg       [15:0] register_19;
  reg       [15:0] register_20;
  reg       [15:0] register_21;
  reg       [15:0] register_22;
  reg       [15:0] register_23;
  reg       [15:0] register_24;
  reg       [15:0] register_25;
  reg       [15:0] register_26;
  reg       [15:0] register_27;
  reg       [15:0] register_28;
  reg       [15:0] register_29;
  reg       [15:0] register_30;
  reg       [15:0] register_31;
  reg       [15:0] register_32;
  reg       [15:0] register_33;
  reg       [15:0] register_34;
  reg       [15:0] register_35;
  reg       [15:0] register_36;
  reg       [15:0] register_37;
  reg       [15:0] register_38;
  reg       [15:0] register_39;
  reg       [15:0] register_40;
  reg       [15:0] register_41;
  reg       [15:0] register_42;
  reg       [15:0] register_43;
  reg       [15:0] register_44;
  reg       [15:0] register_45;
  reg       [15:0] register_46;
  reg       [15:0] register_47;
  reg       [15:0] register_48;
  reg       [15:0] register_49;
  reg       [15:0] register_50;
  reg       [15:0] register_51;
  reg       [15:0] register_52;
  reg       [15:0] register_53;
  reg       [15:0] register_54;
  reg       [15:0] register_55;
  reg       [15:0] register_56;
  reg       [15:0] register_57;
  reg       [15:0] register_58;
  reg       [15:0] register_59;
  reg       [15:0] register_60;
  reg       [15:0] register_61;
  reg       [15:0] register_62;
  reg       [15:0] register_63;
  reg       [15:0] register_64;
  reg       [15:0] register_65;
  reg       [15:0] register_66;
  reg       [15:0] register_67;
  reg       [15:0] register_68;
  reg       [15:0] register_69;
  reg       [15:0] register_70;
  reg       [15:0] register_71;
  reg       [15:0] register_72;
  reg       [15:0] register_73;
  reg       [15:0] register_74;
  reg       [15:0] register_75;
  reg       [15:0] register_76;
  reg       [15:0] register_77;
  reg       [15:0] register_78;
  reg       [15:0] register_79;
  reg       [15:0] register_80;
  reg       [15:0] register_81;
  reg       [15:0] register_82;
  reg       [15:0] register_83;
  reg       [15:0] register_84;
  reg       [15:0] register_85;
  reg       [15:0] register_86;
  reg       [15:0] register_87;
  reg       [15:0] register_88;
  reg       [15:0] register_89;
  reg       [15:0] register_90;
  reg       [15:0] register_91;
  reg       [15:0] register_92;
  reg       [15:0] register_93;
  reg       [15:0] register_94;
  reg       [15:0] register_95;
  reg       [15:0] register_96;
  reg       [15:0] register_97;
  reg       [15:0] register_98;
  reg       [15:0] register_99;
  reg       [15:0] register_100;
  reg       [15:0] register_101;
  reg       [15:0] register_102;
  reg       [15:0] register_103;
  reg       [15:0] register_104;
  reg       [15:0] register_105;
  reg       [15:0] register_106;
  reg       [15:0] register_107;
  reg       [15:0] register_108;
  reg       [15:0] register_109;
  reg       [15:0] register_110;
  reg       [15:0] register_111;
  reg       [15:0] register_112;
  reg       [15:0] register_113;
  reg       [15:0] register_114;
  reg       [15:0] register_115;
  reg       [15:0] register_116;
  reg       [15:0] register_117;
  reg       [15:0] register_118;
  reg       [15:0] register_119;
  reg       [15:0] register_120;
  reg       [15:0] register_121;
  reg       [15:0] register_122;
  reg       [15:0] register_123;
  reg       [15:0] register_124;
  reg       [15:0] register_125;
  reg       [15:0] register_126;
  reg       [15:0] register_127;
  reg       [15:0] register_128;
  reg       [15:0] register_129;
  reg       [15:0] register_130;
  reg       [15:0] register_131;
  reg       [15:0] register_132;
  reg       [15:0] register_133;
  reg       [15:0] register_134;
  reg       [15:0] register_135;
  reg       [15:0] register_136;
  reg       [15:0] register_137;
  reg       [15:0] register_138;
  reg       [15:0] register_139;
  reg       [15:0] register_140;
  reg       [15:0] register_141;
  reg       [15:0] register_142;
  reg       [15:0] register_143;
  reg       [15:0] register_144;
  reg       [15:0] register_145;
  reg       [15:0] register_146;
  reg       [15:0] register_147;
  reg       [15:0] register_148;
  reg       [15:0] register_149;
  reg       [15:0] register_150;
  reg       [15:0] register_151;
  reg       [15:0] register_152;
  reg       [15:0] register_153;
  reg       [15:0] s_output_rs232_tx_stb;
  reg       [15:0] s_output_leds_stb;
  reg       [15:0] s_output_eth_tx_stb;
  reg       [15:0] s_output_checksum_stb;
  reg       [15:0] s_output_rs232_tx;
  reg       [15:0] s_output_leds;
  reg       [15:0] s_output_eth_tx;
  reg       [15:0] s_output_checksum;
  reg       [15:0] s_input_checksum_ack;
  reg       [15:0] s_input_eth_rx_ack;
  reg       [15:0] s_input_rs232_rx_ack;
  reg [15:0] memory [2881:0];

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
    memory[16'd512] = 16'd112;
    memory[16'd513] = 16'd117;
    memory[16'd514] = 16'd116;
    memory[16'd515] = 16'd95;
    memory[16'd516] = 16'd101;
    memory[16'd517] = 16'd116;
    memory[16'd518] = 16'd104;
    memory[16'd519] = 16'd10;
    memory[16'd520] = 16'd0;
    memory[16'd521] = 16'd103;
    memory[16'd522] = 16'd101;
    memory[16'd523] = 16'd116;
    memory[16'd524] = 16'd95;
    memory[16'd525] = 16'd101;
    memory[16'd526] = 16'd116;
    memory[16'd527] = 16'd104;
    memory[16'd528] = 16'd10;
    memory[16'd529] = 16'd0;
    memory[16'd626] = 16'd112;
    memory[16'd627] = 16'd117;
    memory[16'd628] = 16'd116;
    memory[16'd629] = 16'd95;
    memory[16'd630] = 16'd105;
    memory[16'd631] = 16'd112;
    memory[16'd632] = 16'd10;
    memory[16'd633] = 16'd0;
    memory[16'd634] = 16'd103;
    memory[16'd635] = 16'd101;
    memory[16'd636] = 16'd116;
    memory[16'd637] = 16'd95;
    memory[16'd638] = 16'd105;
    memory[16'd639] = 16'd112;
    memory[16'd640] = 16'd10;
    memory[16'd641] = 16'd0;
    memory[16'd650] = 16'd112;
    memory[16'd651] = 16'd117;
    memory[16'd652] = 16'd116;
    memory[16'd653] = 16'd32;
    memory[16'd654] = 16'd116;
    memory[16'd655] = 16'd99;
    memory[16'd656] = 16'd112;
    memory[16'd657] = 16'd10;
    memory[16'd658] = 16'd0;
    memory[16'd659] = 16'd103;
    memory[16'd660] = 16'd101;
    memory[16'd661] = 16'd116;
    memory[16'd662] = 16'd32;
    memory[16'd663] = 16'd116;
    memory[16'd664] = 16'd99;
    memory[16'd665] = 16'd112;
    memory[16'd666] = 16'd10;
    memory[16'd667] = 16'd0;
    memory[16'd668] = 16'd116;
    memory[16'd669] = 16'd99;
    memory[16'd670] = 16'd112;
    memory[16'd671] = 16'd95;
    memory[16'd672] = 16'd104;
    memory[16'd673] = 16'd101;
    memory[16'd674] = 16'd97;
    memory[16'd675] = 16'd100;
    memory[16'd676] = 16'd101;
    memory[16'd677] = 16'd114;
    memory[16'd678] = 16'd95;
    memory[16'd679] = 16'd108;
    memory[16'd680] = 16'd101;
    memory[16'd681] = 16'd110;
    memory[16'd682] = 16'd103;
    memory[16'd683] = 16'd116;
    memory[16'd684] = 16'd104;
    memory[16'd685] = 16'd32;
    memory[16'd686] = 16'd0;
    memory[16'd687] = 16'd10;
    memory[16'd688] = 16'd0;
    memory[16'd689] = 16'd114;
    memory[16'd690] = 16'd120;
    memory[16'd691] = 16'd95;
    memory[16'd692] = 16'd108;
    memory[16'd693] = 16'd101;
    memory[16'd694] = 16'd110;
    memory[16'd695] = 16'd103;
    memory[16'd696] = 16'd116;
    memory[16'd697] = 16'd104;
    memory[16'd698] = 16'd32;
    memory[16'd699] = 16'd0;
    memory[16'd700] = 16'd10;
    memory[16'd701] = 16'd0;
    memory[16'd702] = 16'd101;
    memory[16'd703] = 16'd99;
    memory[16'd704] = 16'd104;
    memory[16'd705] = 16'd111;
    memory[16'd706] = 16'd32;
    memory[16'd707] = 16'd100;
    memory[16'd708] = 16'd97;
    memory[16'd709] = 16'd116;
    memory[16'd710] = 16'd97;
    memory[16'd711] = 16'd58;
    memory[16'd712] = 16'd10;
    memory[16'd713] = 16'd0;
    memory[16'd714] = 16'd10;
    memory[16'd715] = 16'd0;
    memory[16'd2764] = 16'd10;
    memory[16'd2765] = 16'd69;
    memory[16'd2766] = 16'd116;
    memory[16'd2767] = 16'd104;
    memory[16'd2768] = 16'd101;
    memory[16'd2769] = 16'd114;
    memory[16'd2770] = 16'd110;
    memory[16'd2771] = 16'd101;
    memory[16'd2772] = 16'd116;
    memory[16'd2773] = 16'd32;
    memory[16'd2774] = 16'd77;
    memory[16'd2775] = 16'd111;
    memory[16'd2776] = 16'd110;
    memory[16'd2777] = 16'd105;
    memory[16'd2778] = 16'd116;
    memory[16'd2779] = 16'd111;
    memory[16'd2780] = 16'd114;
    memory[16'd2781] = 16'd10;
    memory[16'd2782] = 16'd0;
    memory[16'd2783] = 16'd105;
    memory[16'd2784] = 16'd110;
    memory[16'd2785] = 16'd99;
    memory[16'd2786] = 16'd111;
    memory[16'd2787] = 16'd109;
    memory[16'd2788] = 16'd109;
    memory[16'd2789] = 16'd105;
    memory[16'd2790] = 16'd110;
    memory[16'd2791] = 16'd103;
    memory[16'd2792] = 16'd32;
    memory[16'd2793] = 16'd99;
    memory[16'd2794] = 16'd111;
    memory[16'd2795] = 16'd110;
    memory[16'd2796] = 16'd110;
    memory[16'd2797] = 16'd101;
    memory[16'd2798] = 16'd99;
    memory[16'd2799] = 16'd116;
    memory[16'd2800] = 16'd105;
    memory[16'd2801] = 16'd111;
    memory[16'd2802] = 16'd110;
    memory[16'd2803] = 16'd32;
    memory[16'd2804] = 16'd102;
    memory[16'd2805] = 16'd114;
    memory[16'd2806] = 16'd111;
    memory[16'd2807] = 16'd109;
    memory[16'd2808] = 16'd58;
    memory[16'd2809] = 16'd32;
    memory[16'd2810] = 16'd0;
    memory[16'd2811] = 16'd10;
    memory[16'd2812] = 16'd0;
    memory[16'd2813] = 16'd119;
    memory[16'd2814] = 16'd97;
    memory[16'd2815] = 16'd105;
    memory[16'd2816] = 16'd116;
    memory[16'd2817] = 16'd105;
    memory[16'd2818] = 16'd110;
    memory[16'd2819] = 16'd103;
    memory[16'd2820] = 16'd32;
    memory[16'd2821] = 16'd102;
    memory[16'd2822] = 16'd111;
    memory[16'd2823] = 16'd114;
    memory[16'd2824] = 16'd32;
    memory[16'd2825] = 16'd97;
    memory[16'd2826] = 16'd99;
    memory[16'd2827] = 16'd107;
    memory[16'd2828] = 16'd110;
    memory[16'd2829] = 16'd111;
    memory[16'd2830] = 16'd119;
    memory[16'd2831] = 16'd108;
    memory[16'd2832] = 16'd101;
    memory[16'd2833] = 16'd100;
    memory[16'd2834] = 16'd103;
    memory[16'd2835] = 16'd101;
    memory[16'd2836] = 16'd109;
    memory[16'd2837] = 16'd101;
    memory[16'd2838] = 16'd110;
    memory[16'd2839] = 16'd116;
    memory[16'd2840] = 16'd10;
    memory[16'd2841] = 16'd0;
    memory[16'd2842] = 16'd99;
    memory[16'd2843] = 16'd111;
    memory[16'd2844] = 16'd110;
    memory[16'd2845] = 16'd110;
    memory[16'd2846] = 16'd101;
    memory[16'd2847] = 16'd99;
    memory[16'd2848] = 16'd116;
    memory[16'd2849] = 16'd105;
    memory[16'd2850] = 16'd111;
    memory[16'd2851] = 16'd110;
    memory[16'd2852] = 16'd32;
    memory[16'd2853] = 16'd101;
    memory[16'd2854] = 16'd115;
    memory[16'd2855] = 16'd116;
    memory[16'd2856] = 16'd97;
    memory[16'd2857] = 16'd98;
    memory[16'd2858] = 16'd108;
    memory[16'd2859] = 16'd105;
    memory[16'd2860] = 16'd115;
    memory[16'd2861] = 16'd104;
    memory[16'd2862] = 16'd101;
    memory[16'd2863] = 16'd100;
    memory[16'd2864] = 16'd10;
    memory[16'd2865] = 16'd0;
    memory[16'd2866] = 16'd105;
    memory[16'd2867] = 16'd110;
    memory[16'd2868] = 16'd99;
    memory[16'd2869] = 16'd111;
    memory[16'd2870] = 16'd109;
    memory[16'd2871] = 16'd105;
    memory[16'd2872] = 16'd110;
    memory[16'd2873] = 16'd103;
    memory[16'd2874] = 16'd32;
    memory[16'd2875] = 16'd100;
    memory[16'd2876] = 16'd97;
    memory[16'd2877] = 16'd116;
    memory[16'd2878] = 16'd97;
    memory[16'd2879] = 16'd58;
    memory[16'd2880] = 16'd10;
    memory[16'd2881] = 16'd0;
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
        register_0 <= 16'd1;
        register_1 <= 16'd515;
        register_2 <= 16'd1029;
        register_3 <= 16'd49320;
        register_4 <= 16'd257;
        register_5 <= 16'd23;
        register_6 <= 16'd0;
        register_40 <= 16'd530;
        register_41 <= 16'd546;
        register_42 <= 16'd562;
        register_43 <= 16'd578;
        register_44 <= 16'd594;
        register_45 <= 16'd0;
        register_78 <= 16'd0;
        register_79 <= 16'd0;
        register_80 <= 16'd0;
        register_81 <= 16'd0;
        register_82 <= 16'd642;
        register_83 <= 16'd644;
        register_84 <= 16'd255;
        register_85 <= 16'd0;
        register_86 <= 16'd0;
        register_87 <= 16'd0;
        register_88 <= 16'd0;
        register_89 <= 16'd0;
        register_90 <= 16'd0;
        register_91 <= 16'd0;
        register_92 <= 16'd0;
        register_93 <= 16'd646;
        register_94 <= 16'd648;
        register_95 <= 16'd0;
        register_96 <= 16'd0;
        register_97 <= 16'd0;
        register_98 <= 16'd0;
        register_99 <= 16'd0;
        register_100 <= 16'd0;
        register_101 <= 16'd0;
        register_111 <= 16'd0;
        register_112 <= 16'd0;
        program_counter <= 16'd900;
        register_137 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_10 <= 16'd0;
      end

      16'd3:
      begin
        register_152 <= register_10;
      end

      16'd4:
      begin
        register_152 <= $signed(register_152) + $signed(register_9);
      end

      16'd5:
      begin
        address <= register_152;
      end

      16'd6:
      begin
        register_152 <= data_out;
      end

      16'd7:
      begin
        register_152 <= data_out;
      end

      16'd8:
      begin
        register_152 <= $signed(register_152) != $signed(16'd0);
      end

      16'd9:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 19;
      end

      16'd10:
      begin
        register_152 <= register_10;
      end

      16'd11:
      begin
        register_152 <= $signed(register_152) + $signed(register_9);
      end

      16'd12:
      begin
        address <= register_152;
      end

      16'd13:
      begin
        register_152 <= data_out;
      end

      16'd14:
      begin
        register_152 <= data_out;
      end

      16'd15:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 15;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        register_152 <= register_10;
      end

      16'd17:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd18:
      begin
        register_10 <= register_152;
        program_counter <= 16'd20;
      end

      16'd19:
      begin
        program_counter <= 16'd21;
      end

      16'd20:
      begin
        program_counter <= 16'd3;
      end

      16'd21:
      begin
        register_8 <= 16'd0;
        program_counter <= register_7;
      end

      16'd22:
      begin
        register_152 <= register_13;
      end

      16'd23:
      begin
        register_152 <= $signed(register_152) > $signed(16'd9);
      end

      16'd24:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 28;
      end

      16'd25:
      begin
        register_12 <= register_13;
      end

      16'd26:
      begin
        register_12 <= $signed(register_12) + $signed(16'd87);
        program_counter <= register_11;
      end

      16'd27:
      begin
        program_counter <= 16'd28;
      end

      16'd28:
      begin
        register_12 <= register_13;
      end

      16'd29:
      begin
        register_12 <= $signed(register_12) + $signed(16'd48);
        program_counter <= register_11;
      end

      16'd30:
      begin
        register_13 <= register_16;
      end

      16'd31:
      begin
        register_13 <= $signed(register_13) >>> $signed(16'd12);
      end

      16'd32:
      begin
        register_13 <= $signed(register_13) & $signed(16'd15);
        program_counter <= 16'd22;
        register_11 <= 16'd33;
      end

      16'd33:
      begin
        register_152 <= register_12;
      end

      16'd34:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 34;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 35;
        end
      end

      16'd35:
      begin
        register_13 <= register_16;
      end

      16'd36:
      begin
        register_13 <= $signed(register_13) >>> $signed(16'd8);
      end

      16'd37:
      begin
        register_13 <= $signed(register_13) & $signed(16'd15);
        program_counter <= 16'd22;
        register_11 <= 16'd38;
      end

      16'd38:
      begin
        register_152 <= register_12;
      end

      16'd39:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 39;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 40;
        end
      end

      16'd40:
      begin
        register_152 <= 16'd32;
      end

      16'd41:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 41;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 42;
        end
      end

      16'd42:
      begin
        register_13 <= register_16;
      end

      16'd43:
      begin
        register_13 <= $signed(register_13) >>> $signed(16'd4);
      end

      16'd44:
      begin
        register_13 <= $signed(register_13) & $signed(16'd15);
        program_counter <= 16'd22;
        register_11 <= 16'd45;
      end

      16'd45:
      begin
        register_152 <= register_12;
      end

      16'd46:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 46;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 47;
        end
      end

      16'd47:
      begin
        register_13 <= register_16;
      end

      16'd48:
      begin
        register_13 <= $signed(register_13) & $signed(16'd15);
        program_counter <= 16'd22;
        register_11 <= 16'd49;
      end

      16'd49:
      begin
        register_152 <= register_12;
      end

      16'd50:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 50;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 51;
        end
      end

      16'd51:
      begin
        register_152 <= 16'd32;
      end

      16'd52:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 52;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 53;
        end
      end

      16'd53:
      begin
        register_15 <= 16'd0;
        program_counter <= register_14;
      end

      16'd54:
      begin
        register_152 <= 16'd0;
        register_153 <= register_21;
      end

      16'd55:
      begin
        register_152 <= $signed(register_152) + $signed(register_20);
      end

      16'd56:
      begin
        address <= register_152;
      end

      16'd57:
      begin
        register_152 <= data_out;
      end

      16'd58:
      begin
        register_152 <= data_out;
      end

      16'd59:
      begin
        register_152 <= $signed(register_152) + $signed(register_153);
        register_153 <= 16'd0;
      end

      16'd60:
      begin
        register_153 <= $signed(register_153) + $signed(register_19);
      end

      16'd61:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1;
        register_153 <= 16'd1;
      end

      16'd62:
      begin
        register_152 <= $signed(register_152) + $signed(register_20);
        register_153 <= $signed(register_153) + $signed(register_19);
      end

      16'd63:
      begin
        address <= register_152;
      end

      16'd64:
      begin
        register_152 <= data_out;
      end

      16'd65:
      begin
        register_152 <= data_out;
      end

      16'd66:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= register_21;
      end

      16'd67:
      begin
        register_152 <= $signed(register_152) + $signed(register_20);
      end

      16'd68:
      begin
        address <= register_152;
      end

      16'd69:
      begin
        register_152 <= data_out;
      end

      16'd70:
      begin
        register_152 <= data_out;
      end

      16'd71:
      begin
        register_152 <= $signed(register_152) | $signed(register_153);
      end

      16'd72:
      begin
        register_152 <= $signed(register_152) & $signed(16'd32768);
      end

      16'd73:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 90;
      end

      16'd74:
      begin
        register_152 <= 16'd0;
      end

      16'd75:
      begin
        register_152 <= $signed(register_152) + $signed(register_19);
      end

      16'd76:
      begin
        address <= register_152;
      end

      16'd77:
      begin
        register_152 <= data_out;
      end

      16'd78:
      begin
        register_152 <= data_out;
      end

      16'd79:
      begin
        register_152 <= $signed(register_152) & $signed(16'd32768);
      end

      16'd80:
      begin
        register_152 <= $signed(register_152) == $signed(16'd0);
      end

      16'd81:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 89;
      end

      16'd82:
      begin
        register_152 <= 16'd1;
        register_153 <= 16'd1;
      end

      16'd83:
      begin
        register_152 <= $signed(register_152) + $signed(register_19);
        register_153 <= $signed(register_153) + $signed(register_19);
      end

      16'd84:
      begin
        address <= register_152;
      end

      16'd85:
      begin
        register_152 <= data_out;
      end

      16'd86:
      begin
        register_152 <= data_out;
      end

      16'd87:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd88:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd89;
      end

      16'd89:
      begin
        program_counter <= 16'd90;
      end

      16'd90:
      begin
        register_18 <= 16'd0;
        program_counter <= register_17;
      end

      16'd91:
      begin
        register_30 <= 16'd0;
        register_31 <= 16'd0;
        register_32 <= 16'd512;
      end

      16'd92:
      begin
        register_9 <= register_32;
        program_counter <= 16'd2;
        register_7 <= 16'd93;
      end

      16'd93:
      begin
        register_152 <= register_8;
        register_153 <= 16'd0;
      end

      16'd94:
      begin
        register_152 <= register_26;
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd95:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_27;
        register_153 <= 16'd1;
      end

      16'd96:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd97:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_28;
        register_153 <= 16'd2;
      end

      16'd98:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd99:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_0;
        register_153 <= 16'd3;
      end

      16'd100:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd101:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_1;
        register_153 <= 16'd4;
      end

      16'd102:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd103:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_2;
        register_153 <= 16'd5;
      end

      16'd104:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd105:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_29;
        register_153 <= 16'd6;
      end

      16'd106:
      begin
        register_153 <= $signed(register_153) + $signed(register_24);
      end

      16'd107:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_25;
      end

      16'd108:
      begin
        s_output_eth_tx <= register_152;
        program_counter <= 108;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 109;
        end
      end

      16'd109:
      begin
        register_152 <= 16'd0;
      end

      16'd110:
      begin
        register_31 <= register_152;
        register_152 <= 16'd0;
      end

      16'd111:
      begin
        register_30 <= register_152;
      end

      16'd112:
      begin
        register_152 <= register_30;
        register_153 <= register_25;
      end

      16'd113:
      begin
        register_152 <= $signed(register_152) < $signed(register_153);
      end

      16'd114:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 127;
      end

      16'd115:
      begin
        register_152 <= register_31;
      end

      16'd116:
      begin
        register_152 <= $signed(register_152) + $signed(register_24);
      end

      16'd117:
      begin
        address <= register_152;
      end

      16'd118:
      begin
        register_152 <= data_out;
      end

      16'd119:
      begin
        register_152 <= data_out;
      end

      16'd120:
      begin
        s_output_eth_tx <= register_152;
        program_counter <= 120;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 121;
        end
      end

      16'd121:
      begin
        register_152 <= register_31;
      end

      16'd122:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd123:
      begin
        register_31 <= register_152;
      end

      16'd124:
      begin
        register_152 <= register_30;
      end

      16'd125:
      begin
        register_152 <= $signed(register_152) + $signed(16'd2);
      end

      16'd126:
      begin
        register_30 <= register_152;
        program_counter <= 16'd112;
      end

      16'd127:
      begin
        register_23 <= 16'd0;
        program_counter <= register_22;
      end

      16'd128:
      begin
        register_36 <= 16'd521;
      end

      16'd129:
      begin
        register_9 <= register_36;
        program_counter <= 16'd2;
        register_7 <= 16'd130;
      end

      16'd130:
      begin
        register_152 <= register_8;
        register_37 <= 16'd0;
        register_38 <= 16'd0;
        register_39 <= 16'd0;
      end

      16'd131:
      begin
        register_152 <= input_eth_rx;
        program_counter <= 131;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd132;
        end
      end

      16'd132:
      begin
        register_37 <= register_152;
        register_152 <= 16'd0;
      end

      16'd133:
      begin
        register_38 <= register_152;
        register_152 <= 16'd0;
      end

      16'd134:
      begin
        register_39 <= register_152;
      end

      16'd135:
      begin
        register_152 <= register_39;
        register_153 <= register_37;
      end

      16'd136:
      begin
        register_152 <= $signed(register_152) < $signed(register_153);
      end

      16'd137:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 147;
      end

      16'd138:
      begin
        register_152 <= input_eth_rx;
        program_counter <= 138;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd139;
        end
      end

      16'd139:
      begin
        register_153 <= register_38;
      end

      16'd140:
      begin
        register_153 <= $signed(register_153) + $signed(register_35);
      end

      16'd141:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_38;
      end

      16'd142:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd143:
      begin
        register_38 <= register_152;
      end

      16'd144:
      begin
        register_152 <= register_39;
      end

      16'd145:
      begin
        register_152 <= $signed(register_152) + $signed(16'd2);
      end

      16'd146:
      begin
        register_39 <= register_152;
        program_counter <= 16'd135;
      end

      16'd147:
      begin
        register_152 <= 16'd0;
        register_153 <= register_0;
      end

      16'd148:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd149:
      begin
        address <= register_152;
      end

      16'd150:
      begin
        register_152 <= data_out;
      end

      16'd151:
      begin
        register_152 <= data_out;
      end

      16'd152:
      begin
        register_152 <= $signed(register_152) != $signed(register_153);
      end

      16'd153:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 160;
      end

      16'd154:
      begin
        register_152 <= 16'd0;
      end

      16'd155:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd156:
      begin
        address <= register_152;
      end

      16'd157:
      begin
        register_152 <= data_out;
      end

      16'd158:
      begin
        register_152 <= data_out;
      end

      16'd159:
      begin
        register_152 <= $signed(register_152) != $signed(16'd65535);
      end

      16'd160:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 163;
      end

      16'd161:
      begin
        program_counter <= 16'd131;
      end

      16'd162:
      begin
        program_counter <= 16'd163;
      end

      16'd163:
      begin
        register_152 <= 16'd1;
        register_153 <= register_1;
      end

      16'd164:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd165:
      begin
        address <= register_152;
      end

      16'd166:
      begin
        register_152 <= data_out;
      end

      16'd167:
      begin
        register_152 <= data_out;
      end

      16'd168:
      begin
        register_152 <= $signed(register_152) != $signed(register_153);
      end

      16'd169:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 176;
      end

      16'd170:
      begin
        register_152 <= 16'd1;
      end

      16'd171:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd172:
      begin
        address <= register_152;
      end

      16'd173:
      begin
        register_152 <= data_out;
      end

      16'd174:
      begin
        register_152 <= data_out;
      end

      16'd175:
      begin
        register_152 <= $signed(register_152) != $signed(16'd65535);
      end

      16'd176:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 179;
      end

      16'd177:
      begin
        program_counter <= 16'd131;
      end

      16'd178:
      begin
        program_counter <= 16'd179;
      end

      16'd179:
      begin
        register_152 <= 16'd2;
        register_153 <= register_2;
      end

      16'd180:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd181:
      begin
        address <= register_152;
      end

      16'd182:
      begin
        register_152 <= data_out;
      end

      16'd183:
      begin
        register_152 <= data_out;
      end

      16'd184:
      begin
        register_152 <= $signed(register_152) != $signed(register_153);
      end

      16'd185:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 192;
      end

      16'd186:
      begin
        register_152 <= 16'd2;
      end

      16'd187:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd188:
      begin
        address <= register_152;
      end

      16'd189:
      begin
        register_152 <= data_out;
      end

      16'd190:
      begin
        register_152 <= data_out;
      end

      16'd191:
      begin
        register_152 <= $signed(register_152) != $signed(16'd65535);
      end

      16'd192:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 195;
      end

      16'd193:
      begin
        program_counter <= 16'd131;
      end

      16'd194:
      begin
        program_counter <= 16'd195;
      end

      16'd195:
      begin
        register_152 <= 16'd6;
      end

      16'd196:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd197:
      begin
        address <= register_152;
      end

      16'd198:
      begin
        register_152 <= data_out;
      end

      16'd199:
      begin
        register_152 <= data_out;
      end

      16'd200:
      begin
        register_152 <= $signed(register_152) == $signed(16'd2054);
      end

      16'd201:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 265;
      end

      16'd202:
      begin
        register_152 <= 16'd10;
      end

      16'd203:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
      end

      16'd204:
      begin
        address <= register_152;
      end

      16'd205:
      begin
        register_152 <= data_out;
      end

      16'd206:
      begin
        register_152 <= data_out;
      end

      16'd207:
      begin
        register_152 <= $signed(register_152) == $signed(16'd1);
      end

      16'd208:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 263;
      end

      16'd209:
      begin
        register_152 <= 16'd1;
        register_153 <= 16'd7;
        register_24 <= register_6;
        register_25 <= 16'd64;
        register_26 <= 16'd11;
        register_27 <= 16'd12;
        register_28 <= 16'd13;
        register_29 <= 16'd2054;
      end

      16'd210:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
        register_26 <= $signed(register_26) + $signed(register_35);
        register_27 <= $signed(register_27) + $signed(register_35);
        register_28 <= $signed(register_28) + $signed(register_35);
      end

      16'd211:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd2048;
        register_153 <= 16'd8;
      end

      16'd212:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd213:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1540;
        register_153 <= 16'd9;
      end

      16'd214:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd215:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd2;
        register_153 <= 16'd10;
      end

      16'd216:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd217:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_0;
        register_153 <= 16'd11;
      end

      16'd218:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd219:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_1;
        register_153 <= 16'd12;
      end

      16'd220:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd221:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_2;
        register_153 <= 16'd13;
      end

      16'd222:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd223:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_3;
        register_153 <= 16'd14;
      end

      16'd224:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd225:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_4;
        register_153 <= 16'd15;
      end

      16'd226:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd227:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd11;
        register_153 <= 16'd16;
      end

      16'd228:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd229:
      begin
        address <= register_152;
      end

      16'd230:
      begin
        register_152 <= data_out;
      end

      16'd231:
      begin
        register_152 <= data_out;
      end

      16'd232:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd12;
        register_153 <= 16'd17;
      end

      16'd233:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd234:
      begin
        address <= register_152;
      end

      16'd235:
      begin
        register_152 <= data_out;
      end

      16'd236:
      begin
        register_152 <= data_out;
      end

      16'd237:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd13;
        register_153 <= 16'd18;
      end

      16'd238:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd239:
      begin
        address <= register_152;
      end

      16'd240:
      begin
        register_152 <= data_out;
      end

      16'd241:
      begin
        register_152 <= data_out;
      end

      16'd242:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd14;
        register_153 <= 16'd19;
      end

      16'd243:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd244:
      begin
        address <= register_152;
      end

      16'd245:
      begin
        register_152 <= data_out;
      end

      16'd246:
      begin
        register_152 <= data_out;
      end

      16'd247:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd15;
        register_153 <= 16'd20;
      end

      16'd248:
      begin
        register_152 <= $signed(register_152) + $signed(register_35);
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd249:
      begin
        address <= register_152;
      end

      16'd250:
      begin
        register_152 <= data_out;
      end

      16'd251:
      begin
        register_152 <= data_out;
      end

      16'd252:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
      end

      16'd253:
      begin
        address <= register_26;
      end

      16'd254:
      begin
        register_26 <= data_out;
      end

      16'd255:
      begin
        register_26 <= data_out;
      end

      16'd256:
      begin
        address <= register_27;
      end

      16'd257:
      begin
        register_27 <= data_out;
      end

      16'd258:
      begin
        register_27 <= data_out;
      end

      16'd259:
      begin
        address <= register_28;
      end

      16'd260:
      begin
        register_28 <= data_out;
      end

      16'd261:
      begin
        register_28 <= data_out;
        program_counter <= 16'd91;
        register_22 <= 16'd262;
      end

      16'd262:
      begin
        register_152 <= register_23;
        program_counter <= 16'd263;
      end

      16'd263:
      begin
        program_counter <= 16'd131;
      end

      16'd264:
      begin
        program_counter <= 16'd265;
      end

      16'd265:
      begin
        program_counter <= 16'd267;
      end

      16'd266:
      begin
        program_counter <= 16'd131;
      end

      16'd267:
      begin
        register_34 <= register_37;
        program_counter <= register_33;
      end

      16'd268:
      begin
        register_50 <= 16'd0;
        register_51 <= 16'd0;
        register_52 <= 16'd610;
        register_53 <= 16'd0;
        register_152 <= 16'd0;
      end

      16'd269:
      begin
        register_53 <= register_152;
      end

      16'd270:
      begin
        register_152 <= register_53;
      end

      16'd271:
      begin
        register_152 <= $signed(register_152) < $signed(16'd16);
      end

      16'd272:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 292;
      end

      16'd273:
      begin
        register_152 <= register_53;
        register_153 <= register_48;
      end

      16'd274:
      begin
        register_152 <= $signed(register_152) + $signed(register_40);
      end

      16'd275:
      begin
        address <= register_152;
      end

      16'd276:
      begin
        register_152 <= data_out;
      end

      16'd277:
      begin
        register_152 <= data_out;
      end

      16'd278:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd279:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 286;
      end

      16'd280:
      begin
        register_152 <= register_53;
        register_153 <= register_49;
      end

      16'd281:
      begin
        register_152 <= $signed(register_152) + $signed(register_41);
      end

      16'd282:
      begin
        address <= register_152;
      end

      16'd283:
      begin
        register_152 <= data_out;
      end

      16'd284:
      begin
        register_152 <= data_out;
      end

      16'd285:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd286:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 289;
      end

      16'd287:
      begin
        register_47 <= register_53;
        program_counter <= register_46;
      end

      16'd288:
      begin
        program_counter <= 16'd289;
      end

      16'd289:
      begin
        register_152 <= register_53;
      end

      16'd290:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd291:
      begin
        register_53 <= register_152;
        program_counter <= 16'd270;
      end

      16'd292:
      begin
        register_152 <= 16'd1;
        register_153 <= 16'd7;
        register_24 <= register_6;
        register_25 <= 16'd64;
        register_26 <= 16'd65535;
        register_27 <= 16'd65535;
        register_28 <= 16'd65535;
        register_29 <= 16'd2054;
      end

      16'd293:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd294:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd2048;
        register_153 <= 16'd8;
      end

      16'd295:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd296:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1540;
        register_153 <= 16'd9;
      end

      16'd297:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd298:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1;
        register_153 <= 16'd10;
      end

      16'd299:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd300:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_0;
        register_153 <= 16'd11;
      end

      16'd301:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd302:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_1;
        register_153 <= 16'd12;
      end

      16'd303:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd304:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_2;
        register_153 <= 16'd13;
      end

      16'd305:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd306:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_3;
        register_153 <= 16'd14;
      end

      16'd307:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd308:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_4;
        register_153 <= 16'd15;
      end

      16'd309:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd310:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_48;
        register_153 <= 16'd19;
      end

      16'd311:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd312:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_49;
        register_153 <= 16'd20;
      end

      16'd313:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd314:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd91;
        register_22 <= 16'd315;
      end

      16'd315:
      begin
        register_152 <= register_23;
      end

      16'd316:
      begin
        register_152 <= input_eth_rx;
        program_counter <= 316;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd317;
        end
      end

      16'd317:
      begin
        register_50 <= register_152;
        register_152 <= 16'd0;
      end

      16'd318:
      begin
        register_53 <= register_152;
        register_152 <= 16'd0;
      end

      16'd319:
      begin
        register_51 <= register_152;
      end

      16'd320:
      begin
        register_152 <= register_51;
        register_153 <= register_50;
      end

      16'd321:
      begin
        register_152 <= $signed(register_152) < $signed(register_153);
      end

      16'd322:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 337;
      end

      16'd323:
      begin
        register_152 <= register_53;
      end

      16'd324:
      begin
        register_152 <= $signed(register_152) < $signed(16'd16);
      end

      16'd325:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 330;
      end

      16'd326:
      begin
        register_152 <= input_eth_rx;
        program_counter <= 326;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd327;
        end
      end

      16'd327:
      begin
        register_153 <= register_53;
      end

      16'd328:
      begin
        register_153 <= $signed(register_153) + $signed(register_52);
      end

      16'd329:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd331;
      end

      16'd330:
      begin
        register_152 <= input_eth_rx;
        program_counter <= 330;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd331;
        end
      end

      16'd331:
      begin
        register_152 <= register_53;
      end

      16'd332:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd333:
      begin
        register_53 <= register_152;
      end

      16'd334:
      begin
        register_152 <= register_51;
      end

      16'd335:
      begin
        register_152 <= $signed(register_152) + $signed(16'd2);
      end

      16'd336:
      begin
        register_51 <= register_152;
        program_counter <= 16'd320;
      end

      16'd337:
      begin
        register_152 <= 16'd6;
      end

      16'd338:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
      end

      16'd339:
      begin
        address <= register_152;
      end

      16'd340:
      begin
        register_152 <= data_out;
      end

      16'd341:
      begin
        register_152 <= data_out;
      end

      16'd342:
      begin
        register_152 <= $signed(register_152) == $signed(16'd2054);
      end

      16'd343:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 350;
      end

      16'd344:
      begin
        register_152 <= 16'd10;
      end

      16'd345:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
      end

      16'd346:
      begin
        address <= register_152;
      end

      16'd347:
      begin
        register_152 <= data_out;
      end

      16'd348:
      begin
        register_152 <= data_out;
      end

      16'd349:
      begin
        register_152 <= $signed(register_152) == $signed(16'd2);
      end

      16'd350:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 396;
      end

      16'd351:
      begin
        register_152 <= 16'd14;
        register_153 <= register_48;
      end

      16'd352:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
      end

      16'd353:
      begin
        address <= register_152;
      end

      16'd354:
      begin
        register_152 <= data_out;
      end

      16'd355:
      begin
        register_152 <= data_out;
      end

      16'd356:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd357:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 364;
      end

      16'd358:
      begin
        register_152 <= 16'd15;
        register_153 <= register_49;
      end

      16'd359:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
      end

      16'd360:
      begin
        address <= register_152;
      end

      16'd361:
      begin
        register_152 <= data_out;
      end

      16'd362:
      begin
        register_152 <= data_out;
      end

      16'd363:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd364:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 395;
      end

      16'd365:
      begin
        register_152 <= register_48;
        register_153 <= register_45;
      end

      16'd366:
      begin
        register_153 <= $signed(register_153) + $signed(register_40);
      end

      16'd367:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_49;
        register_153 <= register_45;
      end

      16'd368:
      begin
        register_153 <= $signed(register_153) + $signed(register_41);
      end

      16'd369:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd11;
        register_153 <= register_45;
      end

      16'd370:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
        register_153 <= $signed(register_153) + $signed(register_42);
      end

      16'd371:
      begin
        address <= register_152;
      end

      16'd372:
      begin
        register_152 <= data_out;
      end

      16'd373:
      begin
        register_152 <= data_out;
      end

      16'd374:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd12;
        register_153 <= register_45;
      end

      16'd375:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
        register_153 <= $signed(register_153) + $signed(register_43);
      end

      16'd376:
      begin
        address <= register_152;
      end

      16'd377:
      begin
        register_152 <= data_out;
      end

      16'd378:
      begin
        register_152 <= data_out;
      end

      16'd379:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd13;
        register_153 <= register_45;
      end

      16'd380:
      begin
        register_152 <= $signed(register_152) + $signed(register_52);
        register_153 <= $signed(register_153) + $signed(register_44);
      end

      16'd381:
      begin
        address <= register_152;
      end

      16'd382:
      begin
        register_152 <= data_out;
      end

      16'd383:
      begin
        register_152 <= data_out;
      end

      16'd384:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_45;
      end

      16'd385:
      begin
        register_53 <= register_152;
        register_152 <= register_45;
      end

      16'd386:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd387:
      begin
        register_45 <= register_152;
      end

      16'd388:
      begin
        register_152 <= register_45;
      end

      16'd389:
      begin
        register_152 <= $signed(register_152) == $signed(16'd16);
      end

      16'd390:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 393;
      end

      16'd391:
      begin
        register_152 <= 16'd0;
      end

      16'd392:
      begin
        register_45 <= register_152;
        program_counter <= 16'd393;
      end

      16'd393:
      begin
        register_47 <= register_53;
        program_counter <= register_46;
      end

      16'd394:
      begin
        program_counter <= 16'd395;
      end

      16'd395:
      begin
        program_counter <= 16'd396;
      end

      16'd396:
      begin
        program_counter <= 16'd316;
      end

      16'd397:
      begin
        register_61 <= 16'd626;
      end

      16'd398:
      begin
        register_9 <= register_61;
        program_counter <= 16'd2;
        register_7 <= 16'd399;
      end

      16'd399:
      begin
        register_152 <= register_8;
        register_62 <= 16'd0;
        register_63 <= 16'd0;
        register_64 <= 16'd0;
        register_48 <= register_59;
        register_49 <= register_60;
        program_counter <= 16'd268;
        register_46 <= 16'd400;
      end

      16'd400:
      begin
        register_152 <= register_47;
        register_153 <= 16'd7;
      end

      16'd401:
      begin
        register_64 <= register_152;
        register_152 <= 16'd17664;
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd402:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_57;
        register_153 <= 16'd8;
      end

      16'd403:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd404:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= 16'd9;
      end

      16'd405:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd406:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd16384;
        register_153 <= 16'd10;
      end

      16'd407:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd408:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_58;
        register_153 <= 16'd11;
      end

      16'd409:
      begin
        register_152 <= $signed(16'd65280) | $signed(register_152);
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd410:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= 16'd12;
      end

      16'd411:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd412:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_3;
        register_153 <= 16'd13;
      end

      16'd413:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd414:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_4;
        register_153 <= 16'd14;
      end

      16'd415:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd416:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_59;
        register_153 <= 16'd15;
      end

      16'd417:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd418:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_60;
        register_153 <= 16'd16;
      end

      16'd419:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd420:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_57;
      end

      16'd421:
      begin
        register_152 <= $signed(register_152) + $signed(16'd14);
      end

      16'd422:
      begin
        register_62 <= register_152;
        register_152 <= 16'd10;
      end

      16'd423:
      begin
        s_output_checksum <= register_152;
        program_counter <= 423;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 424;
        end
      end

      16'd424:
      begin
        register_152 <= 16'd7;
      end

      16'd425:
      begin
        register_63 <= register_152;
      end

      16'd426:
      begin
        register_152 <= register_63;
      end

      16'd427:
      begin
        register_152 <= $signed(register_152) <= $signed(16'd16);
      end

      16'd428:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 438;
      end

      16'd429:
      begin
        register_152 <= register_63;
      end

      16'd430:
      begin
        register_152 <= $signed(register_152) + $signed(register_56);
      end

      16'd431:
      begin
        address <= register_152;
      end

      16'd432:
      begin
        register_152 <= data_out;
      end

      16'd433:
      begin
        register_152 <= data_out;
      end

      16'd434:
      begin
        s_output_checksum <= register_152;
        program_counter <= 434;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 435;
        end
      end

      16'd435:
      begin
        register_152 <= register_63;
      end

      16'd436:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd437:
      begin
        register_63 <= register_152;
        program_counter <= 16'd426;
      end

      16'd438:
      begin
        register_152 <= input_checksum;
        program_counter <= 438;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd439;
        end
      end

      16'd439:
      begin
        register_153 <= 16'd12;
      end

      16'd440:
      begin
        register_153 <= $signed(register_153) + $signed(register_56);
      end

      16'd441:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_62;
      end

      16'd442:
      begin
        register_152 <= $signed(register_152) < $signed(16'd64);
      end

      16'd443:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 446;
      end

      16'd444:
      begin
        register_152 <= 16'd64;
      end

      16'd445:
      begin
        register_62 <= register_152;
        program_counter <= 16'd446;
      end

      16'd446:
      begin
        register_24 <= register_56;
        register_25 <= register_62;
        register_26 <= register_64;
        register_27 <= register_64;
        register_28 <= register_64;
        register_29 <= 16'd2048;
      end

      16'd447:
      begin
        register_26 <= $signed(register_26) + $signed(register_42);
        register_27 <= $signed(register_27) + $signed(register_43);
        register_28 <= $signed(register_28) + $signed(register_44);
      end

      16'd448:
      begin
        address <= register_26;
      end

      16'd449:
      begin
        register_26 <= data_out;
      end

      16'd450:
      begin
        register_26 <= data_out;
      end

      16'd451:
      begin
        address <= register_27;
      end

      16'd452:
      begin
        register_27 <= data_out;
      end

      16'd453:
      begin
        register_27 <= data_out;
      end

      16'd454:
      begin
        address <= register_28;
      end

      16'd455:
      begin
        register_28 <= data_out;
      end

      16'd456:
      begin
        register_28 <= data_out;
        program_counter <= 16'd91;
        register_22 <= 16'd457;
      end

      16'd457:
      begin
        register_152 <= register_23;
        register_55 <= 16'd0;
        program_counter <= register_54;
      end

      16'd458:
      begin
        register_68 <= 16'd0;
        register_69 <= 16'd0;
        register_70 <= 16'd0;
        register_71 <= 16'd0;
        register_72 <= 16'd0;
        register_73 <= 16'd0;
        register_74 <= 16'd0;
        register_75 <= 16'd0;
        register_76 <= 16'd0;
        register_77 <= 16'd634;
      end

      16'd459:
      begin
        register_9 <= register_77;
        program_counter <= 16'd2;
        register_7 <= 16'd460;
      end

      16'd460:
      begin
        register_152 <= register_8;
      end

      16'd461:
      begin
        register_35 <= register_67;
        program_counter <= 16'd128;
        register_33 <= 16'd462;
      end

      16'd462:
      begin
        register_152 <= register_34;
      end

      16'd463:
      begin
        register_62 <= register_152;
        register_152 <= 16'd6;
      end

      16'd464:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd465:
      begin
        address <= register_152;
      end

      16'd466:
      begin
        register_152 <= data_out;
      end

      16'd467:
      begin
        register_152 <= data_out;
      end

      16'd468:
      begin
        register_152 <= $signed(register_152) == $signed(16'd2048);
      end

      16'd469:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 583;
      end

      16'd470:
      begin
        register_152 <= 16'd15;
        register_153 <= register_3;
      end

      16'd471:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd472:
      begin
        address <= register_152;
      end

      16'd473:
      begin
        register_152 <= data_out;
      end

      16'd474:
      begin
        register_152 <= data_out;
      end

      16'd475:
      begin
        register_152 <= $signed(register_152) != $signed(register_153);
      end

      16'd476:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 479;
      end

      16'd477:
      begin
        program_counter <= 16'd461;
      end

      16'd478:
      begin
        program_counter <= 16'd479;
      end

      16'd479:
      begin
        register_152 <= 16'd16;
        register_153 <= register_4;
      end

      16'd480:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd481:
      begin
        address <= register_152;
      end

      16'd482:
      begin
        register_152 <= data_out;
      end

      16'd483:
      begin
        register_152 <= data_out;
      end

      16'd484:
      begin
        register_152 <= $signed(register_152) != $signed(register_153);
      end

      16'd485:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 488;
      end

      16'd486:
      begin
        program_counter <= 16'd461;
      end

      16'd487:
      begin
        program_counter <= 16'd488;
      end

      16'd488:
      begin
        register_152 <= 16'd11;
      end

      16'd489:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd490:
      begin
        address <= register_152;
      end

      16'd491:
      begin
        register_152 <= data_out;
      end

      16'd492:
      begin
        register_152 <= data_out;
      end

      16'd493:
      begin
        register_152 <= $signed(register_152) & $signed(16'd255);
      end

      16'd494:
      begin
        register_152 <= $signed(register_152) == $signed(16'd1);
      end

      16'd495:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 572;
      end

      16'd496:
      begin
        register_152 <= 16'd7;
      end

      16'd497:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd498:
      begin
        address <= register_152;
      end

      16'd499:
      begin
        register_152 <= data_out;
      end

      16'd500:
      begin
        register_152 <= data_out;
      end

      16'd501:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd8);
      end

      16'd502:
      begin
        register_152 <= $signed(register_152) & $signed(16'd15);
      end

      16'd503:
      begin
        register_152 <= $signed(register_152) << $signed(16'd1);
      end

      16'd504:
      begin
        register_70 <= register_152;
      end

      16'd505:
      begin
        register_152 <= register_70;
        register_153 <= register_70;
      end

      16'd506:
      begin
        register_152 <= $signed(register_152) + $signed(16'd7);
      end

      16'd507:
      begin
        register_71 <= register_152;
        register_152 <= 16'd8;
      end

      16'd508:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd509:
      begin
        address <= register_152;
      end

      16'd510:
      begin
        register_152 <= data_out;
      end

      16'd511:
      begin
        register_152 <= data_out;
      end

      16'd512:
      begin
        register_69 <= register_152;
      end

      16'd513:
      begin
        register_152 <= register_69;
      end

      16'd514:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd515:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd1);
      end

      16'd516:
      begin
        register_152 <= $signed(register_152) - $signed(register_153);
      end

      16'd517:
      begin
        register_72 <= register_152;
        register_152 <= register_71;
      end

      16'd518:
      begin
        register_153 <= register_72;
      end

      16'd519:
      begin
        register_152 <= $signed(register_152) + $signed(register_153);
      end

      16'd520:
      begin
        register_152 <= $signed(register_152) - $signed(16'd1);
      end

      16'd521:
      begin
        register_76 <= register_152;
        register_152 <= register_71;
      end

      16'd522:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd523:
      begin
        address <= register_152;
      end

      16'd524:
      begin
        register_152 <= data_out;
      end

      16'd525:
      begin
        register_152 <= data_out;
      end

      16'd526:
      begin
        register_152 <= $signed(register_152) == $signed(16'd2048);
      end

      16'd527:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 571;
      end

      16'd528:
      begin
        register_152 <= 16'd19;
      end

      16'd529:
      begin
        register_75 <= register_152;
        register_152 <= register_72;
      end

      16'd530:
      begin
        s_output_checksum <= register_152;
        program_counter <= 530;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 531;
        end
      end

      16'd531:
      begin
        register_152 <= 16'd0;
      end

      16'd532:
      begin
        s_output_checksum <= register_152;
        program_counter <= 532;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 533;
        end
      end

      16'd533:
      begin
        register_152 <= 16'd0;
      end

      16'd534:
      begin
        s_output_checksum <= register_152;
        program_counter <= 534;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 535;
        end
      end

      16'd535:
      begin
        register_152 <= register_71;
      end

      16'd536:
      begin
        register_152 <= $signed(register_152) + $signed(16'd2);
      end

      16'd537:
      begin
        register_74 <= register_152;
      end

      16'd538:
      begin
        register_152 <= register_74;
        register_153 <= register_76;
      end

      16'd539:
      begin
        register_152 <= $signed(register_152) <= $signed(register_153);
      end

      16'd540:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 557;
      end

      16'd541:
      begin
        register_152 <= register_74;
      end

      16'd542:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd543:
      begin
        address <= register_152;
      end

      16'd544:
      begin
        register_152 <= data_out;
      end

      16'd545:
      begin
        register_152 <= data_out;
      end

      16'd546:
      begin
        register_73 <= register_152;
      end

      16'd547:
      begin
        register_152 <= register_73;
      end

      16'd548:
      begin
        s_output_checksum <= register_152;
        program_counter <= 548;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 549;
        end
      end

      16'd549:
      begin
        register_152 <= register_73;
        register_153 <= register_75;
      end

      16'd550:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd551:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_75;
      end

      16'd552:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd553:
      begin
        register_75 <= register_152;
      end

      16'd554:
      begin
        register_152 <= register_74;
      end

      16'd555:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd556:
      begin
        register_74 <= register_152;
        program_counter <= 16'd538;
      end

      16'd557:
      begin
        register_152 <= 16'd0;
        register_153 <= 16'd17;
      end

      16'd558:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
      end

      16'd559:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
      end

      16'd560:
      begin
        register_152 <= input_checksum;
        program_counter <= 560;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd561;
        end
      end

      16'd561:
      begin
        register_153 <= 16'd18;
        register_56 <= register_6;
        register_57 <= register_69;
        register_58 <= 16'd1;
        register_59 <= 16'd13;
        register_60 <= 16'd14;
      end

      16'd562:
      begin
        register_153 <= $signed(register_153) + $signed(register_6);
        register_59 <= $signed(register_59) + $signed(register_67);
        register_60 <= $signed(register_60) + $signed(register_67);
      end

      16'd563:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
      end

      16'd564:
      begin
        address <= register_59;
      end

      16'd565:
      begin
        register_59 <= data_out;
      end

      16'd566:
      begin
        register_59 <= data_out;
      end

      16'd567:
      begin
        address <= register_60;
      end

      16'd568:
      begin
        register_60 <= data_out;
      end

      16'd569:
      begin
        register_60 <= data_out;
        program_counter <= 16'd397;
        register_54 <= 16'd570;
      end

      16'd570:
      begin
        register_152 <= register_55;
        program_counter <= 16'd571;
      end

      16'd571:
      begin
        program_counter <= 16'd582;
      end

      16'd572:
      begin
        register_152 <= 16'd11;
      end

      16'd573:
      begin
        register_152 <= $signed(register_152) + $signed(register_67);
      end

      16'd574:
      begin
        address <= register_152;
      end

      16'd575:
      begin
        register_152 <= data_out;
      end

      16'd576:
      begin
        register_152 <= data_out;
      end

      16'd577:
      begin
        register_152 <= $signed(register_152) & $signed(16'd255);
      end

      16'd578:
      begin
        register_152 <= $signed(register_152) == $signed(16'd6);
      end

      16'd579:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 582;
      end

      16'd580:
      begin
        register_66 <= register_62;
        program_counter <= register_65;
      end

      16'd581:
      begin
        program_counter <= 16'd582;
      end

      16'd582:
      begin
        program_counter <= 16'd583;
      end

      16'd583:
      begin
        program_counter <= 16'd461;
      end

      16'd584:
      begin
        register_106 <= 16'd650;
      end

      16'd585:
      begin
        register_9 <= register_106;
        program_counter <= 16'd2;
        register_7 <= 16'd586;
      end

      16'd586:
      begin
        register_152 <= register_8;
        register_107 <= 16'd17;
        register_108 <= 16'd0;
        register_109 <= 16'd0;
        register_110 <= 16'd0;
      end

      16'd587:
      begin
        register_152 <= register_80;
        register_153 <= register_107;
      end

      16'd588:
      begin
        register_153 <= $signed(register_153) + $signed(16'd0);
      end

      16'd589:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd590:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_81;
        register_153 <= register_107;
      end

      16'd591:
      begin
        register_153 <= $signed(register_153) + $signed(16'd1);
      end

      16'd592:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd593:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1;
        register_153 <= register_107;
      end

      16'd594:
      begin
        register_152 <= $signed(register_152) + $signed(register_82);
        register_153 <= $signed(register_153) + $signed(16'd2);
      end

      16'd595:
      begin
        address <= register_152;
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd596:
      begin
        register_152 <= data_out;
      end

      16'd597:
      begin
        register_152 <= data_out;
      end

      16'd598:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= register_107;
      end

      16'd599:
      begin
        register_152 <= $signed(register_152) + $signed(register_82);
        register_153 <= $signed(register_153) + $signed(16'd3);
      end

      16'd600:
      begin
        address <= register_152;
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd601:
      begin
        register_152 <= data_out;
      end

      16'd602:
      begin
        register_152 <= data_out;
      end

      16'd603:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd1;
        register_153 <= register_107;
      end

      16'd604:
      begin
        register_152 <= $signed(register_152) + $signed(register_83);
        register_153 <= $signed(register_153) + $signed(16'd4);
      end

      16'd605:
      begin
        address <= register_152;
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd606:
      begin
        register_152 <= data_out;
      end

      16'd607:
      begin
        register_152 <= data_out;
      end

      16'd608:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= register_107;
      end

      16'd609:
      begin
        register_152 <= $signed(register_152) + $signed(register_83);
        register_153 <= $signed(register_153) + $signed(16'd5);
      end

      16'd610:
      begin
        address <= register_152;
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd611:
      begin
        register_152 <= data_out;
      end

      16'd612:
      begin
        register_152 <= data_out;
      end

      16'd613:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd20480;
        register_153 <= register_107;
      end

      16'd614:
      begin
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd615:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd616:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_84;
        register_153 <= register_107;
      end

      16'd617:
      begin
        register_153 <= $signed(register_153) + $signed(16'd7);
      end

      16'd618:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd619:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= register_107;
      end

      16'd620:
      begin
        register_153 <= $signed(register_153) + $signed(16'd8);
      end

      16'd621:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd622:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= register_107;
      end

      16'd623:
      begin
        register_153 <= $signed(register_153) + $signed(16'd9);
      end

      16'd624:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd625:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_85;
      end

      16'd626:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 635;
      end

      16'd627:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd628:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd629:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd630:
      begin
        address <= register_152;
      end

      16'd631:
      begin
        register_152 <= data_out;
      end

      16'd632:
      begin
        register_152 <= data_out;
      end

      16'd633:
      begin
        register_152 <= $signed(register_152) | $signed(16'd1);
      end

      16'd634:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd635;
      end

      16'd635:
      begin
        register_152 <= register_86;
      end

      16'd636:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 645;
      end

      16'd637:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd638:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd639:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd640:
      begin
        address <= register_152;
      end

      16'd641:
      begin
        register_152 <= data_out;
      end

      16'd642:
      begin
        register_152 <= data_out;
      end

      16'd643:
      begin
        register_152 <= $signed(register_152) | $signed(16'd2);
      end

      16'd644:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd645;
      end

      16'd645:
      begin
        register_152 <= register_87;
      end

      16'd646:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 655;
      end

      16'd647:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd648:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd649:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd650:
      begin
        address <= register_152;
      end

      16'd651:
      begin
        register_152 <= data_out;
      end

      16'd652:
      begin
        register_152 <= data_out;
      end

      16'd653:
      begin
        register_152 <= $signed(register_152) | $signed(16'd4);
      end

      16'd654:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd655;
      end

      16'd655:
      begin
        register_152 <= register_88;
      end

      16'd656:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 665;
      end

      16'd657:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd658:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd659:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd660:
      begin
        address <= register_152;
      end

      16'd661:
      begin
        register_152 <= data_out;
      end

      16'd662:
      begin
        register_152 <= data_out;
      end

      16'd663:
      begin
        register_152 <= $signed(register_152) | $signed(16'd8);
      end

      16'd664:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd665;
      end

      16'd665:
      begin
        register_152 <= register_89;
      end

      16'd666:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 675;
      end

      16'd667:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd668:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd669:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd670:
      begin
        address <= register_152;
      end

      16'd671:
      begin
        register_152 <= data_out;
      end

      16'd672:
      begin
        register_152 <= data_out;
      end

      16'd673:
      begin
        register_152 <= $signed(register_152) | $signed(16'd16);
      end

      16'd674:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd675;
      end

      16'd675:
      begin
        register_152 <= register_90;
      end

      16'd676:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 685;
      end

      16'd677:
      begin
        register_152 <= register_107;
        register_153 <= register_107;
      end

      16'd678:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
        register_153 <= $signed(register_153) + $signed(16'd6);
      end

      16'd679:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd680:
      begin
        address <= register_152;
      end

      16'd681:
      begin
        register_152 <= data_out;
      end

      16'd682:
      begin
        register_152 <= data_out;
      end

      16'd683:
      begin
        register_152 <= $signed(register_152) | $signed(16'd32);
      end

      16'd684:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd685;
      end

      16'd685:
      begin
        register_152 <= register_105;
      end

      16'd686:
      begin
        register_152 <= $signed(register_152) + $signed(16'd20);
      end

      16'd687:
      begin
        register_152 <= $signed(register_152) + $signed(16'd12);
      end

      16'd688:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd689:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd1);
      end

      16'd690:
      begin
        register_108 <= register_152;
      end

      16'd691:
      begin
        register_152 <= register_108;
      end

      16'd692:
      begin
        s_output_checksum <= register_152;
        program_counter <= 692;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 693;
        end
      end

      16'd693:
      begin
        register_152 <= register_3;
      end

      16'd694:
      begin
        s_output_checksum <= register_152;
        program_counter <= 694;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 695;
        end
      end

      16'd695:
      begin
        register_152 <= register_4;
      end

      16'd696:
      begin
        s_output_checksum <= register_152;
        program_counter <= 696;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 697;
        end
      end

      16'd697:
      begin
        register_152 <= register_78;
      end

      16'd698:
      begin
        s_output_checksum <= register_152;
        program_counter <= 698;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 699;
        end
      end

      16'd699:
      begin
        register_152 <= register_79;
      end

      16'd700:
      begin
        s_output_checksum <= register_152;
        program_counter <= 700;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 701;
        end
      end

      16'd701:
      begin
        register_152 <= 16'd6;
      end

      16'd702:
      begin
        s_output_checksum <= register_152;
        program_counter <= 702;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 703;
        end
      end

      16'd703:
      begin
        register_152 <= register_105;
      end

      16'd704:
      begin
        register_152 <= $signed(register_152) + $signed(16'd20);
      end

      16'd705:
      begin
        s_output_checksum <= register_152;
        program_counter <= 705;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 706;
        end
      end

      16'd706:
      begin
        register_152 <= register_105;
      end

      16'd707:
      begin
        register_152 <= $signed(register_152) + $signed(16'd20);
      end

      16'd708:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd709:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd1);
      end

      16'd710:
      begin
        register_109 <= register_152;
        register_152 <= register_107;
      end

      16'd711:
      begin
        register_110 <= register_152;
        register_152 <= 16'd0;
      end

      16'd712:
      begin
        register_73 <= register_152;
      end

      16'd713:
      begin
        register_152 <= register_73;
        register_153 <= register_109;
      end

      16'd714:
      begin
        register_152 <= $signed(register_152) < $signed(register_153);
      end

      16'd715:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 728;
      end

      16'd716:
      begin
        register_152 <= register_110;
      end

      16'd717:
      begin
        register_152 <= $signed(register_152) + $signed(register_104);
      end

      16'd718:
      begin
        address <= register_152;
      end

      16'd719:
      begin
        register_152 <= data_out;
      end

      16'd720:
      begin
        register_152 <= data_out;
      end

      16'd721:
      begin
        s_output_checksum <= register_152;
        program_counter <= 721;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 722;
        end
      end

      16'd722:
      begin
        register_152 <= register_110;
      end

      16'd723:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd724:
      begin
        register_110 <= register_152;
      end

      16'd725:
      begin
        register_152 <= register_73;
      end

      16'd726:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd727:
      begin
        register_73 <= register_152;
        program_counter <= 16'd713;
      end

      16'd728:
      begin
        register_152 <= input_checksum;
        program_counter <= 728;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd729;
        end
      end

      16'd729:
      begin
        register_153 <= register_107;
        register_56 <= register_104;
        register_57 <= register_105;
        register_58 <= 16'd6;
        register_59 <= register_78;
        register_60 <= register_79;
      end

      16'd730:
      begin
        register_153 <= $signed(register_153) + $signed(16'd8);
        register_57 <= $signed(register_57) + $signed(16'd40);
      end

      16'd731:
      begin
        register_153 <= $signed(register_153) + $signed(register_104);
      end

      16'd732:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd397;
        register_54 <= 16'd733;
      end

      16'd733:
      begin
        register_152 <= register_55;
        register_103 <= 16'd0;
        program_counter <= register_102;
      end

      16'd734:
      begin
        register_116 <= 16'd659;
      end

      16'd735:
      begin
        register_9 <= register_116;
        program_counter <= 16'd2;
        register_7 <= 16'd736;
      end

      16'd736:
      begin
        register_152 <= register_8;
        register_117 <= 16'd0;
        register_118 <= 16'd0;
        register_119 <= 16'd0;
        register_120 <= 16'd0;
        register_121 <= 16'd0;
        register_122 <= 16'd0;
        register_123 <= 16'd0;
        register_67 <= register_115;
        program_counter <= 16'd458;
        register_65 <= 16'd737;
      end

      16'd737:
      begin
        register_152 <= register_66;
        register_124 <= 16'd668;
      end

      16'd738:
      begin
        register_117 <= register_152;
        register_152 <= 16'd7;
        register_9 <= register_124;
      end

      16'd739:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd740:
      begin
        address <= register_152;
      end

      16'd741:
      begin
        register_152 <= data_out;
      end

      16'd742:
      begin
        register_152 <= data_out;
      end

      16'd743:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd8);
      end

      16'd744:
      begin
        register_152 <= $signed(register_152) & $signed(16'd15);
      end

      16'd745:
      begin
        register_152 <= $signed(register_152) << $signed(16'd1);
      end

      16'd746:
      begin
        register_118 <= register_152;
      end

      16'd747:
      begin
        register_152 <= register_118;
        register_153 <= register_118;
      end

      16'd748:
      begin
        register_152 <= $signed(register_152) + $signed(16'd7);
        register_153 <= $signed(register_153) << $signed(16'd1);
      end

      16'd749:
      begin
        register_119 <= register_152;
        register_152 <= 16'd8;
      end

      16'd750:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd751:
      begin
        address <= register_152;
      end

      16'd752:
      begin
        register_152 <= data_out;
      end

      16'd753:
      begin
        register_152 <= data_out;
      end

      16'd754:
      begin
        register_120 <= register_152;
      end

      16'd755:
      begin
        register_152 <= register_120;
      end

      16'd756:
      begin
        register_152 <= $signed(register_152) - $signed(register_153);
      end

      16'd757:
      begin
        register_121 <= register_152;
        register_152 <= register_119;
      end

      16'd758:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd759:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd760:
      begin
        address <= register_152;
      end

      16'd761:
      begin
        register_152 <= data_out;
      end

      16'd762:
      begin
        register_152 <= data_out;
      end

      16'd763:
      begin
        register_152 <= $signed(register_152) & $signed(16'd61440);
      end

      16'd764:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd10);
      end

      16'd765:
      begin
        register_123 <= register_152;
        program_counter <= 16'd2;
        register_7 <= 16'd766;
      end

      16'd766:
      begin
        register_152 <= register_8;
        register_16 <= register_123;
        program_counter <= 16'd30;
        register_14 <= 16'd767;
      end

      16'd767:
      begin
        register_152 <= register_15;
        register_125 <= 16'd687;
      end

      16'd768:
      begin
        register_9 <= register_125;
        program_counter <= 16'd2;
        register_7 <= 16'd769;
      end

      16'd769:
      begin
        register_152 <= register_8;
        register_153 <= register_123;
        register_126 <= 16'd689;
      end

      16'd770:
      begin
        register_152 <= register_121;
        register_9 <= register_126;
      end

      16'd771:
      begin
        register_152 <= $signed(register_152) - $signed(register_153);
        register_153 <= register_123;
      end

      16'd772:
      begin
        register_111 <= register_152;
        register_152 <= register_119;
        register_153 <= $signed(register_153) >>> $signed(16'd1);
      end

      16'd773:
      begin
        register_152 <= $signed(register_152) + $signed(register_153);
      end

      16'd774:
      begin
        register_112 <= register_152;
        program_counter <= 16'd2;
        register_7 <= 16'd775;
      end

      16'd775:
      begin
        register_152 <= register_8;
        register_16 <= register_111;
        program_counter <= 16'd30;
        register_14 <= 16'd776;
      end

      16'd776:
      begin
        register_152 <= register_15;
        register_127 <= 16'd700;
      end

      16'd777:
      begin
        register_9 <= register_127;
        program_counter <= 16'd2;
        register_7 <= 16'd778;
      end

      16'd778:
      begin
        register_152 <= register_8;
        register_153 <= 16'd1;
        register_114 <= 16'd0;
      end

      16'd779:
      begin
        register_152 <= register_119;
        register_153 <= $signed(register_153) + $signed(register_93);
      end

      16'd780:
      begin
        register_152 <= $signed(register_152) + $signed(16'd0);
      end

      16'd781:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd782:
      begin
        address <= register_152;
      end

      16'd783:
      begin
        register_152 <= data_out;
      end

      16'd784:
      begin
        register_152 <= data_out;
      end

      16'd785:
      begin
        register_91 <= register_152;
        register_152 <= register_119;
      end

      16'd786:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd787:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd788:
      begin
        address <= register_152;
      end

      16'd789:
      begin
        register_152 <= data_out;
      end

      16'd790:
      begin
        register_152 <= data_out;
      end

      16'd791:
      begin
        register_92 <= register_152;
        register_152 <= register_119;
      end

      16'd792:
      begin
        register_152 <= $signed(register_152) + $signed(16'd2);
      end

      16'd793:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd794:
      begin
        address <= register_152;
      end

      16'd795:
      begin
        register_152 <= data_out;
      end

      16'd796:
      begin
        register_152 <= data_out;
      end

      16'd797:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_119;
        register_153 <= 16'd0;
      end

      16'd798:
      begin
        register_152 <= $signed(register_152) + $signed(16'd3);
        register_153 <= $signed(register_153) + $signed(register_93);
      end

      16'd799:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd800:
      begin
        address <= register_152;
      end

      16'd801:
      begin
        register_152 <= data_out;
      end

      16'd802:
      begin
        register_152 <= data_out;
      end

      16'd803:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_119;
        register_153 <= 16'd1;
      end

      16'd804:
      begin
        register_152 <= $signed(register_152) + $signed(16'd4);
        register_153 <= $signed(register_153) + $signed(register_94);
      end

      16'd805:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd806:
      begin
        address <= register_152;
      end

      16'd807:
      begin
        register_152 <= data_out;
      end

      16'd808:
      begin
        register_152 <= data_out;
      end

      16'd809:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_119;
        register_153 <= 16'd0;
      end

      16'd810:
      begin
        register_152 <= $signed(register_152) + $signed(16'd5);
        register_153 <= $signed(register_153) + $signed(register_94);
      end

      16'd811:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd812:
      begin
        address <= register_152;
      end

      16'd813:
      begin
        register_152 <= data_out;
      end

      16'd814:
      begin
        register_152 <= data_out;
      end

      16'd815:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= register_119;
      end

      16'd816:
      begin
        register_152 <= $signed(register_152) + $signed(16'd7);
      end

      16'd817:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd818:
      begin
        address <= register_152;
      end

      16'd819:
      begin
        register_152 <= data_out;
      end

      16'd820:
      begin
        register_152 <= data_out;
      end

      16'd821:
      begin
        register_95 <= register_152;
        register_152 <= register_119;
      end

      16'd822:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd823:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd824:
      begin
        address <= register_152;
      end

      16'd825:
      begin
        register_152 <= data_out;
      end

      16'd826:
      begin
        register_152 <= data_out;
      end

      16'd827:
      begin
        register_152 <= $signed(register_152) & $signed(16'd1);
      end

      16'd828:
      begin
        register_96 <= register_152;
        register_152 <= register_119;
      end

      16'd829:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd830:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd831:
      begin
        address <= register_152;
      end

      16'd832:
      begin
        register_152 <= data_out;
      end

      16'd833:
      begin
        register_152 <= data_out;
      end

      16'd834:
      begin
        register_152 <= $signed(register_152) & $signed(16'd2);
      end

      16'd835:
      begin
        register_97 <= register_152;
        register_152 <= register_119;
      end

      16'd836:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd837:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd838:
      begin
        address <= register_152;
      end

      16'd839:
      begin
        register_152 <= data_out;
      end

      16'd840:
      begin
        register_152 <= data_out;
      end

      16'd841:
      begin
        register_152 <= $signed(register_152) & $signed(16'd4);
      end

      16'd842:
      begin
        register_98 <= register_152;
        register_152 <= register_119;
      end

      16'd843:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd844:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd845:
      begin
        address <= register_152;
      end

      16'd846:
      begin
        register_152 <= data_out;
      end

      16'd847:
      begin
        register_152 <= data_out;
      end

      16'd848:
      begin
        register_152 <= $signed(register_152) & $signed(16'd8);
      end

      16'd849:
      begin
        register_99 <= register_152;
        register_152 <= register_119;
      end

      16'd850:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd851:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd852:
      begin
        address <= register_152;
      end

      16'd853:
      begin
        register_152 <= data_out;
      end

      16'd854:
      begin
        register_152 <= data_out;
      end

      16'd855:
      begin
        register_152 <= $signed(register_152) & $signed(16'd16);
      end

      16'd856:
      begin
        register_100 <= register_152;
        register_152 <= register_119;
      end

      16'd857:
      begin
        register_152 <= $signed(register_152) + $signed(16'd6);
      end

      16'd858:
      begin
        register_152 <= $signed(register_152) + $signed(register_115);
      end

      16'd859:
      begin
        address <= register_152;
      end

      16'd860:
      begin
        register_152 <= data_out;
      end

      16'd861:
      begin
        register_152 <= data_out;
      end

      16'd862:
      begin
        register_152 <= $signed(register_152) & $signed(16'd32);
      end

      16'd863:
      begin
        register_101 <= register_152;
        program_counter <= register_113;
      end

      16'd864:
      begin
        register_133 <= 16'd0;
        register_134 <= 16'd0;
        register_135 <= 16'd702;
      end

      16'd865:
      begin
        register_9 <= register_135;
        program_counter <= 16'd2;
        register_7 <= 16'd866;
      end

      16'd866:
      begin
        register_152 <= register_8;
      end

      16'd867:
      begin
        register_152 <= register_131;
      end

      16'd868:
      begin
        register_134 <= register_152;
        register_152 <= register_132;
      end

      16'd869:
      begin
        register_133 <= register_152;
      end

      16'd870:
      begin
        register_152 <= register_133;
      end

      16'd871:
      begin
        register_152 <= $signed(register_152) > $signed(16'd0);
      end

      16'd872:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 897;
      end

      16'd873:
      begin
        register_152 <= register_133;
      end

      16'd874:
      begin
        register_152 <= $signed(register_152) > $signed(16'd1);
      end

      16'd875:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 884;
      end

      16'd876:
      begin
        register_152 <= register_134;
      end

      16'd877:
      begin
        register_152 <= $signed(register_152) + $signed(register_130);
      end

      16'd878:
      begin
        address <= register_152;
      end

      16'd879:
      begin
        register_152 <= data_out;
      end

      16'd880:
      begin
        register_152 <= data_out;
      end

      16'd881:
      begin
        register_152 <= $signed(register_152) >>> $signed(16'd8);
      end

      16'd882:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 882;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 883;
        end
      end

      16'd883:
      begin
        program_counter <= 16'd884;
      end

      16'd884:
      begin
        register_152 <= register_134;
      end

      16'd885:
      begin
        register_152 <= $signed(register_152) + $signed(register_130);
      end

      16'd886:
      begin
        address <= register_152;
      end

      16'd887:
      begin
        register_152 <= data_out;
      end

      16'd888:
      begin
        register_152 <= data_out;
      end

      16'd889:
      begin
        register_152 <= $signed(register_152) & $signed(16'd255);
      end

      16'd890:
      begin
        s_output_rs232_tx <= register_152;
        program_counter <= 890;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 891;
        end
      end

      16'd891:
      begin
        register_152 <= register_134;
      end

      16'd892:
      begin
        register_152 <= $signed(register_152) + $signed(16'd1);
      end

      16'd893:
      begin
        register_134 <= register_152;
      end

      16'd894:
      begin
        register_152 <= register_133;
      end

      16'd895:
      begin
        register_152 <= $signed(register_152) - $signed(16'd1);
      end

      16'd896:
      begin
        register_133 <= register_152;
        program_counter <= 16'd870;
      end

      16'd897:
      begin
        register_136 <= 16'd714;
      end

      16'd898:
      begin
        register_9 <= register_136;
        program_counter <= 16'd2;
        register_7 <= 16'd899;
      end

      16'd899:
      begin
        register_152 <= register_8;
        register_129 <= 16'd0;
        program_counter <= register_128;
      end

      16'd900:
      begin
        register_139 <= 16'd716;
        register_140 <= 16'd1740;
        register_141 <= 16'd27;
        register_142 <= 16'd1;
        register_143 <= 16'd2;
        register_144 <= 16'd3;
        register_152 <= 16'd0;
        register_153 <= 16'd0;
        register_146 <= 16'd2764;
      end

      16'd901:
      begin
        register_145 <= register_142;
        register_153 <= $signed(register_153) + $signed(register_82);
        register_9 <= register_146;
      end

      16'd902:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        register_152 <= 16'd0;
        register_153 <= 16'd1;
      end

      16'd903:
      begin
        register_153 <= $signed(register_153) + $signed(register_82);
      end

      16'd904:
      begin
        address <= register_153;
        data_in <= register_152;
        write_enable <= 1'b1;
        program_counter <= 16'd2;
        register_7 <= 16'd905;
      end

      16'd905:
      begin
        register_152 <= register_8;
      end

      16'd906:
      begin
        register_152 <= register_145;
        register_153 <= register_142;
      end

      16'd907:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd908:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 950;
      end

      16'd909:
      begin
        register_115 <= register_139;
        program_counter <= 16'd734;
        register_113 <= 16'd910;
      end

      16'd910:
      begin
        register_152 <= register_114;
      end

      16'd911:
      begin
        register_152 <= register_97;
      end

      16'd912:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 949;
      end

      16'd913:
      begin
        register_147 <= 16'd2783;
      end

      16'd914:
      begin
        register_9 <= register_147;
        program_counter <= 16'd2;
        register_7 <= 16'd915;
      end

      16'd915:
      begin
        register_152 <= register_8;
        register_16 <= 16'd13;
      end

      16'd916:
      begin
        register_16 <= $signed(register_16) + $signed(register_139);
      end

      16'd917:
      begin
        address <= register_16;
      end

      16'd918:
      begin
        register_16 <= data_out;
      end

      16'd919:
      begin
        register_16 <= data_out;
        program_counter <= 16'd30;
        register_14 <= 16'd920;
      end

      16'd920:
      begin
        register_152 <= register_15;
        register_16 <= 16'd14;
      end

      16'd921:
      begin
        register_16 <= $signed(register_16) + $signed(register_139);
      end

      16'd922:
      begin
        address <= register_16;
      end

      16'd923:
      begin
        register_16 <= data_out;
      end

      16'd924:
      begin
        register_16 <= data_out;
        program_counter <= 16'd30;
        register_14 <= 16'd925;
      end

      16'd925:
      begin
        register_152 <= register_15;
        register_148 <= 16'd2811;
      end

      16'd926:
      begin
        register_9 <= register_148;
        program_counter <= 16'd2;
        register_7 <= 16'd927;
      end

      16'd927:
      begin
        register_152 <= register_8;
        register_19 <= register_83;
        register_20 <= register_93;
        register_21 <= 16'd1;
      end

      16'd928:
      begin
        register_152 <= 16'd13;
      end

      16'd929:
      begin
        register_152 <= $signed(register_152) + $signed(register_139);
      end

      16'd930:
      begin
        address <= register_152;
      end

      16'd931:
      begin
        register_152 <= data_out;
      end

      16'd932:
      begin
        register_152 <= data_out;
      end

      16'd933:
      begin
        register_78 <= register_152;
        register_152 <= 16'd14;
      end

      16'd934:
      begin
        register_152 <= $signed(register_152) + $signed(register_139);
      end

      16'd935:
      begin
        address <= register_152;
      end

      16'd936:
      begin
        register_152 <= data_out;
      end

      16'd937:
      begin
        register_152 <= data_out;
      end

      16'd938:
      begin
        register_79 <= register_152;
        register_152 <= register_91;
      end

      16'd939:
      begin
        register_81 <= register_152;
        register_152 <= register_5;
      end

      16'd940:
      begin
        register_80 <= register_152;
        program_counter <= 16'd54;
        register_17 <= 16'd941;
      end

      16'd941:
      begin
        register_152 <= register_18;
        register_104 <= register_140;
        register_105 <= 16'd0;
      end

      16'd942:
      begin
        register_152 <= 16'd1;
      end

      16'd943:
      begin
        register_86 <= register_152;
        register_152 <= 16'd1;
      end

      16'd944:
      begin
        register_89 <= register_152;
        register_152 <= register_143;
      end

      16'd945:
      begin
        register_145 <= register_152;
        program_counter <= 16'd584;
        register_102 <= 16'd946;
      end

      16'd946:
      begin
        register_152 <= register_103;
        register_149 <= 16'd2813;
      end

      16'd947:
      begin
        register_9 <= register_149;
        program_counter <= 16'd2;
        register_7 <= 16'd948;
      end

      16'd948:
      begin
        register_152 <= register_8;
        program_counter <= 16'd949;
      end

      16'd949:
      begin
        program_counter <= 16'd980;
      end

      16'd950:
      begin
        register_152 <= register_145;
        register_153 <= register_143;
      end

      16'd951:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd952:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 964;
      end

      16'd953:
      begin
        register_115 <= register_139;
        program_counter <= 16'd734;
        register_113 <= 16'd954;
      end

      16'd954:
      begin
        register_152 <= register_114;
      end

      16'd955:
      begin
        register_152 <= register_100;
      end

      16'd956:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 963;
      end

      16'd957:
      begin
        register_150 <= 16'd2842;
      end

      16'd958:
      begin
        register_9 <= register_150;
        program_counter <= 16'd2;
        register_7 <= 16'd959;
      end

      16'd959:
      begin
        register_152 <= register_8;
      end

      16'd960:
      begin
        register_152 <= register_144;
      end

      16'd961:
      begin
        register_145 <= register_152;
        register_152 <= 16'd0;
      end

      16'd962:
      begin
        register_86 <= register_152;
        program_counter <= 16'd963;
      end

      16'd963:
      begin
        program_counter <= 16'd980;
      end

      16'd964:
      begin
        register_152 <= register_145;
        register_153 <= register_144;
      end

      16'd965:
      begin
        register_152 <= $signed(register_152) == $signed(register_153);
      end

      16'd966:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 980;
      end

      16'd967:
      begin
        register_115 <= register_139;
        program_counter <= 16'd734;
        register_113 <= 16'd968;
      end

      16'd968:
      begin
        register_152 <= register_114;
      end

      16'd969:
      begin
        register_152 <= register_111;
      end

      16'd970:
      begin
        if (register_152 == 16'h0000)
          program_counter <= 979;
      end

      16'd971:
      begin
        register_151 <= 16'd2866;
      end

      16'd972:
      begin
        register_9 <= register_151;
        program_counter <= 16'd2;
        register_7 <= 16'd973;
      end

      16'd973:
      begin
        register_152 <= register_8;
        register_130 <= register_139;
        register_131 <= register_112;
        register_132 <= register_111;
        program_counter <= 16'd864;
        register_128 <= 16'd974;
      end

      16'd974:
      begin
        register_152 <= register_129;
        register_19 <= register_83;
        register_20 <= register_93;
        register_21 <= register_111;
        program_counter <= 16'd54;
        register_17 <= 16'd975;
      end

      16'd975:
      begin
        register_152 <= register_18;
        register_104 <= register_140;
        register_105 <= 16'd0;
      end

      16'd976:
      begin
        register_152 <= 16'd1;
      end

      16'd977:
      begin
        register_89 <= register_152;
        program_counter <= 16'd584;
        register_102 <= 16'd978;
      end

      16'd978:
      begin
        register_152 <= register_103;
        program_counter <= 16'd979;
      end

      16'd979:
      begin
        program_counter <= 16'd980;
      end

      16'd980:
      begin
        program_counter <= 16'd906;
      end

      16'd981:
      begin
        register_152 <= 16'd5;
      end

      16'd982:
      begin
        s_output_leds <= register_152;
        program_counter <= 982;
        s_output_leds_stb <= 1'b1;
        if (s_output_leds_stb == 1'b1 && output_leds_ack == 1'b1) begin
          s_output_leds_stb <= 1'b0;
          program_counter <= 983;
        end
      end

      16'd983:
      begin
        register_152 <= 16'd5;
      end

      16'd984:
      begin
        s_output_checksum <= register_152;
        program_counter <= 984;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 985;
        end
      end

      16'd985:
      begin
        register_152 <= input_rs232_rx;
        program_counter <= 985;
        s_input_rs232_rx_ack <= 1'b1;
       if (s_input_rs232_rx_ack == 1'b1 && input_rs232_rx_stb == 1'b1) begin
          s_input_rs232_rx_ack <= 1'b0;
          program_counter <= 16'd986;
        end
      end

      16'd986:
      begin
        register_152 <= input_checksum;
        program_counter <= 986;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd987;
        end
      end

      16'd987:
      begin
        register_138 <= 16'd0;
        program_counter <= register_137;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end
  assign input_checksum_ack = s_input_checksum_ack;
  assign input_eth_rx_ack = s_input_eth_rx_ack;
  assign input_rs232_rx_ack = s_input_rs232_rx_ack;
  assign output_rs232_tx_stb = s_output_rs232_tx_stb;
  assign output_rs232_tx = s_output_rs232_tx;
  assign output_leds_stb = s_output_leds_stb;
  assign output_leds = s_output_leds;
  assign output_eth_tx_stb = s_output_eth_tx_stb;
  assign output_eth_tx = s_output_eth_tx;
  assign output_checksum_stb = s_output_checksum_stb;
  assign output_checksum = s_output_checksum;

endmodule
