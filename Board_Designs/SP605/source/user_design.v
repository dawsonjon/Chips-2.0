//name : user_design
//tag : c components
//input : input_checksum:16
//input : input_eth_rx:16
//input : input_rs232_rx:16
//output : output_rs232_tx:16
//output : output_leds:16
//output : output_eth_tx:16
//output : output_checksum:16
//source_file : user_design.c
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
  reg       [8:0] program_counter;
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
  reg [15:0] memory [1674:0];

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
    memory[16'd569] = 16'd112;
    memory[16'd570] = 16'd117;
    memory[16'd571] = 16'd116;
    memory[16'd572] = 16'd95;
    memory[16'd573] = 16'd105;
    memory[16'd574] = 16'd112;
    memory[16'd575] = 16'd10;
    memory[16'd576] = 16'd0;
    memory[16'd577] = 16'd103;
    memory[16'd578] = 16'd101;
    memory[16'd579] = 16'd116;
    memory[16'd580] = 16'd95;
    memory[16'd581] = 16'd105;
    memory[16'd582] = 16'd112;
    memory[16'd583] = 16'd10;
    memory[16'd584] = 16'd0;
    memory[16'd585] = 16'd105;
    memory[16'd586] = 16'd112;
    memory[16'd587] = 16'd10;
    memory[16'd588] = 16'd0;
    memory[16'd589] = 16'd105;
    memory[16'd590] = 16'd112;
    memory[16'd591] = 16'd32;
    memory[16'd592] = 16'd97;
    memory[16'd593] = 16'd100;
    memory[16'd594] = 16'd100;
    memory[16'd595] = 16'd114;
    memory[16'd596] = 16'd101;
    memory[16'd597] = 16'd115;
    memory[16'd598] = 16'd115;
    memory[16'd599] = 16'd32;
    memory[16'd600] = 16'd103;
    memory[16'd601] = 16'd111;
    memory[16'd602] = 16'd111;
    memory[16'd603] = 16'd100;
    memory[16'd604] = 16'd10;
    memory[16'd605] = 16'd0;
    memory[16'd606] = 16'd105;
    memory[16'd607] = 16'd99;
    memory[16'd608] = 16'd109;
    memory[16'd609] = 16'd112;
    memory[16'd610] = 16'd10;
    memory[16'd611] = 16'd0;
    memory[16'd612] = 16'd112;
    memory[16'd613] = 16'd105;
    memory[16'd614] = 16'd110;
    memory[16'd615] = 16'd103;
    memory[16'd616] = 16'd95;
    memory[16'd617] = 16'd114;
    memory[16'd618] = 16'd101;
    memory[16'd619] = 16'd113;
    memory[16'd620] = 16'd117;
    memory[16'd621] = 16'd101;
    memory[16'd622] = 16'd115;
    memory[16'd623] = 16'd116;
    memory[16'd624] = 16'd10;
    memory[16'd625] = 16'd0;
    memory[16'd626] = 16'd111;
    memory[16'd627] = 16'd116;
    memory[16'd628] = 16'd104;
    memory[16'd629] = 16'd101;
    memory[16'd630] = 16'd114;
    memory[16'd631] = 16'd0;
    memory[16'd1656] = 16'd10;
    memory[16'd1657] = 16'd69;
    memory[16'd1658] = 16'd116;
    memory[16'd1659] = 16'd104;
    memory[16'd1660] = 16'd101;
    memory[16'd1661] = 16'd114;
    memory[16'd1662] = 16'd110;
    memory[16'd1663] = 16'd101;
    memory[16'd1664] = 16'd116;
    memory[16'd1665] = 16'd32;
    memory[16'd1666] = 16'd77;
    memory[16'd1667] = 16'd111;
    memory[16'd1668] = 16'd110;
    memory[16'd1669] = 16'd105;
    memory[16'd1670] = 16'd116;
    memory[16'd1671] = 16'd111;
    memory[16'd1672] = 16'd114;
    memory[16'd1673] = 16'd10;
    memory[16'd1674] = 16'd0;
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
        program_counter <= 16'd417;
        register_67 <= 16'd1;
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
        register_72 <= register_9;
      end

      16'd4:
      begin
        register_72 <= $signed(register_72) + $signed(register_8);
      end

      16'd5:
      begin
        address <= register_72;
      end

      16'd6:
      begin
        register_72 <= data_out;
      end

      16'd7:
      begin
        register_72 <= data_out;
      end

      16'd8:
      begin
        register_72 <= $signed(register_72) != $signed(16'd0);
      end

      16'd9:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 19;
      end

      16'd10:
      begin
        register_72 <= register_9;
      end

      16'd11:
      begin
        register_72 <= $signed(register_72) + $signed(register_8);
      end

      16'd12:
      begin
        address <= register_72;
      end

      16'd13:
      begin
        register_72 <= data_out;
      end

      16'd14:
      begin
        register_72 <= data_out;
      end

      16'd15:
      begin
        s_output_rs232_tx <= register_72;
        program_counter <= 15;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        register_72 <= register_9;
      end

      16'd17:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd18:
      begin
        register_9 <= register_72;
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
        register_72 <= register_12;
      end

      16'd23:
      begin
        register_72 <= $signed(register_72) > $signed(16'd9);
      end

      16'd24:
      begin
        if (register_72 == 16'h0000)
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
        register_72 <= register_11;
      end

      16'd34:
      begin
        s_output_rs232_tx <= register_72;
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
        register_72 <= register_11;
      end

      16'd39:
      begin
        s_output_rs232_tx <= register_72;
        program_counter <= 39;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 40;
        end
      end

      16'd40:
      begin
        register_72 <= 16'd32;
      end

      16'd41:
      begin
        s_output_rs232_tx <= register_72;
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
        register_72 <= register_11;
      end

      16'd46:
      begin
        s_output_rs232_tx <= register_72;
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
        register_72 <= register_11;
      end

      16'd50:
      begin
        s_output_rs232_tx <= register_72;
        program_counter <= 50;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 51;
        end
      end

      16'd51:
      begin
        register_72 <= 16'd32;
      end

      16'd52:
      begin
        s_output_rs232_tx <= register_72;
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
        register_72 <= register_7;
        register_73 <= 16'd0;
      end

      16'd57:
      begin
        register_72 <= register_20;
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd58:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_21;
        register_73 <= 16'd1;
      end

      16'd59:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd60:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_22;
        register_73 <= 16'd2;
      end

      16'd61:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd62:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_0;
        register_73 <= 16'd3;
      end

      16'd63:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd64:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_1;
        register_73 <= 16'd4;
      end

      16'd65:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd66:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_2;
        register_73 <= 16'd5;
      end

      16'd67:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd68:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_23;
        register_73 <= 16'd6;
      end

      16'd69:
      begin
        register_73 <= $signed(register_73) + $signed(register_18);
      end

      16'd70:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_19;
      end

      16'd71:
      begin
        s_output_eth_tx <= register_72;
        program_counter <= 71;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 72;
        end
      end

      16'd72:
      begin
        register_72 <= 16'd0;
      end

      16'd73:
      begin
        register_25 <= register_72;
        register_72 <= 16'd0;
      end

      16'd74:
      begin
        register_24 <= register_72;
      end

      16'd75:
      begin
        register_72 <= register_24;
        register_73 <= register_19;
      end

      16'd76:
      begin
        register_72 <= $signed(register_72) < $signed(register_73);
      end

      16'd77:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 90;
      end

      16'd78:
      begin
        register_72 <= register_25;
      end

      16'd79:
      begin
        register_72 <= $signed(register_72) + $signed(register_18);
      end

      16'd80:
      begin
        address <= register_72;
      end

      16'd81:
      begin
        register_72 <= data_out;
      end

      16'd82:
      begin
        register_72 <= data_out;
      end

      16'd83:
      begin
        s_output_eth_tx <= register_72;
        program_counter <= 83;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 84;
        end
      end

      16'd84:
      begin
        register_72 <= register_25;
      end

      16'd85:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd86:
      begin
        register_25 <= register_72;
      end

      16'd87:
      begin
        register_72 <= register_24;
      end

      16'd88:
      begin
        register_72 <= $signed(register_72) + $signed(16'd2);
      end

      16'd89:
      begin
        register_24 <= register_72;
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
        register_72 <= register_7;
        register_31 <= 16'd0;
        register_32 <= 16'd0;
        register_33 <= 16'd0;
      end

      16'd94:
      begin
        register_72 <= input_eth_rx;
        program_counter <= 94;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd95;
        end
      end

      16'd95:
      begin
        register_31 <= register_72;
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
        register_72 <= register_7;
        register_15 <= register_31;
        program_counter <= 16'd30;
        register_13 <= 16'd98;
      end

      16'd98:
      begin
        register_72 <= register_14;
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
        register_72 <= register_7;
      end

      16'd101:
      begin
        register_72 <= 16'd0;
      end

      16'd102:
      begin
        register_32 <= register_72;
        register_72 <= 16'd0;
      end

      16'd103:
      begin
        register_33 <= register_72;
      end

      16'd104:
      begin
        register_72 <= register_33;
        register_73 <= register_31;
      end

      16'd105:
      begin
        register_72 <= $signed(register_72) < $signed(register_73);
      end

      16'd106:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 116;
      end

      16'd107:
      begin
        register_72 <= input_eth_rx;
        program_counter <= 107;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd108;
        end
      end

      16'd108:
      begin
        register_73 <= register_32;
      end

      16'd109:
      begin
        register_73 <= $signed(register_73) + $signed(register_29);
      end

      16'd110:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_32;
      end

      16'd111:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd112:
      begin
        register_32 <= register_72;
      end

      16'd113:
      begin
        register_72 <= register_33;
      end

      16'd114:
      begin
        register_72 <= $signed(register_72) + $signed(16'd2);
      end

      16'd115:
      begin
        register_33 <= register_72;
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
        register_72 <= register_7;
        register_73 <= register_0;
      end

      16'd119:
      begin
        register_72 <= 16'd0;
      end

      16'd120:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd121:
      begin
        address <= register_72;
      end

      16'd122:
      begin
        register_72 <= data_out;
      end

      16'd123:
      begin
        register_72 <= data_out;
      end

      16'd124:
      begin
        register_72 <= $signed(register_72) != $signed(register_73);
      end

      16'd125:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 132;
      end

      16'd126:
      begin
        register_72 <= 16'd0;
      end

      16'd127:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd128:
      begin
        address <= register_72;
      end

      16'd129:
      begin
        register_72 <= data_out;
      end

      16'd130:
      begin
        register_72 <= data_out;
      end

      16'd131:
      begin
        register_72 <= $signed(register_72) != $signed(16'd65535);
      end

      16'd132:
      begin
        if (register_72 == 16'h0000)
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
        register_72 <= 16'd1;
        register_73 <= register_1;
      end

      16'd136:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd137:
      begin
        address <= register_72;
      end

      16'd138:
      begin
        register_72 <= data_out;
      end

      16'd139:
      begin
        register_72 <= data_out;
      end

      16'd140:
      begin
        register_72 <= $signed(register_72) != $signed(register_73);
      end

      16'd141:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 148;
      end

      16'd142:
      begin
        register_72 <= 16'd1;
      end

      16'd143:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd144:
      begin
        address <= register_72;
      end

      16'd145:
      begin
        register_72 <= data_out;
      end

      16'd146:
      begin
        register_72 <= data_out;
      end

      16'd147:
      begin
        register_72 <= $signed(register_72) != $signed(16'd65535);
      end

      16'd148:
      begin
        if (register_72 == 16'h0000)
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
        register_72 <= 16'd2;
        register_73 <= register_2;
      end

      16'd152:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd153:
      begin
        address <= register_72;
      end

      16'd154:
      begin
        register_72 <= data_out;
      end

      16'd155:
      begin
        register_72 <= data_out;
      end

      16'd156:
      begin
        register_72 <= $signed(register_72) != $signed(register_73);
      end

      16'd157:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 164;
      end

      16'd158:
      begin
        register_72 <= 16'd2;
      end

      16'd159:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd160:
      begin
        address <= register_72;
      end

      16'd161:
      begin
        register_72 <= data_out;
      end

      16'd162:
      begin
        register_72 <= data_out;
      end

      16'd163:
      begin
        register_72 <= $signed(register_72) != $signed(16'd65535);
      end

      16'd164:
      begin
        if (register_72 == 16'h0000)
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
        register_72 <= register_7;
      end

      16'd170:
      begin
        register_72 <= 16'd6;
      end

      16'd171:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
      end

      16'd172:
      begin
        address <= register_72;
      end

      16'd173:
      begin
        register_72 <= data_out;
      end

      16'd174:
      begin
        register_72 <= data_out;
      end

      16'd175:
      begin
        register_72 <= $signed(register_72) == $signed(16'd2054);
      end

      16'd176:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 233;
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
        register_72 <= register_7;
        register_73 <= 16'd7;
        register_18 <= register_5;
        register_19 <= 16'd64;
        register_20 <= 16'd11;
        register_21 <= 16'd12;
        register_22 <= 16'd13;
        register_23 <= 16'd2054;
      end

      16'd180:
      begin
        register_72 <= 16'd1;
        register_73 <= $signed(register_73) + $signed(register_5);
        register_20 <= $signed(register_20) + $signed(register_29);
        register_21 <= $signed(register_21) + $signed(register_29);
        register_22 <= $signed(register_22) + $signed(register_29);
      end

      16'd181:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd2048;
        register_73 <= 16'd8;
      end

      16'd182:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd183:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd1540;
        register_73 <= 16'd9;
      end

      16'd184:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd185:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd2;
        register_73 <= 16'd10;
      end

      16'd186:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd187:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_0;
        register_73 <= 16'd11;
      end

      16'd188:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd189:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_1;
        register_73 <= 16'd12;
      end

      16'd190:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd191:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_2;
        register_73 <= 16'd13;
      end

      16'd192:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd193:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_3;
        register_73 <= 16'd14;
      end

      16'd194:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd195:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_4;
        register_73 <= 16'd15;
      end

      16'd196:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd197:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd11;
        register_73 <= 16'd16;
      end

      16'd198:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd199:
      begin
        address <= register_72;
      end

      16'd200:
      begin
        register_72 <= data_out;
      end

      16'd201:
      begin
        register_72 <= data_out;
      end

      16'd202:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd12;
        register_73 <= 16'd17;
      end

      16'd203:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd204:
      begin
        address <= register_72;
      end

      16'd205:
      begin
        register_72 <= data_out;
      end

      16'd206:
      begin
        register_72 <= data_out;
      end

      16'd207:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd13;
        register_73 <= 16'd18;
      end

      16'd208:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd209:
      begin
        address <= register_72;
      end

      16'd210:
      begin
        register_72 <= data_out;
      end

      16'd211:
      begin
        register_72 <= data_out;
      end

      16'd212:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd14;
        register_73 <= 16'd19;
      end

      16'd213:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd214:
      begin
        address <= register_72;
      end

      16'd215:
      begin
        register_72 <= data_out;
      end

      16'd216:
      begin
        register_72 <= data_out;
      end

      16'd217:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd15;
        register_73 <= 16'd20;
      end

      16'd218:
      begin
        register_72 <= $signed(register_72) + $signed(register_29);
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd219:
      begin
        address <= register_72;
      end

      16'd220:
      begin
        register_72 <= data_out;
      end

      16'd221:
      begin
        register_72 <= data_out;
      end

      16'd222:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
      end

      16'd223:
      begin
        address <= register_20;
      end

      16'd224:
      begin
        register_20 <= data_out;
      end

      16'd225:
      begin
        register_20 <= data_out;
      end

      16'd226:
      begin
        address <= register_21;
      end

      16'd227:
      begin
        register_21 <= data_out;
      end

      16'd228:
      begin
        register_21 <= data_out;
      end

      16'd229:
      begin
        address <= register_22;
      end

      16'd230:
      begin
        register_22 <= data_out;
      end

      16'd231:
      begin
        register_22 <= data_out;
        program_counter <= 16'd54;
        register_16 <= 16'd232;
      end

      16'd232:
      begin
        register_72 <= register_17;
        program_counter <= 16'd233;
      end

      16'd233:
      begin
        program_counter <= 16'd235;
      end

      16'd234:
      begin
        program_counter <= 16'd94;
      end

      16'd235:
      begin
        register_28 <= register_31;
        program_counter <= register_27;
      end

      16'd236:
      begin
        register_46 <= 16'd569;
      end

      16'd237:
      begin
        register_8 <= register_46;
        program_counter <= 16'd2;
        register_6 <= 16'd238;
      end

      16'd238:
      begin
        register_72 <= register_7;
        register_47 <= 16'd0;
        register_48 <= 16'd0;
        register_73 <= 16'd7;
      end

      16'd239:
      begin
        register_72 <= 16'd17664;
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd240:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_42;
        register_73 <= 16'd8;
      end

      16'd241:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd242:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd0;
        register_73 <= 16'd9;
      end

      16'd243:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd244:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd16384;
        register_73 <= 16'd10;
      end

      16'd245:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd246:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_43;
        register_73 <= 16'd11;
      end

      16'd247:
      begin
        register_72 <= $signed(16'd65280) | $signed(register_72);
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd248:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= 16'd0;
        register_73 <= 16'd12;
      end

      16'd249:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd250:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_3;
        register_73 <= 16'd13;
      end

      16'd251:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd252:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_4;
        register_73 <= 16'd14;
      end

      16'd253:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd254:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_44;
        register_73 <= 16'd15;
      end

      16'd255:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd256:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_45;
        register_73 <= 16'd16;
      end

      16'd257:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd258:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_42;
      end

      16'd259:
      begin
        register_72 <= $signed(register_72) + $signed(16'd14);
      end

      16'd260:
      begin
        register_47 <= register_72;
        register_72 <= 16'd10;
      end

      16'd261:
      begin
        s_output_checksum <= register_72;
        program_counter <= 261;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 262;
        end
      end

      16'd262:
      begin
        register_72 <= 16'd7;
      end

      16'd263:
      begin
        register_48 <= register_72;
      end

      16'd264:
      begin
        register_72 <= register_48;
      end

      16'd265:
      begin
        register_72 <= $signed(register_72) <= $signed(16'd16);
      end

      16'd266:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 276;
      end

      16'd267:
      begin
        register_72 <= register_48;
      end

      16'd268:
      begin
        register_72 <= $signed(register_72) + $signed(register_41);
      end

      16'd269:
      begin
        address <= register_72;
      end

      16'd270:
      begin
        register_72 <= data_out;
      end

      16'd271:
      begin
        register_72 <= data_out;
      end

      16'd272:
      begin
        s_output_checksum <= register_72;
        program_counter <= 272;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 273;
        end
      end

      16'd273:
      begin
        register_72 <= register_48;
      end

      16'd274:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd275:
      begin
        register_48 <= register_72;
        program_counter <= 16'd264;
      end

      16'd276:
      begin
        register_72 <= input_checksum;
        program_counter <= 276;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd277;
        end
      end

      16'd277:
      begin
        register_73 <= 16'd12;
      end

      16'd278:
      begin
        register_73 <= $signed(register_73) + $signed(register_41);
      end

      16'd279:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_47;
      end

      16'd280:
      begin
        register_72 <= $signed(register_72) < $signed(16'd64);
      end

      16'd281:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 284;
      end

      16'd282:
      begin
        register_72 <= 16'd64;
      end

      16'd283:
      begin
        register_47 <= register_72;
        program_counter <= 16'd284;
      end

      16'd284:
      begin
        register_18 <= register_41;
        register_19 <= register_47;
        register_20 <= 16'd27888;
        register_21 <= 16'd18847;
        register_22 <= 16'd24971;
        register_23 <= 16'd2048;
        program_counter <= 16'd54;
        register_16 <= 16'd285;
      end

      16'd285:
      begin
        register_72 <= register_17;
        register_40 <= 16'd0;
        program_counter <= register_39;
      end

      16'd286:
      begin
        register_52 <= 16'd0;
        register_53 <= 16'd0;
        register_54 <= 16'd0;
        register_55 <= 16'd0;
        register_56 <= 16'd0;
        register_57 <= 16'd0;
        register_58 <= 16'd0;
        register_59 <= 16'd0;
        register_60 <= 16'd0;
        register_61 <= 16'd577;
      end

      16'd287:
      begin
        register_8 <= register_61;
        program_counter <= 16'd2;
        register_6 <= 16'd288;
      end

      16'd288:
      begin
        register_72 <= register_7;
      end

      16'd289:
      begin
        register_29 <= register_51;
        program_counter <= 16'd91;
        register_27 <= 16'd290;
      end

      16'd290:
      begin
        register_72 <= register_28;
      end

      16'd291:
      begin
        register_47 <= register_72;
        register_72 <= 16'd6;
      end

      16'd292:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd293:
      begin
        address <= register_72;
      end

      16'd294:
      begin
        register_72 <= data_out;
      end

      16'd295:
      begin
        register_72 <= data_out;
      end

      16'd296:
      begin
        register_72 <= $signed(register_72) == $signed(16'd2048);
      end

      16'd297:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 412;
      end

      16'd298:
      begin
        register_62 <= 16'd585;
      end

      16'd299:
      begin
        register_8 <= register_62;
        program_counter <= 16'd2;
        register_6 <= 16'd300;
      end

      16'd300:
      begin
        register_72 <= register_7;
        register_73 <= register_3;
      end

      16'd301:
      begin
        register_72 <= 16'd15;
      end

      16'd302:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd303:
      begin
        address <= register_72;
      end

      16'd304:
      begin
        register_72 <= data_out;
      end

      16'd305:
      begin
        register_72 <= data_out;
      end

      16'd306:
      begin
        register_72 <= $signed(register_72) != $signed(register_73);
      end

      16'd307:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 310;
      end

      16'd308:
      begin
        program_counter <= 16'd289;
      end

      16'd309:
      begin
        program_counter <= 16'd310;
      end

      16'd310:
      begin
        register_72 <= 16'd16;
        register_73 <= register_4;
      end

      16'd311:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd312:
      begin
        address <= register_72;
      end

      16'd313:
      begin
        register_72 <= data_out;
      end

      16'd314:
      begin
        register_72 <= data_out;
      end

      16'd315:
      begin
        register_72 <= $signed(register_72) != $signed(register_73);
      end

      16'd316:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 319;
      end

      16'd317:
      begin
        program_counter <= 16'd289;
      end

      16'd318:
      begin
        program_counter <= 16'd319;
      end

      16'd319:
      begin
        register_63 <= 16'd589;
      end

      16'd320:
      begin
        register_8 <= register_63;
        program_counter <= 16'd2;
        register_6 <= 16'd321;
      end

      16'd321:
      begin
        register_72 <= register_7;
      end

      16'd322:
      begin
        register_72 <= 16'd11;
      end

      16'd323:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd324:
      begin
        address <= register_72;
      end

      16'd325:
      begin
        register_72 <= data_out;
      end

      16'd326:
      begin
        register_72 <= data_out;
      end

      16'd327:
      begin
        register_72 <= $signed(register_72) & $signed(16'd255);
      end

      16'd328:
      begin
        register_72 <= $signed(register_72) == $signed(16'd1);
      end

      16'd329:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 411;
      end

      16'd330:
      begin
        register_72 <= 16'd7;
        register_64 <= 16'd606;
      end

      16'd331:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
        register_8 <= register_64;
      end

      16'd332:
      begin
        address <= register_72;
      end

      16'd333:
      begin
        register_72 <= data_out;
      end

      16'd334:
      begin
        register_72 <= data_out;
      end

      16'd335:
      begin
        register_72 <= $signed(register_72) >>> $signed(16'd8);
      end

      16'd336:
      begin
        register_72 <= $signed(register_72) & $signed(16'd15);
      end

      16'd337:
      begin
        register_72 <= $signed(register_72) << $signed(16'd1);
      end

      16'd338:
      begin
        register_54 <= register_72;
      end

      16'd339:
      begin
        register_72 <= register_54;
        register_73 <= register_54;
      end

      16'd340:
      begin
        register_72 <= $signed(register_72) + $signed(16'd7);
      end

      16'd341:
      begin
        register_55 <= register_72;
        register_72 <= 16'd8;
      end

      16'd342:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd343:
      begin
        address <= register_72;
      end

      16'd344:
      begin
        register_72 <= data_out;
      end

      16'd345:
      begin
        register_72 <= data_out;
      end

      16'd346:
      begin
        register_53 <= register_72;
      end

      16'd347:
      begin
        register_72 <= register_53;
      end

      16'd348:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd349:
      begin
        register_72 <= $signed(register_72) >>> $signed(16'd1);
      end

      16'd350:
      begin
        register_72 <= $signed(register_72) - $signed(register_73);
      end

      16'd351:
      begin
        register_56 <= register_72;
        register_72 <= register_55;
      end

      16'd352:
      begin
        register_73 <= register_56;
      end

      16'd353:
      begin
        register_72 <= $signed(register_72) + $signed(register_73);
      end

      16'd354:
      begin
        register_72 <= $signed(register_72) - $signed(16'd1);
      end

      16'd355:
      begin
        register_60 <= register_72;
        program_counter <= 16'd2;
        register_6 <= 16'd356;
      end

      16'd356:
      begin
        register_72 <= register_7;
      end

      16'd357:
      begin
        register_72 <= register_55;
      end

      16'd358:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd359:
      begin
        address <= register_72;
      end

      16'd360:
      begin
        register_72 <= data_out;
      end

      16'd361:
      begin
        register_72 <= data_out;
      end

      16'd362:
      begin
        register_72 <= $signed(register_72) == $signed(16'd2048);
      end

      16'd363:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 410;
      end

      16'd364:
      begin
        register_65 <= 16'd612;
      end

      16'd365:
      begin
        register_8 <= register_65;
        program_counter <= 16'd2;
        register_6 <= 16'd366;
      end

      16'd366:
      begin
        register_72 <= register_7;
      end

      16'd367:
      begin
        register_72 <= 16'd19;
      end

      16'd368:
      begin
        register_59 <= register_72;
        register_72 <= register_56;
      end

      16'd369:
      begin
        s_output_checksum <= register_72;
        program_counter <= 369;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 370;
        end
      end

      16'd370:
      begin
        register_72 <= 16'd0;
      end

      16'd371:
      begin
        s_output_checksum <= register_72;
        program_counter <= 371;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 372;
        end
      end

      16'd372:
      begin
        register_72 <= 16'd0;
      end

      16'd373:
      begin
        s_output_checksum <= register_72;
        program_counter <= 373;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 374;
        end
      end

      16'd374:
      begin
        register_72 <= register_55;
      end

      16'd375:
      begin
        register_72 <= $signed(register_72) + $signed(16'd2);
      end

      16'd376:
      begin
        register_58 <= register_72;
      end

      16'd377:
      begin
        register_72 <= register_58;
        register_73 <= register_60;
      end

      16'd378:
      begin
        register_72 <= $signed(register_72) <= $signed(register_73);
      end

      16'd379:
      begin
        if (register_72 == 16'h0000)
          program_counter <= 396;
      end

      16'd380:
      begin
        register_72 <= register_58;
      end

      16'd381:
      begin
        register_72 <= $signed(register_72) + $signed(register_51);
      end

      16'd382:
      begin
        address <= register_72;
      end

      16'd383:
      begin
        register_72 <= data_out;
      end

      16'd384:
      begin
        register_72 <= data_out;
      end

      16'd385:
      begin
        register_57 <= register_72;
      end

      16'd386:
      begin
        register_72 <= register_57;
      end

      16'd387:
      begin
        s_output_checksum <= register_72;
        program_counter <= 387;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 388;
        end
      end

      16'd388:
      begin
        register_72 <= register_57;
        register_73 <= register_59;
      end

      16'd389:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd390:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
        register_72 <= register_59;
      end

      16'd391:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd392:
      begin
        register_59 <= register_72;
      end

      16'd393:
      begin
        register_72 <= register_58;
      end

      16'd394:
      begin
        register_72 <= $signed(register_72) + $signed(16'd1);
      end

      16'd395:
      begin
        register_58 <= register_72;
        program_counter <= 16'd377;
      end

      16'd396:
      begin
        register_72 <= 16'd0;
        register_73 <= 16'd17;
      end

      16'd397:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
      end

      16'd398:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
      end

      16'd399:
      begin
        register_72 <= input_checksum;
        program_counter <= 399;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd400;
        end
      end

      16'd400:
      begin
        register_73 <= 16'd18;
        register_41 <= register_5;
        register_42 <= register_53;
        register_43 <= 16'd1;
        register_44 <= 16'd13;
        register_45 <= 16'd14;
      end

      16'd401:
      begin
        register_73 <= $signed(register_73) + $signed(register_5);
        register_44 <= $signed(register_44) + $signed(register_51);
        register_45 <= $signed(register_45) + $signed(register_51);
      end

      16'd402:
      begin
        address <= register_73;
        data_in <= register_72;
        write_enable <= 1'b1;
      end

      16'd403:
      begin
        address <= register_44;
      end

      16'd404:
      begin
        register_44 <= data_out;
      end

      16'd405:
      begin
        register_44 <= data_out;
      end

      16'd406:
      begin
        address <= register_45;
      end

      16'd407:
      begin
        register_45 <= data_out;
      end

      16'd408:
      begin
        register_45 <= data_out;
        program_counter <= 16'd236;
        register_39 <= 16'd409;
      end

      16'd409:
      begin
        register_72 <= register_40;
        program_counter <= 16'd410;
      end

      16'd410:
      begin
        program_counter <= 16'd411;
      end

      16'd411:
      begin
        program_counter <= 16'd415;
      end

      16'd412:
      begin
        register_66 <= 16'd626;
      end

      16'd413:
      begin
        register_8 <= register_66;
        program_counter <= 16'd2;
        register_6 <= 16'd414;
      end

      16'd414:
      begin
        register_72 <= register_7;
      end

      16'd415:
      begin
        program_counter <= 16'd289;
      end

      16'd416:
      begin
        register_50 <= register_47;
        program_counter <= register_49;
      end

      16'd417:
      begin
        register_69 <= 16'd0;
        register_70 <= 16'd632;
        register_71 <= 16'd1656;
      end

      16'd418:
      begin
        register_8 <= register_71;
        program_counter <= 16'd2;
        register_6 <= 16'd419;
      end

      16'd419:
      begin
        register_72 <= register_7;
        register_51 <= register_70;
        program_counter <= 16'd286;
        register_49 <= 16'd420;
      end

      16'd420:
      begin
        register_72 <= register_50;
      end

      16'd421:
      begin
        register_72 <= 16'd5;
      end

      16'd422:
      begin
        s_output_leds <= register_72;
        program_counter <= 422;
        s_output_leds_stb <= 1'b1;
        if (s_output_leds_stb == 1'b1 && output_leds_ack == 1'b1) begin
          s_output_leds_stb <= 1'b0;
          program_counter <= 423;
        end
      end

      16'd423:
      begin
        register_72 <= 16'd5;
      end

      16'd424:
      begin
        s_output_checksum <= register_72;
        program_counter <= 424;
        s_output_checksum_stb <= 1'b1;
        if (s_output_checksum_stb == 1'b1 && output_checksum_ack == 1'b1) begin
          s_output_checksum_stb <= 1'b0;
          program_counter <= 425;
        end
      end

      16'd425:
      begin
        register_72 <= input_rs232_rx;
        program_counter <= 425;
        s_input_rs232_rx_ack <= 1'b1;
       if (s_input_rs232_rx_ack == 1'b1 && input_rs232_rx_stb == 1'b1) begin
          s_input_rs232_rx_ack <= 1'b0;
          program_counter <= 16'd426;
        end
      end

      16'd426:
      begin
        register_72 <= input_checksum;
        program_counter <= 426;
        s_input_checksum_ack <= 1'b1;
       if (s_input_checksum_ack == 1'b1 && input_checksum_stb == 1'b1) begin
          s_input_checksum_ack <= 1'b0;
          program_counter <= 16'd427;
        end
      end

      16'd427:
      begin
        register_68 <= 16'd0;
        program_counter <= register_67;
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
