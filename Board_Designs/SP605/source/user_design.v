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
  reg [15:0] memory [1848:0];

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
    memory[16'd530] = 16'd114;
    memory[16'd531] = 16'd101;
    memory[16'd532] = 16'd97;
    memory[16'd533] = 16'd100;
    memory[16'd534] = 16'd105;
    memory[16'd535] = 16'd110;
    memory[16'd536] = 16'd103;
    memory[16'd537] = 16'd32;
    memory[16'd538] = 16'd98;
    memory[16'd539] = 16'd121;
    memory[16'd540] = 16'd116;
    memory[16'd541] = 16'd101;
    memory[16'd542] = 16'd115;
    memory[16'd543] = 16'd58;
    memory[16'd544] = 16'd32;
    memory[16'd545] = 16'd0;
    memory[16'd546] = 16'd10;
    memory[16'd547] = 16'd0;
    memory[16'd548] = 16'd100;
    memory[16'd549] = 16'd111;
    memory[16'd550] = 16'd110;
    memory[16'd551] = 16'd101;
    memory[16'd552] = 16'd10;
    memory[16'd553] = 16'd0;
    memory[16'd554] = 16'd109;
    memory[16'd555] = 16'd97;
    memory[16'd556] = 16'd99;
    memory[16'd557] = 16'd32;
    memory[16'd558] = 16'd103;
    memory[16'd559] = 16'd111;
    memory[16'd560] = 16'd111;
    memory[16'd561] = 16'd100;
    memory[16'd562] = 16'd10;
    memory[16'd563] = 16'd0;
    memory[16'd564] = 16'd97;
    memory[16'd565] = 16'd114;
    memory[16'd566] = 16'd112;
    memory[16'd567] = 16'd10;
    memory[16'd568] = 16'd0;
    memory[16'd665] = 16'd99;
    memory[16'd666] = 16'd97;
    memory[16'd667] = 16'd99;
    memory[16'd668] = 16'd104;
    memory[16'd669] = 16'd101;
    memory[16'd670] = 16'd32;
    memory[16'd671] = 16'd104;
    memory[16'd672] = 16'd105;
    memory[16'd673] = 16'd116;
    memory[16'd674] = 16'd10;
    memory[16'd675] = 16'd0;
    memory[16'd676] = 16'd99;
    memory[16'd677] = 16'd97;
    memory[16'd678] = 16'd99;
    memory[16'd679] = 16'd104;
    memory[16'd680] = 16'd101;
    memory[16'd681] = 16'd32;
    memory[16'd682] = 16'd109;
    memory[16'd683] = 16'd105;
    memory[16'd684] = 16'd115;
    memory[16'd685] = 16'd115;
    memory[16'd686] = 16'd10;
    memory[16'd687] = 16'd0;
    memory[16'd688] = 16'd97;
    memory[16'd689] = 16'd114;
    memory[16'd690] = 16'd112;
    memory[16'd691] = 16'd32;
    memory[16'd692] = 16'd114;
    memory[16'd693] = 16'd101;
    memory[16'd694] = 16'd113;
    memory[16'd695] = 16'd117;
    memory[16'd696] = 16'd101;
    memory[16'd697] = 16'd115;
    memory[16'd698] = 16'd116;
    memory[16'd699] = 16'd10;
    memory[16'd700] = 16'd0;
    memory[16'd701] = 16'd103;
    memory[16'd702] = 16'd111;
    memory[16'd703] = 16'd116;
    memory[16'd704] = 16'd95;
    memory[16'd705] = 16'd112;
    memory[16'd706] = 16'd97;
    memory[16'd707] = 16'd99;
    memory[16'd708] = 16'd107;
    memory[16'd709] = 16'd101;
    memory[16'd710] = 16'd116;
    memory[16'd711] = 16'd10;
    memory[16'd712] = 16'd0;
    memory[16'd713] = 16'd97;
    memory[16'd714] = 16'd114;
    memory[16'd715] = 16'd112;
    memory[16'd716] = 16'd32;
    memory[16'd717] = 16'd114;
    memory[16'd718] = 16'd101;
    memory[16'd719] = 16'd115;
    memory[16'd720] = 16'd112;
    memory[16'd721] = 16'd111;
    memory[16'd722] = 16'd110;
    memory[16'd723] = 16'd115;
    memory[16'd724] = 16'd101;
    memory[16'd725] = 16'd10;
    memory[16'd726] = 16'd0;
    memory[16'd727] = 16'd117;
    memory[16'd728] = 16'd112;
    memory[16'd729] = 16'd100;
    memory[16'd730] = 16'd97;
    memory[16'd731] = 16'd116;
    memory[16'd732] = 16'd105;
    memory[16'd733] = 16'd110;
    memory[16'd734] = 16'd103;
    memory[16'd735] = 16'd32;
    memory[16'd736] = 16'd99;
    memory[16'd737] = 16'd97;
    memory[16'd738] = 16'd99;
    memory[16'd739] = 16'd104;
    memory[16'd740] = 16'd101;
    memory[16'd741] = 16'd10;
    memory[16'd742] = 16'd0;
    memory[16'd743] = 16'd112;
    memory[16'd744] = 16'd117;
    memory[16'd745] = 16'd116;
    memory[16'd746] = 16'd95;
    memory[16'd747] = 16'd105;
    memory[16'd748] = 16'd112;
    memory[16'd749] = 16'd10;
    memory[16'd750] = 16'd0;
    memory[16'd751] = 16'd103;
    memory[16'd752] = 16'd101;
    memory[16'd753] = 16'd116;
    memory[16'd754] = 16'd95;
    memory[16'd755] = 16'd105;
    memory[16'd756] = 16'd112;
    memory[16'd757] = 16'd10;
    memory[16'd758] = 16'd0;
    memory[16'd759] = 16'd105;
    memory[16'd760] = 16'd112;
    memory[16'd761] = 16'd10;
    memory[16'd762] = 16'd0;
    memory[16'd763] = 16'd105;
    memory[16'd764] = 16'd112;
    memory[16'd765] = 16'd32;
    memory[16'd766] = 16'd97;
    memory[16'd767] = 16'd100;
    memory[16'd768] = 16'd100;
    memory[16'd769] = 16'd114;
    memory[16'd770] = 16'd101;
    memory[16'd771] = 16'd115;
    memory[16'd772] = 16'd115;
    memory[16'd773] = 16'd32;
    memory[16'd774] = 16'd103;
    memory[16'd775] = 16'd111;
    memory[16'd776] = 16'd111;
    memory[16'd777] = 16'd100;
    memory[16'd778] = 16'd10;
    memory[16'd779] = 16'd0;
    memory[16'd780] = 16'd105;
    memory[16'd781] = 16'd99;
    memory[16'd782] = 16'd109;
    memory[16'd783] = 16'd112;
    memory[16'd784] = 16'd10;
    memory[16'd785] = 16'd0;
    memory[16'd786] = 16'd112;
    memory[16'd787] = 16'd105;
    memory[16'd788] = 16'd110;
    memory[16'd789] = 16'd103;
    memory[16'd790] = 16'd95;
    memory[16'd791] = 16'd114;
    memory[16'd792] = 16'd101;
    memory[16'd793] = 16'd113;
    memory[16'd794] = 16'd117;
    memory[16'd795] = 16'd101;
    memory[16'd796] = 16'd115;
    memory[16'd797] = 16'd116;
    memory[16'd798] = 16'd10;
    memory[16'd799] = 16'd0;
    memory[16'd800] = 16'd111;
    memory[16'd801] = 16'd116;
    memory[16'd802] = 16'd104;
    memory[16'd803] = 16'd101;
    memory[16'd804] = 16'd114;
    memory[16'd805] = 16'd0;
    memory[16'd1830] = 16'd10;
    memory[16'd1831] = 16'd69;
    memory[16'd1832] = 16'd116;
    memory[16'd1833] = 16'd104;
    memory[16'd1834] = 16'd101;
    memory[16'd1835] = 16'd114;
    memory[16'd1836] = 16'd110;
    memory[16'd1837] = 16'd101;
    memory[16'd1838] = 16'd116;
    memory[16'd1839] = 16'd32;
    memory[16'd1840] = 16'd77;
    memory[16'd1841] = 16'd111;
    memory[16'd1842] = 16'd110;
    memory[16'd1843] = 16'd105;
    memory[16'd1844] = 16'd116;
    memory[16'd1845] = 16'd111;
    memory[16'd1846] = 16'd114;
    memory[16'd1847] = 16'd10;
    memory[16'd1848] = 16'd0;
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
        register_5 <= 16'd0;
        register_39 <= 16'd569;
        register_40 <= 16'd585;
        register_41 <= 16'd601;
        register_42 <= 16'd617;
        register_43 <= 16'd633;
        register_44 <= 16'd0;
        program_counter <= 16'd581;
        register_88 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_9 <= 16'd0;
      end

      16'd3:
      begin
        register_93 <= register_9;
      end

      16'd4:
      begin
        register_93 <= $signed(register_93) + $signed(register_8);
      end

      16'd5:
      begin
        address <= register_93;
      end

      16'd6:
      begin
        register_93 <= data_out;
      end

      16'd7:
      begin
        register_93 <= data_out;
      end

      16'd8:
      begin
        register_93 <= $signed(register_93) != $signed(16'd0);
      end

      16'd9:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 19;
      end

      16'd10:
      begin
        register_93 <= register_9;
      end

      16'd11:
      begin
        register_93 <= $signed(register_93) + $signed(register_8);
      end

      16'd12:
      begin
        address <= register_93;
      end

      16'd13:
      begin
        register_93 <= data_out;
      end

      16'd14:
      begin
        register_93 <= data_out;
      end

      16'd15:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 15;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        register_93 <= register_9;
      end

      16'd17:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd18:
      begin
        register_9 <= register_93;
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
        register_7 <= 16'd0;
        program_counter <= register_6;
      end

      16'd22:
      begin
        register_93 <= register_12;
      end

      16'd23:
      begin
        register_93 <= $signed(register_93) > $signed(16'd9);
      end

      16'd24:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 28;
      end

      16'd25:
      begin
        register_11 <= register_12;
      end

      16'd26:
      begin
        register_11 <= $signed(register_11) + $signed(16'd87);
        program_counter <= register_10;
      end

      16'd27:
      begin
        program_counter <= 16'd28;
      end

      16'd28:
      begin
        register_11 <= register_12;
      end

      16'd29:
      begin
        register_11 <= $signed(register_11) + $signed(16'd48);
        program_counter <= register_10;
      end

      16'd30:
      begin
        register_12 <= register_15;
      end

      16'd31:
      begin
        register_12 <= $signed(register_12) >>> $signed(16'd12);
      end

      16'd32:
      begin
        register_12 <= $signed(register_12) & $signed(16'd15);
        program_counter <= 16'd22;
        register_10 <= 16'd33;
      end

      16'd33:
      begin
        register_93 <= register_11;
      end

      16'd34:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 34;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 35;
        end
      end

      16'd35:
      begin
        register_12 <= register_15;
      end

      16'd36:
      begin
        register_12 <= $signed(register_12) >>> $signed(16'd8);
      end

      16'd37:
      begin
        register_12 <= $signed(register_12) & $signed(16'd15);
        program_counter <= 16'd22;
        register_10 <= 16'd38;
      end

      16'd38:
      begin
        register_93 <= register_11;
      end

      16'd39:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 39;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 40;
        end
      end

      16'd40:
      begin
        register_93 <= 16'd32;
      end

      16'd41:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 41;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 42;
        end
      end

      16'd42:
      begin
        register_12 <= register_15;
      end

      16'd43:
      begin
        register_12 <= $signed(register_12) >>> $signed(16'd4);
      end

      16'd44:
      begin
        register_12 <= $signed(register_12) & $signed(16'd15);
        program_counter <= 16'd22;
        register_10 <= 16'd45;
      end

      16'd45:
      begin
        register_93 <= register_11;
      end

      16'd46:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 46;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 47;
        end
      end

      16'd47:
      begin
        register_12 <= register_15;
      end

      16'd48:
      begin
        register_12 <= $signed(register_12) & $signed(16'd15);
        program_counter <= 16'd22;
        register_10 <= 16'd49;
      end

      16'd49:
      begin
        register_93 <= register_11;
      end

      16'd50:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 50;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 51;
        end
      end

      16'd51:
      begin
        register_93 <= 16'd32;
      end

      16'd52:
      begin
        s_output_rs232_tx <= register_93;
        program_counter <= 52;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 53;
        end
      end

      16'd53:
      begin
        register_14 <= 16'd0;
        program_counter <= register_13;
      end

      16'd54:
      begin
        register_24 <= 16'd0;
        register_25 <= 16'd0;
        register_26 <= 16'd512;
      end

      16'd55:
      begin
        register_8 <= register_26;
        program_counter <= 16'd2;
        register_6 <= 16'd56;
      end

      16'd56:
      begin
        register_93 <= register_7;
        register_94 <= 16'd0;
      end

      16'd57:
      begin
        register_93 <= register_20;
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd58:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_21;
        register_94 <= 16'd1;
      end

      16'd59:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd60:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_22;
        register_94 <= 16'd2;
      end

      16'd61:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd62:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_0;
        register_94 <= 16'd3;
      end

      16'd63:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd64:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_1;
        register_94 <= 16'd4;
      end

      16'd65:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd66:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_2;
        register_94 <= 16'd5;
      end

      16'd67:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd68:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_23;
        register_94 <= 16'd6;
      end

      16'd69:
      begin
        register_94 <= $signed(register_94) + $signed(register_18);
      end

      16'd70:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_19;
      end

      16'd71:
      begin
        s_output_eth_tx <= register_93;
        program_counter <= 71;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 72;
        end
      end

      16'd72:
      begin
        register_93 <= 16'd0;
      end

      16'd73:
      begin
        register_25 <= register_93;
        register_93 <= 16'd0;
      end

      16'd74:
      begin
        register_24 <= register_93;
      end

      16'd75:
      begin
        register_93 <= register_24;
        register_94 <= register_19;
      end

      16'd76:
      begin
        register_93 <= $signed(register_93) < $signed(register_94);
      end

      16'd77:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 90;
      end

      16'd78:
      begin
        register_93 <= register_25;
      end

      16'd79:
      begin
        register_93 <= $signed(register_93) + $signed(register_18);
      end

      16'd80:
      begin
        address <= register_93;
      end

      16'd81:
      begin
        register_93 <= data_out;
      end

      16'd82:
      begin
        register_93 <= data_out;
      end

      16'd83:
      begin
        s_output_eth_tx <= register_93;
        program_counter <= 83;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 84;
        end
      end

      16'd84:
      begin
        register_93 <= register_25;
      end

      16'd85:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd86:
      begin
        register_25 <= register_93;
      end

      16'd87:
      begin
        register_93 <= register_24;
      end

      16'd88:
      begin
        register_93 <= $signed(register_93) + $signed(16'd2);
      end

      16'd89:
      begin
        register_24 <= register_93;
        program_counter <= 16'd75;
      end

      16'd90:
      begin
        register_17 <= 16'd0;
        program_counter <= register_16;
      end

      16'd91:
      begin
        register_30 <= 16'd521;
      end

      16'd92:
      begin
        register_8 <= register_30;
        program_counter <= 16'd2;
        register_6 <= 16'd93;
      end

      16'd93:
      begin
        register_93 <= register_7;
        register_31 <= 16'd0;
        register_32 <= 16'd0;
        register_33 <= 16'd0;
      end

      16'd94:
      begin
        register_93 <= input_eth_rx;
        program_counter <= 94;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd95;
        end
      end

      16'd95:
      begin
        register_31 <= register_93;
        register_34 <= 16'd530;
      end

      16'd96:
      begin
        register_8 <= register_34;
        program_counter <= 16'd2;
        register_6 <= 16'd97;
      end

      16'd97:
      begin
        register_93 <= register_7;
        register_15 <= register_31;
        program_counter <= 16'd30;
        register_13 <= 16'd98;
      end

      16'd98:
      begin
        register_93 <= register_14;
        register_35 <= 16'd546;
      end

      16'd99:
      begin
        register_8 <= register_35;
        program_counter <= 16'd2;
        register_6 <= 16'd100;
      end

      16'd100:
      begin
        register_93 <= register_7;
      end

      16'd101:
      begin
        register_93 <= 16'd0;
      end

      16'd102:
      begin
        register_32 <= register_93;
        register_93 <= 16'd0;
      end

      16'd103:
      begin
        register_33 <= register_93;
      end

      16'd104:
      begin
        register_93 <= register_33;
        register_94 <= register_31;
      end

      16'd105:
      begin
        register_93 <= $signed(register_93) < $signed(register_94);
      end

      16'd106:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 116;
      end

      16'd107:
      begin
        register_93 <= input_eth_rx;
        program_counter <= 107;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd108;
        end
      end

      16'd108:
      begin
        register_94 <= register_32;
      end

      16'd109:
      begin
        register_94 <= $signed(register_94) + $signed(register_29);
      end

      16'd110:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_32;
      end

      16'd111:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd112:
      begin
        register_32 <= register_93;
      end

      16'd113:
      begin
        register_93 <= register_33;
      end

      16'd114:
      begin
        register_93 <= $signed(register_93) + $signed(16'd2);
      end

      16'd115:
      begin
        register_33 <= register_93;
        program_counter <= 16'd104;
      end

      16'd116:
      begin
        register_36 <= 16'd548;
      end

      16'd117:
      begin
        register_8 <= register_36;
        program_counter <= 16'd2;
        register_6 <= 16'd118;
      end

      16'd118:
      begin
        register_93 <= register_7;
        register_94 <= register_0;
      end

      16'd119:
      begin
        register_93 <= 16'd0;
      end

      16'd120:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd121:
      begin
        address <= register_93;
      end

      16'd122:
      begin
        register_93 <= data_out;
      end

      16'd123:
      begin
        register_93 <= data_out;
      end

      16'd124:
      begin
        register_93 <= $signed(register_93) != $signed(register_94);
      end

      16'd125:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 132;
      end

      16'd126:
      begin
        register_93 <= 16'd0;
      end

      16'd127:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd128:
      begin
        address <= register_93;
      end

      16'd129:
      begin
        register_93 <= data_out;
      end

      16'd130:
      begin
        register_93 <= data_out;
      end

      16'd131:
      begin
        register_93 <= $signed(register_93) != $signed(16'd65535);
      end

      16'd132:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 135;
      end

      16'd133:
      begin
        program_counter <= 16'd94;
      end

      16'd134:
      begin
        program_counter <= 16'd135;
      end

      16'd135:
      begin
        register_93 <= 16'd1;
        register_94 <= register_1;
      end

      16'd136:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd137:
      begin
        address <= register_93;
      end

      16'd138:
      begin
        register_93 <= data_out;
      end

      16'd139:
      begin
        register_93 <= data_out;
      end

      16'd140:
      begin
        register_93 <= $signed(register_93) != $signed(register_94);
      end

      16'd141:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 148;
      end

      16'd142:
      begin
        register_93 <= 16'd1;
      end

      16'd143:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd144:
      begin
        address <= register_93;
      end

      16'd145:
      begin
        register_93 <= data_out;
      end

      16'd146:
      begin
        register_93 <= data_out;
      end

      16'd147:
      begin
        register_93 <= $signed(register_93) != $signed(16'd65535);
      end

      16'd148:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 151;
      end

      16'd149:
      begin
        program_counter <= 16'd94;
      end

      16'd150:
      begin
        program_counter <= 16'd151;
      end

      16'd151:
      begin
        register_93 <= 16'd2;
        register_94 <= register_2;
      end

      16'd152:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd153:
      begin
        address <= register_93;
      end

      16'd154:
      begin
        register_93 <= data_out;
      end

      16'd155:
      begin
        register_93 <= data_out;
      end

      16'd156:
      begin
        register_93 <= $signed(register_93) != $signed(register_94);
      end

      16'd157:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 164;
      end

      16'd158:
      begin
        register_93 <= 16'd2;
      end

      16'd159:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd160:
      begin
        address <= register_93;
      end

      16'd161:
      begin
        register_93 <= data_out;
      end

      16'd162:
      begin
        register_93 <= data_out;
      end

      16'd163:
      begin
        register_93 <= $signed(register_93) != $signed(16'd65535);
      end

      16'd164:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 167;
      end

      16'd165:
      begin
        program_counter <= 16'd94;
      end

      16'd166:
      begin
        program_counter <= 16'd167;
      end

      16'd167:
      begin
        register_37 <= 16'd554;
      end

      16'd168:
      begin
        register_8 <= register_37;
        program_counter <= 16'd2;
        register_6 <= 16'd169;
      end

      16'd169:
      begin
        register_93 <= register_7;
      end

      16'd170:
      begin
        register_93 <= 16'd6;
      end

      16'd171:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd172:
      begin
        address <= register_93;
      end

      16'd173:
      begin
        register_93 <= data_out;
      end

      16'd174:
      begin
        register_93 <= data_out;
      end

      16'd175:
      begin
        register_93 <= $signed(register_93) == $signed(16'd2054);
      end

      16'd176:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 243;
      end

      16'd177:
      begin
        register_38 <= 16'd564;
      end

      16'd178:
      begin
        register_8 <= register_38;
        program_counter <= 16'd2;
        register_6 <= 16'd179;
      end

      16'd179:
      begin
        register_93 <= register_7;
      end

      16'd180:
      begin
        register_93 <= 16'd10;
      end

      16'd181:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
      end

      16'd182:
      begin
        address <= register_93;
      end

      16'd183:
      begin
        register_93 <= data_out;
      end

      16'd184:
      begin
        register_93 <= data_out;
      end

      16'd185:
      begin
        register_93 <= $signed(register_93) == $signed(16'd1);
      end

      16'd186:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 241;
      end

      16'd187:
      begin
        register_93 <= 16'd1;
        register_94 <= 16'd7;
        register_18 <= register_5;
        register_19 <= 16'd64;
        register_20 <= 16'd11;
        register_21 <= 16'd12;
        register_22 <= 16'd13;
        register_23 <= 16'd2054;
      end

      16'd188:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
        register_20 <= $signed(register_20) + $signed(register_29);
        register_21 <= $signed(register_21) + $signed(register_29);
        register_22 <= $signed(register_22) + $signed(register_29);
      end

      16'd189:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd2048;
        register_94 <= 16'd8;
      end

      16'd190:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd191:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd1540;
        register_94 <= 16'd9;
      end

      16'd192:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd193:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd2;
        register_94 <= 16'd10;
      end

      16'd194:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd195:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_0;
        register_94 <= 16'd11;
      end

      16'd196:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd197:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_1;
        register_94 <= 16'd12;
      end

      16'd198:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd199:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_2;
        register_94 <= 16'd13;
      end

      16'd200:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd201:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_3;
        register_94 <= 16'd14;
      end

      16'd202:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd203:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_4;
        register_94 <= 16'd15;
      end

      16'd204:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd205:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd11;
        register_94 <= 16'd16;
      end

      16'd206:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd207:
      begin
        address <= register_93;
      end

      16'd208:
      begin
        register_93 <= data_out;
      end

      16'd209:
      begin
        register_93 <= data_out;
      end

      16'd210:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd12;
        register_94 <= 16'd17;
      end

      16'd211:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd212:
      begin
        address <= register_93;
      end

      16'd213:
      begin
        register_93 <= data_out;
      end

      16'd214:
      begin
        register_93 <= data_out;
      end

      16'd215:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd13;
        register_94 <= 16'd18;
      end

      16'd216:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd217:
      begin
        address <= register_93;
      end

      16'd218:
      begin
        register_93 <= data_out;
      end

      16'd219:
      begin
        register_93 <= data_out;
      end

      16'd220:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd14;
        register_94 <= 16'd19;
      end

      16'd221:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd222:
      begin
        address <= register_93;
      end

      16'd223:
      begin
        register_93 <= data_out;
      end

      16'd224:
      begin
        register_93 <= data_out;
      end

      16'd225:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd15;
        register_94 <= 16'd20;
      end

      16'd226:
      begin
        register_93 <= $signed(register_93) + $signed(register_29);
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd227:
      begin
        address <= register_93;
      end

      16'd228:
      begin
        register_93 <= data_out;
      end

      16'd229:
      begin
        register_93 <= data_out;
      end

      16'd230:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
      end

      16'd231:
      begin
        address <= register_20;
      end

      16'd232:
      begin
        register_20 <= data_out;
      end

      16'd233:
      begin
        register_20 <= data_out;
      end

      16'd234:
      begin
        address <= register_21;
      end

      16'd235:
      begin
        register_21 <= data_out;
      end

      16'd236:
      begin
        register_21 <= data_out;
      end

      16'd237:
      begin
        address <= register_22;
      end

      16'd238:
      begin
        register_22 <= data_out;
      end

      16'd239:
      begin
        register_22 <= data_out;
        program_counter <= 16'd54;
        register_16 <= 16'd240;
      end

      16'd240:
      begin
        register_93 <= register_17;
        program_counter <= 16'd241;
      end

      16'd241:
      begin
        program_counter <= 16'd94;
      end

      16'd242:
      begin
        program_counter <= 16'd243;
      end

      16'd243:
      begin
        program_counter <= 16'd245;
      end

      16'd244:
      begin
        program_counter <= 16'd94;
      end

      16'd245:
      begin
        register_28 <= register_31;
        program_counter <= register_27;
      end

      16'd246:
      begin
        register_49 <= 16'd0;
        register_50 <= 16'd0;
        register_51 <= 16'd649;
        register_52 <= 16'd0;
        register_93 <= 16'd0;
      end

      16'd247:
      begin
        register_52 <= register_93;
      end

      16'd248:
      begin
        register_93 <= register_52;
      end

      16'd249:
      begin
        register_93 <= $signed(register_93) < $signed(16'd16);
      end

      16'd250:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 272;
      end

      16'd251:
      begin
        register_93 <= register_52;
        register_94 <= register_47;
      end

      16'd252:
      begin
        register_93 <= $signed(register_93) + $signed(register_39);
      end

      16'd253:
      begin
        address <= register_93;
      end

      16'd254:
      begin
        register_93 <= data_out;
      end

      16'd255:
      begin
        register_93 <= data_out;
      end

      16'd256:
      begin
        register_93 <= $signed(register_93) == $signed(register_94);
      end

      16'd257:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 264;
      end

      16'd258:
      begin
        register_93 <= register_52;
        register_94 <= register_48;
      end

      16'd259:
      begin
        register_93 <= $signed(register_93) + $signed(register_40);
      end

      16'd260:
      begin
        address <= register_93;
      end

      16'd261:
      begin
        register_93 <= data_out;
      end

      16'd262:
      begin
        register_93 <= data_out;
      end

      16'd263:
      begin
        register_93 <= $signed(register_93) == $signed(register_94);
      end

      16'd264:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 269;
      end

      16'd265:
      begin
        register_53 <= 16'd665;
      end

      16'd266:
      begin
        register_8 <= register_53;
        program_counter <= 16'd2;
        register_6 <= 16'd267;
      end

      16'd267:
      begin
        register_93 <= register_7;
        register_46 <= register_52;
        program_counter <= register_45;
      end

      16'd268:
      begin
        program_counter <= 16'd269;
      end

      16'd269:
      begin
        register_93 <= register_52;
      end

      16'd270:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd271:
      begin
        register_52 <= register_93;
        program_counter <= 16'd248;
      end

      16'd272:
      begin
        register_54 <= 16'd676;
      end

      16'd273:
      begin
        register_8 <= register_54;
        program_counter <= 16'd2;
        register_6 <= 16'd274;
      end

      16'd274:
      begin
        register_93 <= register_7;
        register_94 <= 16'd7;
        register_18 <= register_5;
        register_19 <= 16'd64;
        register_20 <= 16'd65535;
        register_21 <= 16'd65535;
        register_22 <= 16'd65535;
        register_23 <= 16'd2054;
      end

      16'd275:
      begin
        register_93 <= 16'd1;
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd276:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd2048;
        register_94 <= 16'd8;
      end

      16'd277:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd278:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd1540;
        register_94 <= 16'd9;
      end

      16'd279:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd280:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd1;
        register_94 <= 16'd10;
      end

      16'd281:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd282:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_0;
        register_94 <= 16'd11;
      end

      16'd283:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd284:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_1;
        register_94 <= 16'd12;
      end

      16'd285:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd286:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_2;
        register_94 <= 16'd13;
      end

      16'd287:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd288:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_3;
        register_94 <= 16'd14;
      end

      16'd289:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd290:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_4;
        register_94 <= 16'd15;
      end

      16'd291:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd292:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_47;
        register_94 <= 16'd19;
      end

      16'd293:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd294:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_48;
        register_94 <= 16'd20;
      end

      16'd295:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd296:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        program_counter <= 16'd54;
        register_16 <= 16'd297;
      end

      16'd297:
      begin
        register_93 <= register_17;
        register_55 <= 16'd688;
      end

      16'd298:
      begin
        register_8 <= register_55;
        program_counter <= 16'd2;
        register_6 <= 16'd299;
      end

      16'd299:
      begin
        register_93 <= register_7;
      end

      16'd300:
      begin
        register_93 <= input_eth_rx;
        program_counter <= 300;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd301;
        end
      end

      16'd301:
      begin
        register_49 <= register_93;
        register_93 <= 16'd0;
      end

      16'd302:
      begin
        register_52 <= register_93;
        register_93 <= 16'd0;
      end

      16'd303:
      begin
        register_50 <= register_93;
      end

      16'd304:
      begin
        register_93 <= register_50;
        register_94 <= register_49;
      end

      16'd305:
      begin
        register_93 <= $signed(register_93) < $signed(register_94);
      end

      16'd306:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 321;
      end

      16'd307:
      begin
        register_93 <= register_52;
      end

      16'd308:
      begin
        register_93 <= $signed(register_93) < $signed(16'd16);
      end

      16'd309:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 314;
      end

      16'd310:
      begin
        register_93 <= input_eth_rx;
        program_counter <= 310;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd311;
        end
      end

      16'd311:
      begin
        register_94 <= register_52;
      end

      16'd312:
      begin
        register_94 <= $signed(register_94) + $signed(register_51);
      end

      16'd313:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        program_counter <= 16'd315;
      end

      16'd314:
      begin
        register_93 <= input_eth_rx;
        program_counter <= 314;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd315;
        end
      end

      16'd315:
      begin
        register_93 <= register_52;
      end

      16'd316:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd317:
      begin
        register_52 <= register_93;
      end

      16'd318:
      begin
        register_93 <= register_50;
      end

      16'd319:
      begin
        register_93 <= $signed(register_93) + $signed(16'd2);
      end

      16'd320:
      begin
        register_50 <= register_93;
        program_counter <= 16'd304;
      end

      16'd321:
      begin
        register_56 <= 16'd701;
      end

      16'd322:
      begin
        register_8 <= register_56;
        program_counter <= 16'd2;
        register_6 <= 16'd323;
      end

      16'd323:
      begin
        register_93 <= register_7;
      end

      16'd324:
      begin
        register_93 <= 16'd6;
      end

      16'd325:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
      end

      16'd326:
      begin
        address <= register_93;
      end

      16'd327:
      begin
        register_93 <= data_out;
      end

      16'd328:
      begin
        register_93 <= data_out;
      end

      16'd329:
      begin
        register_93 <= $signed(register_93) == $signed(16'd2054);
      end

      16'd330:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 337;
      end

      16'd331:
      begin
        register_93 <= 16'd10;
      end

      16'd332:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
      end

      16'd333:
      begin
        address <= register_93;
      end

      16'd334:
      begin
        register_93 <= data_out;
      end

      16'd335:
      begin
        register_93 <= data_out;
      end

      16'd336:
      begin
        register_93 <= $signed(register_93) == $signed(16'd2);
      end

      16'd337:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 388;
      end

      16'd338:
      begin
        register_57 <= 16'd713;
      end

      16'd339:
      begin
        register_8 <= register_57;
        program_counter <= 16'd2;
        register_6 <= 16'd340;
      end

      16'd340:
      begin
        register_93 <= register_7;
        register_94 <= register_47;
      end

      16'd341:
      begin
        register_93 <= 16'd14;
      end

      16'd342:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
      end

      16'd343:
      begin
        address <= register_93;
      end

      16'd344:
      begin
        register_93 <= data_out;
      end

      16'd345:
      begin
        register_93 <= data_out;
      end

      16'd346:
      begin
        register_93 <= $signed(register_93) == $signed(register_94);
      end

      16'd347:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 354;
      end

      16'd348:
      begin
        register_93 <= 16'd15;
        register_94 <= register_48;
      end

      16'd349:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
      end

      16'd350:
      begin
        address <= register_93;
      end

      16'd351:
      begin
        register_93 <= data_out;
      end

      16'd352:
      begin
        register_93 <= data_out;
      end

      16'd353:
      begin
        register_93 <= $signed(register_93) == $signed(register_94);
      end

      16'd354:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 387;
      end

      16'd355:
      begin
        register_58 <= 16'd727;
      end

      16'd356:
      begin
        register_8 <= register_58;
        program_counter <= 16'd2;
        register_6 <= 16'd357;
      end

      16'd357:
      begin
        register_93 <= register_7;
        register_94 <= register_44;
      end

      16'd358:
      begin
        register_93 <= register_47;
        register_94 <= $signed(register_94) + $signed(register_39);
      end

      16'd359:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_48;
        register_94 <= register_44;
      end

      16'd360:
      begin
        register_94 <= $signed(register_94) + $signed(register_40);
      end

      16'd361:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd11;
        register_94 <= register_44;
      end

      16'd362:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
        register_94 <= $signed(register_94) + $signed(register_41);
      end

      16'd363:
      begin
        address <= register_93;
      end

      16'd364:
      begin
        register_93 <= data_out;
      end

      16'd365:
      begin
        register_93 <= data_out;
      end

      16'd366:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd12;
        register_94 <= register_44;
      end

      16'd367:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
        register_94 <= $signed(register_94) + $signed(register_42);
      end

      16'd368:
      begin
        address <= register_93;
      end

      16'd369:
      begin
        register_93 <= data_out;
      end

      16'd370:
      begin
        register_93 <= data_out;
      end

      16'd371:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd13;
        register_94 <= register_44;
      end

      16'd372:
      begin
        register_93 <= $signed(register_93) + $signed(register_51);
        register_94 <= $signed(register_94) + $signed(register_43);
      end

      16'd373:
      begin
        address <= register_93;
      end

      16'd374:
      begin
        register_93 <= data_out;
      end

      16'd375:
      begin
        register_93 <= data_out;
      end

      16'd376:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_44;
      end

      16'd377:
      begin
        register_52 <= register_93;
        register_93 <= register_44;
      end

      16'd378:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd379:
      begin
        register_44 <= register_93;
      end

      16'd380:
      begin
        register_93 <= register_44;
      end

      16'd381:
      begin
        register_93 <= $signed(register_93) == $signed(16'd16);
      end

      16'd382:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 385;
      end

      16'd383:
      begin
        register_93 <= 16'd0;
      end

      16'd384:
      begin
        register_44 <= register_93;
        program_counter <= 16'd385;
      end

      16'd385:
      begin
        register_46 <= register_52;
        program_counter <= register_45;
      end

      16'd386:
      begin
        program_counter <= 16'd387;
      end

      16'd387:
      begin
        program_counter <= 16'd388;
      end

      16'd388:
      begin
        program_counter <= 16'd300;
      end

      16'd389:
      begin
        register_66 <= 16'd743;
      end

      16'd390:
      begin
        register_8 <= register_66;
        program_counter <= 16'd2;
        register_6 <= 16'd391;
      end

      16'd391:
      begin
        register_93 <= register_7;
        register_67 <= 16'd0;
        register_68 <= 16'd0;
        register_69 <= 16'd0;
        register_47 <= register_64;
        register_48 <= register_65;
        program_counter <= 16'd246;
        register_45 <= 16'd392;
      end

      16'd392:
      begin
        register_93 <= register_46;
        register_94 <= 16'd7;
      end

      16'd393:
      begin
        register_69 <= register_93;
        register_93 <= 16'd17664;
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd394:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_62;
        register_94 <= 16'd8;
      end

      16'd395:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd396:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd0;
        register_94 <= 16'd9;
      end

      16'd397:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd398:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd16384;
        register_94 <= 16'd10;
      end

      16'd399:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd400:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_63;
        register_94 <= 16'd11;
      end

      16'd401:
      begin
        register_93 <= $signed(16'd65280) | $signed(register_93);
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd402:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= 16'd0;
        register_94 <= 16'd12;
      end

      16'd403:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd404:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_3;
        register_94 <= 16'd13;
      end

      16'd405:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd406:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_4;
        register_94 <= 16'd14;
      end

      16'd407:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd408:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_64;
        register_94 <= 16'd15;
      end

      16'd409:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd410:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_65;
        register_94 <= 16'd16;
      end

      16'd411:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd412:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_62;
      end

      16'd413:
      begin
        register_93 <= $signed(register_93) + $signed(16'd14);
      end

      16'd414:
      begin
        register_67 <= register_93;
        register_93 <= 16'd10;
      end

      16'd415:
      begin
        s_output_checksum <= register_93;
        program_counter <= 415;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 416;
        end
      end

      16'd416:
      begin
        register_93 <= 16'd7;
      end

      16'd417:
      begin
        register_68 <= register_93;
      end

      16'd418:
      begin
        register_93 <= register_68;
      end

      16'd419:
      begin
        register_93 <= $signed(register_93) <= $signed(16'd16);
      end

      16'd420:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 430;
      end

      16'd421:
      begin
        register_93 <= register_68;
      end

      16'd422:
      begin
        register_93 <= $signed(register_93) + $signed(register_61);
      end

      16'd423:
      begin
        address <= register_93;
      end

      16'd424:
      begin
        register_93 <= data_out;
      end

      16'd425:
      begin
        register_93 <= data_out;
      end

      16'd426:
      begin
        s_output_checksum <= register_93;
        program_counter <= 426;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 427;
        end
      end

      16'd427:
      begin
        register_93 <= register_68;
      end

      16'd428:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd429:
      begin
        register_68 <= register_93;
        program_counter <= 16'd418;
      end

      16'd430:
      begin
        register_93 <= input_checksum;
        program_counter <= 430;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd431;
        end
      end

      16'd431:
      begin
        register_94 <= 16'd12;
      end

      16'd432:
      begin
        register_94 <= $signed(register_94) + $signed(register_61);
      end

      16'd433:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_67;
      end

      16'd434:
      begin
        register_93 <= $signed(register_93) < $signed(16'd64);
      end

      16'd435:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 438;
      end

      16'd436:
      begin
        register_93 <= 16'd64;
      end

      16'd437:
      begin
        register_67 <= register_93;
        program_counter <= 16'd438;
      end

      16'd438:
      begin
        register_18 <= register_61;
        register_19 <= register_67;
        register_20 <= register_69;
        register_21 <= register_69;
        register_22 <= register_69;
        register_23 <= 16'd2048;
      end

      16'd439:
      begin
        register_20 <= $signed(register_20) + $signed(register_41);
        register_21 <= $signed(register_21) + $signed(register_42);
        register_22 <= $signed(register_22) + $signed(register_43);
      end

      16'd440:
      begin
        address <= register_20;
      end

      16'd441:
      begin
        register_20 <= data_out;
      end

      16'd442:
      begin
        register_20 <= data_out;
      end

      16'd443:
      begin
        address <= register_21;
      end

      16'd444:
      begin
        register_21 <= data_out;
      end

      16'd445:
      begin
        register_21 <= data_out;
      end

      16'd446:
      begin
        address <= register_22;
      end

      16'd447:
      begin
        register_22 <= data_out;
      end

      16'd448:
      begin
        register_22 <= data_out;
        program_counter <= 16'd54;
        register_16 <= 16'd449;
      end

      16'd449:
      begin
        register_93 <= register_17;
        register_60 <= 16'd0;
        program_counter <= register_59;
      end

      16'd450:
      begin
        register_73 <= 16'd0;
        register_74 <= 16'd0;
        register_75 <= 16'd0;
        register_76 <= 16'd0;
        register_77 <= 16'd0;
        register_78 <= 16'd0;
        register_79 <= 16'd0;
        register_80 <= 16'd0;
        register_81 <= 16'd0;
        register_82 <= 16'd751;
      end

      16'd451:
      begin
        register_8 <= register_82;
        program_counter <= 16'd2;
        register_6 <= 16'd452;
      end

      16'd452:
      begin
        register_93 <= register_7;
      end

      16'd453:
      begin
        register_29 <= register_72;
        program_counter <= 16'd91;
        register_27 <= 16'd454;
      end

      16'd454:
      begin
        register_93 <= register_28;
      end

      16'd455:
      begin
        register_67 <= register_93;
        register_93 <= 16'd6;
      end

      16'd456:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd457:
      begin
        address <= register_93;
      end

      16'd458:
      begin
        register_93 <= data_out;
      end

      16'd459:
      begin
        register_93 <= data_out;
      end

      16'd460:
      begin
        register_93 <= $signed(register_93) == $signed(16'd2048);
      end

      16'd461:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 576;
      end

      16'd462:
      begin
        register_83 <= 16'd759;
      end

      16'd463:
      begin
        register_8 <= register_83;
        program_counter <= 16'd2;
        register_6 <= 16'd464;
      end

      16'd464:
      begin
        register_93 <= register_7;
        register_94 <= register_3;
      end

      16'd465:
      begin
        register_93 <= 16'd15;
      end

      16'd466:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd467:
      begin
        address <= register_93;
      end

      16'd468:
      begin
        register_93 <= data_out;
      end

      16'd469:
      begin
        register_93 <= data_out;
      end

      16'd470:
      begin
        register_93 <= $signed(register_93) != $signed(register_94);
      end

      16'd471:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 474;
      end

      16'd472:
      begin
        program_counter <= 16'd453;
      end

      16'd473:
      begin
        program_counter <= 16'd474;
      end

      16'd474:
      begin
        register_93 <= 16'd16;
        register_94 <= register_4;
      end

      16'd475:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd476:
      begin
        address <= register_93;
      end

      16'd477:
      begin
        register_93 <= data_out;
      end

      16'd478:
      begin
        register_93 <= data_out;
      end

      16'd479:
      begin
        register_93 <= $signed(register_93) != $signed(register_94);
      end

      16'd480:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 483;
      end

      16'd481:
      begin
        program_counter <= 16'd453;
      end

      16'd482:
      begin
        program_counter <= 16'd483;
      end

      16'd483:
      begin
        register_84 <= 16'd763;
      end

      16'd484:
      begin
        register_8 <= register_84;
        program_counter <= 16'd2;
        register_6 <= 16'd485;
      end

      16'd485:
      begin
        register_93 <= register_7;
      end

      16'd486:
      begin
        register_93 <= 16'd11;
      end

      16'd487:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd488:
      begin
        address <= register_93;
      end

      16'd489:
      begin
        register_93 <= data_out;
      end

      16'd490:
      begin
        register_93 <= data_out;
      end

      16'd491:
      begin
        register_93 <= $signed(register_93) & $signed(16'd255);
      end

      16'd492:
      begin
        register_93 <= $signed(register_93) == $signed(16'd1);
      end

      16'd493:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 575;
      end

      16'd494:
      begin
        register_93 <= 16'd7;
        register_85 <= 16'd780;
      end

      16'd495:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
        register_8 <= register_85;
      end

      16'd496:
      begin
        address <= register_93;
      end

      16'd497:
      begin
        register_93 <= data_out;
      end

      16'd498:
      begin
        register_93 <= data_out;
      end

      16'd499:
      begin
        register_93 <= $signed(register_93) >>> $signed(16'd8);
      end

      16'd500:
      begin
        register_93 <= $signed(register_93) & $signed(16'd15);
      end

      16'd501:
      begin
        register_93 <= $signed(register_93) << $signed(16'd1);
      end

      16'd502:
      begin
        register_75 <= register_93;
      end

      16'd503:
      begin
        register_93 <= register_75;
        register_94 <= register_75;
      end

      16'd504:
      begin
        register_93 <= $signed(register_93) + $signed(16'd7);
      end

      16'd505:
      begin
        register_76 <= register_93;
        register_93 <= 16'd8;
      end

      16'd506:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd507:
      begin
        address <= register_93;
      end

      16'd508:
      begin
        register_93 <= data_out;
      end

      16'd509:
      begin
        register_93 <= data_out;
      end

      16'd510:
      begin
        register_74 <= register_93;
      end

      16'd511:
      begin
        register_93 <= register_74;
      end

      16'd512:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd513:
      begin
        register_93 <= $signed(register_93) >>> $signed(16'd1);
      end

      16'd514:
      begin
        register_93 <= $signed(register_93) - $signed(register_94);
      end

      16'd515:
      begin
        register_77 <= register_93;
        register_93 <= register_76;
      end

      16'd516:
      begin
        register_94 <= register_77;
      end

      16'd517:
      begin
        register_93 <= $signed(register_93) + $signed(register_94);
      end

      16'd518:
      begin
        register_93 <= $signed(register_93) - $signed(16'd1);
      end

      16'd519:
      begin
        register_81 <= register_93;
        program_counter <= 16'd2;
        register_6 <= 16'd520;
      end

      16'd520:
      begin
        register_93 <= register_7;
      end

      16'd521:
      begin
        register_93 <= register_76;
      end

      16'd522:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd523:
      begin
        address <= register_93;
      end

      16'd524:
      begin
        register_93 <= data_out;
      end

      16'd525:
      begin
        register_93 <= data_out;
      end

      16'd526:
      begin
        register_93 <= $signed(register_93) == $signed(16'd2048);
      end

      16'd527:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 574;
      end

      16'd528:
      begin
        register_86 <= 16'd786;
      end

      16'd529:
      begin
        register_8 <= register_86;
        program_counter <= 16'd2;
        register_6 <= 16'd530;
      end

      16'd530:
      begin
        register_93 <= register_7;
      end

      16'd531:
      begin
        register_93 <= 16'd19;
      end

      16'd532:
      begin
        register_80 <= register_93;
        register_93 <= register_77;
      end

      16'd533:
      begin
        s_output_checksum <= register_93;
        program_counter <= 533;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 534;
        end
      end

      16'd534:
      begin
        register_93 <= 16'd0;
      end

      16'd535:
      begin
        s_output_checksum <= register_93;
        program_counter <= 535;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 536;
        end
      end

      16'd536:
      begin
        register_93 <= 16'd0;
      end

      16'd537:
      begin
        s_output_checksum <= register_93;
        program_counter <= 537;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 538;
        end
      end

      16'd538:
      begin
        register_93 <= register_76;
      end

      16'd539:
      begin
        register_93 <= $signed(register_93) + $signed(16'd2);
      end

      16'd540:
      begin
        register_79 <= register_93;
      end

      16'd541:
      begin
        register_93 <= register_79;
        register_94 <= register_81;
      end

      16'd542:
      begin
        register_93 <= $signed(register_93) <= $signed(register_94);
      end

      16'd543:
      begin
        if (register_93 == 16'h0000)
          program_counter <= 560;
      end

      16'd544:
      begin
        register_93 <= register_79;
      end

      16'd545:
      begin
        register_93 <= $signed(register_93) + $signed(register_72);
      end

      16'd546:
      begin
        address <= register_93;
      end

      16'd547:
      begin
        register_93 <= data_out;
      end

      16'd548:
      begin
        register_93 <= data_out;
      end

      16'd549:
      begin
        register_78 <= register_93;
      end

      16'd550:
      begin
        register_93 <= register_78;
      end

      16'd551:
      begin
        s_output_checksum <= register_93;
        program_counter <= 551;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 552;
        end
      end

      16'd552:
      begin
        register_93 <= register_78;
        register_94 <= register_80;
      end

      16'd553:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd554:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
        register_93 <= register_80;
      end

      16'd555:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd556:
      begin
        register_80 <= register_93;
      end

      16'd557:
      begin
        register_93 <= register_79;
      end

      16'd558:
      begin
        register_93 <= $signed(register_93) + $signed(16'd1);
      end

      16'd559:
      begin
        register_79 <= register_93;
        program_counter <= 16'd541;
      end

      16'd560:
      begin
        register_93 <= 16'd0;
        register_94 <= 16'd17;
      end

      16'd561:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
      end

      16'd562:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
      end

      16'd563:
      begin
        register_93 <= input_checksum;
        program_counter <= 563;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd564;
        end
      end

      16'd564:
      begin
        register_94 <= 16'd18;
        register_61 <= register_5;
        register_62 <= register_74;
        register_63 <= 16'd1;
        register_64 <= 16'd13;
        register_65 <= 16'd14;
      end

      16'd565:
      begin
        register_94 <= $signed(register_94) + $signed(register_5);
        register_64 <= $signed(register_64) + $signed(register_72);
        register_65 <= $signed(register_65) + $signed(register_72);
      end

      16'd566:
      begin
        address <= register_94;
        data_in <= register_93;
        write_enable <= 1'b1;
      end

      16'd567:
      begin
        address <= register_64;
      end

      16'd568:
      begin
        register_64 <= data_out;
      end

      16'd569:
      begin
        register_64 <= data_out;
      end

      16'd570:
      begin
        address <= register_65;
      end

      16'd571:
      begin
        register_65 <= data_out;
      end

      16'd572:
      begin
        register_65 <= data_out;
        program_counter <= 16'd389;
        register_59 <= 16'd573;
      end

      16'd573:
      begin
        register_93 <= register_60;
        program_counter <= 16'd574;
      end

      16'd574:
      begin
        program_counter <= 16'd575;
      end

      16'd575:
      begin
        program_counter <= 16'd579;
      end

      16'd576:
      begin
        register_87 <= 16'd800;
      end

      16'd577:
      begin
        register_8 <= register_87;
        program_counter <= 16'd2;
        register_6 <= 16'd578;
      end

      16'd578:
      begin
        register_93 <= register_7;
      end

      16'd579:
      begin
        program_counter <= 16'd453;
      end

      16'd580:
      begin
        register_71 <= register_67;
        program_counter <= register_70;
      end

      16'd581:
      begin
        register_90 <= 16'd0;
        register_91 <= 16'd806;
        register_92 <= 16'd1830;
      end

      16'd582:
      begin
        register_8 <= register_92;
        program_counter <= 16'd2;
        register_6 <= 16'd583;
      end

      16'd583:
      begin
        register_93 <= register_7;
        register_72 <= register_91;
        program_counter <= 16'd450;
        register_70 <= 16'd584;
      end

      16'd584:
      begin
        register_93 <= register_71;
      end

      16'd585:
      begin
        register_93 <= 16'd5;
      end

      16'd586:
      begin
        s_output_leds <= register_93;
        program_counter <= 586;
        s_output_leds_stb <= 1'b1;
        if (s_output_leds_stb == 1'b1 && output_leds_ack == 1'b1) begin
          s_output_leds_stb <= 1'b0;
          program_counter <= 587;
        end
      end

      16'd587:
      begin
        register_93 <= 16'd5;
      end

      16'd588:
      begin
        s_output_checksum <= register_93;
        program_counter <= 588;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 589;
        end
      end

      16'd589:
      begin
        register_93 <= input_rs232_rx;
        program_counter <= 589;
        s_input_rs232_rx_ack <= 1'b1;
       if (s_input_rs232_rx_ack == 1'b1 && input_rs232_rx_stb == 1'b1) begin
          s_input_rs232_rx_ack <= 1'b0;
          program_counter <= 16'd590;
        end
      end

      16'd590:
      begin
        register_93 <= input_checksum;
        program_counter <= 590;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd591;
        end
      end

      16'd591:
      begin
        register_89 <= 16'd0;
        program_counter <= register_88;
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
