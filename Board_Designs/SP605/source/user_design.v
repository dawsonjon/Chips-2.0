//name : user_design
//tag : c components
//input : input_eth_rx:16
//input : input_rs232_rx:16
//output : output_rs232_tx:16
//output : output_leds:16
//output : output_eth_tx:16
//source_file : user_design.c
///User_Design
///===========
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module user_design(input_eth_rx,input_rs232_rx,input_eth_rx_stb,input_rs232_rx_stb,output_rs232_tx_ack,output_leds_ack,output_eth_tx_ack,clk,rst,output_rs232_tx,output_leds,output_eth_tx,output_rs232_tx_stb,output_leds_stb,output_eth_tx_stb,input_eth_rx_ack,input_rs232_rx_ack);
  input     [15:0] input_eth_rx;
  input     [15:0] input_rs232_rx;
  input     input_eth_rx_stb;
  input     input_rs232_rx_stb;
  input     output_rs232_tx_ack;
  input     output_leds_ack;
  input     output_eth_tx_ack;
  input     clk;
  input     rst;
  output    [15:0] output_rs232_tx;
  output    [15:0] output_leds;
  output    [15:0] output_eth_tx;
  output    output_rs232_tx_stb;
  output    output_leds_stb;
  output    output_eth_tx_stb;
  output    input_eth_rx_ack;
  output    input_rs232_rx_ack;
  reg       [15:0] timer;
  reg       [215:0] program_counter;
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
  reg       [15:0] s_output_rs232_tx_stb;
  reg       [15:0] s_output_leds_stb;
  reg       [15:0] s_output_eth_tx_stb;
  reg       [15:0] s_output_rs232_tx;
  reg       [15:0] s_output_leds;
  reg       [15:0] s_output_eth_tx;
  reg       [15:0] s_input_eth_rx_ack;
  reg       [15:0] s_input_rs232_rx_ack;
  reg [15:0] memory [1140:0];

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
    memory[16'd0] = 16'd103;
    memory[16'd1] = 16'd101;
    memory[16'd2] = 16'd116;
    memory[16'd3] = 16'd95;
    memory[16'd4] = 16'd101;
    memory[16'd5] = 16'd116;
    memory[16'd6] = 16'd104;
    memory[16'd7] = 16'd0;
    memory[16'd8] = 16'd112;
    memory[16'd9] = 16'd117;
    memory[16'd10] = 16'd116;
    memory[16'd11] = 16'd95;
    memory[16'd12] = 16'd101;
    memory[16'd13] = 16'd116;
    memory[16'd14] = 16'd104;
    memory[16'd15] = 16'd0;
    memory[16'd80] = 16'd103;
    memory[16'd81] = 16'd101;
    memory[16'd82] = 16'd116;
    memory[16'd83] = 16'd95;
    memory[16'd84] = 16'd105;
    memory[16'd85] = 16'd112;
    memory[16'd86] = 16'd0;
    memory[16'd87] = 16'd105;
    memory[16'd88] = 16'd112;
    memory[16'd89] = 16'd0;
    memory[16'd90] = 16'd97;
    memory[16'd91] = 16'd114;
    memory[16'd92] = 16'd112;
    memory[16'd93] = 16'd0;
    memory[16'd94] = 16'd111;
    memory[16'd95] = 16'd116;
    memory[16'd96] = 16'd104;
    memory[16'd97] = 16'd101;
    memory[16'd98] = 16'd114;
    memory[16'd99] = 16'd0;
    memory[16'd1124] = 16'd69;
    memory[16'd1125] = 16'd116;
    memory[16'd1126] = 16'd104;
    memory[16'd1127] = 16'd101;
    memory[16'd1128] = 16'd114;
    memory[16'd1129] = 16'd110;
    memory[16'd1130] = 16'd101;
    memory[16'd1131] = 16'd116;
    memory[16'd1132] = 16'd32;
    memory[16'd1133] = 16'd77;
    memory[16'd1134] = 16'd111;
    memory[16'd1135] = 16'd110;
    memory[16'd1136] = 16'd105;
    memory[16'd1137] = 16'd116;
    memory[16'd1138] = 16'd111;
    memory[16'd1139] = 16'd114;
    memory[16'd1140] = 16'd0;
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
        register_10 <= 16'd1;
        register_11 <= 16'd515;
        register_12 <= 16'd1029;
        register_31 <= 16'd49320;
        register_32 <= 16'd257;
        program_counter <= 16'd194;
        register_41 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_3 <= 16'd0;
      end

      16'd3:
      begin
        register_46 <= register_3;
      end

      16'd4:
      begin
        register_46 <= $signed(register_46) + $signed(register_2);
      end

      16'd5:
      begin
        address <= register_46;
      end

      16'd6:
      begin
        register_46 <= data_out;
      end

      16'd7:
      begin
        register_46 <= data_out;
      end

      16'd8:
      begin
        register_46 <= $signed(register_46) != $signed(16'd0);
      end

      16'd9:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 19;
      end

      16'd10:
      begin
        register_46 <= register_3;
      end

      16'd11:
      begin
        register_46 <= $signed(register_46) + $signed(register_2);
      end

      16'd12:
      begin
        address <= register_46;
      end

      16'd13:
      begin
        register_46 <= data_out;
      end

      16'd14:
      begin
        register_46 <= data_out;
      end

      16'd15:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 15;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        register_46 <= register_3;
      end

      16'd17:
      begin
        register_46 <= $signed(register_46) + $signed(16'd1);
      end

      16'd18:
      begin
        register_3 <= register_46;
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
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

      16'd22:
      begin
        register_46 <= register_6;
      end

      16'd23:
      begin
        register_46 <= $signed(register_46) > $signed(16'd9);
      end

      16'd24:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 28;
      end

      16'd25:
      begin
        register_5 <= register_6;
      end

      16'd26:
      begin
        register_5 <= $signed(register_5) + $signed(16'd87);
        program_counter <= register_4;
      end

      16'd27:
      begin
        program_counter <= 16'd28;
      end

      16'd28:
      begin
        register_5 <= register_6;
      end

      16'd29:
      begin
        register_5 <= $signed(register_5) + $signed(16'd48);
        program_counter <= register_4;
      end

      16'd30:
      begin
        register_6 <= register_9;
      end

      16'd31:
      begin
        register_6 <= $signed(register_6) >>> $signed(16'd12);
      end

      16'd32:
      begin
        register_6 <= $signed(register_6) & $signed(16'd15);
        program_counter <= 16'd22;
        register_4 <= 16'd33;
      end

      16'd33:
      begin
        register_46 <= register_5;
      end

      16'd34:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 34;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 35;
        end
      end

      16'd35:
      begin
        register_6 <= register_9;
      end

      16'd36:
      begin
        register_6 <= $signed(register_6) >>> $signed(16'd8);
      end

      16'd37:
      begin
        register_6 <= $signed(register_6) & $signed(16'd15);
        program_counter <= 16'd22;
        register_4 <= 16'd38;
      end

      16'd38:
      begin
        register_46 <= register_5;
      end

      16'd39:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 39;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 40;
        end
      end

      16'd40:
      begin
        register_46 <= 16'd32;
      end

      16'd41:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 41;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 42;
        end
      end

      16'd42:
      begin
        register_6 <= register_9;
      end

      16'd43:
      begin
        register_6 <= $signed(register_6) >>> $signed(16'd4);
      end

      16'd44:
      begin
        register_6 <= $signed(register_6) & $signed(16'd15);
        program_counter <= 16'd22;
        register_4 <= 16'd45;
      end

      16'd45:
      begin
        register_46 <= register_5;
      end

      16'd46:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 46;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 47;
        end
      end

      16'd47:
      begin
        register_6 <= register_9;
      end

      16'd48:
      begin
        register_6 <= $signed(register_6) & $signed(16'd15);
        program_counter <= 16'd22;
        register_4 <= 16'd49;
      end

      16'd49:
      begin
        register_46 <= register_5;
      end

      16'd50:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 50;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 51;
        end
      end

      16'd51:
      begin
        register_46 <= 16'd32;
      end

      16'd52:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 52;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 53;
        end
      end

      16'd53:
      begin
        register_8 <= 16'd0;
        program_counter <= register_7;
      end

      16'd54:
      begin
        register_16 <= 16'd0;
      end

      16'd55:
      begin
        register_2 <= register_16;
        program_counter <= 16'd2;
        register_0 <= 16'd56;
      end

      16'd56:
      begin
        register_46 <= register_1;
        register_17 <= 16'd0;
        register_18 <= 16'd0;
        register_19 <= 16'd0;
      end

      16'd57:
      begin
        register_46 <= input_eth_rx;
        program_counter <= 57;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd58;
        end
      end

      16'd58:
      begin
        register_17 <= register_46;
        register_46 <= 16'd0;
      end

      16'd59:
      begin
        register_18 <= register_46;
        register_46 <= 16'd0;
      end

      16'd60:
      begin
        register_19 <= register_46;
      end

      16'd61:
      begin
        register_46 <= register_19;
        register_47 <= register_17;
      end

      16'd62:
      begin
        register_46 <= $signed(register_46) < $signed(register_47);
      end

      16'd63:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 73;
      end

      16'd64:
      begin
        register_46 <= input_eth_rx;
        program_counter <= 64;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd65;
        end
      end

      16'd65:
      begin
        register_47 <= register_18;
      end

      16'd66:
      begin
        register_47 <= $signed(register_47) + $signed(register_15);
      end

      16'd67:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_18;
      end

      16'd68:
      begin
        register_46 <= $signed(register_46) + $signed(16'd1);
      end

      16'd69:
      begin
        register_18 <= register_46;
      end

      16'd70:
      begin
        register_46 <= register_19;
      end

      16'd71:
      begin
        register_46 <= $signed(register_46) + $signed(16'd2);
      end

      16'd72:
      begin
        register_19 <= register_46;
        program_counter <= 16'd61;
      end

      16'd73:
      begin
        register_14 <= register_17;
        program_counter <= register_13;
      end

      16'd74:
      begin
        register_28 <= 16'd0;
        register_29 <= 16'd0;
        register_30 <= 16'd8;
      end

      16'd75:
      begin
        register_2 <= register_30;
        program_counter <= 16'd2;
        register_0 <= 16'd76;
      end

      16'd76:
      begin
        register_46 <= register_1;
        register_47 <= 16'd0;
      end

      16'd77:
      begin
        register_46 <= register_24;
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd78:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_25;
        register_47 <= 16'd1;
      end

      16'd79:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd80:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_26;
        register_47 <= 16'd2;
      end

      16'd81:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd82:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_10;
        register_47 <= 16'd3;
      end

      16'd83:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd84:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_11;
        register_47 <= 16'd4;
      end

      16'd85:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd86:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_12;
        register_47 <= 16'd5;
      end

      16'd87:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd88:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_27;
        register_47 <= 16'd6;
      end

      16'd89:
      begin
        register_47 <= $signed(register_47) + $signed(register_22);
      end

      16'd90:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_23;
      end

      16'd91:
      begin
        s_output_eth_tx <= register_46;
        program_counter <= 91;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 92;
        end
      end

      16'd92:
      begin
        register_46 <= 16'd0;
      end

      16'd93:
      begin
        register_29 <= register_46;
        register_46 <= 16'd0;
      end

      16'd94:
      begin
        register_28 <= register_46;
      end

      16'd95:
      begin
        register_46 <= register_28;
        register_47 <= register_23;
      end

      16'd96:
      begin
        register_46 <= $signed(register_46) < $signed(register_47);
      end

      16'd97:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 110;
      end

      16'd98:
      begin
        register_46 <= register_29;
      end

      16'd99:
      begin
        register_46 <= $signed(register_46) + $signed(register_22);
      end

      16'd100:
      begin
        address <= register_46;
      end

      16'd101:
      begin
        register_46 <= data_out;
      end

      16'd102:
      begin
        register_46 <= data_out;
      end

      16'd103:
      begin
        s_output_eth_tx <= register_46;
        program_counter <= 103;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 104;
        end
      end

      16'd104:
      begin
        register_46 <= register_29;
      end

      16'd105:
      begin
        register_46 <= $signed(register_46) + $signed(16'd1);
      end

      16'd106:
      begin
        register_29 <= register_46;
      end

      16'd107:
      begin
        register_46 <= register_28;
      end

      16'd108:
      begin
        register_46 <= $signed(register_46) + $signed(16'd2);
      end

      16'd109:
      begin
        register_28 <= register_46;
        program_counter <= 16'd95;
      end

      16'd110:
      begin
        register_21 <= 16'd0;
        program_counter <= register_20;
      end

      16'd111:
      begin
        register_36 <= 16'd16;
        register_37 <= 16'd80;
      end

      16'd112:
      begin
        register_2 <= register_37;
        program_counter <= 16'd2;
        register_0 <= 16'd113;
      end

      16'd113:
      begin
        register_46 <= register_1;
      end

      16'd114:
      begin
        register_15 <= register_35;
        program_counter <= 16'd54;
        register_13 <= 16'd115;
      end

      16'd115:
      begin
        register_46 <= register_14;
      end

      16'd116:
      begin
        register_23 <= register_46;
        register_46 <= 16'd6;
      end

      16'd117:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
      end

      16'd118:
      begin
        address <= register_46;
      end

      16'd119:
      begin
        register_46 <= data_out;
      end

      16'd120:
      begin
        register_46 <= data_out;
      end

      16'd121:
      begin
        register_46 <= $signed(register_46) == $signed(16'd2048);
      end

      16'd122:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 126;
      end

      16'd123:
      begin
        register_38 <= 16'd87;
      end

      16'd124:
      begin
        register_2 <= register_38;
        program_counter <= 16'd2;
        register_0 <= 16'd125;
      end

      16'd125:
      begin
        register_46 <= register_1;
        program_counter <= 16'd192;
      end

      16'd126:
      begin
        register_46 <= 16'd6;
      end

      16'd127:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
      end

      16'd128:
      begin
        address <= register_46;
      end

      16'd129:
      begin
        register_46 <= data_out;
      end

      16'd130:
      begin
        register_46 <= data_out;
      end

      16'd131:
      begin
        register_46 <= $signed(register_46) == $signed(16'd2054);
      end

      16'd132:
      begin
        if (register_46 == 16'h0000)
          program_counter <= 189;
      end

      16'd133:
      begin
        register_39 <= 16'd90;
      end

      16'd134:
      begin
        register_2 <= register_39;
        program_counter <= 16'd2;
        register_0 <= 16'd135;
      end

      16'd135:
      begin
        register_46 <= register_1;
        register_47 <= 16'd7;
        register_22 <= register_36;
        register_23 <= 16'd64;
        register_24 <= 16'd11;
        register_25 <= 16'd12;
        register_26 <= 16'd13;
        register_27 <= 16'd2054;
      end

      16'd136:
      begin
        register_46 <= 16'd1;
        register_47 <= $signed(register_47) + $signed(register_36);
        register_24 <= $signed(register_24) + $signed(register_35);
        register_25 <= $signed(register_25) + $signed(register_35);
        register_26 <= $signed(register_26) + $signed(register_35);
      end

      16'd137:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd2048;
        register_47 <= 16'd8;
      end

      16'd138:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd139:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd1540;
        register_47 <= 16'd9;
      end

      16'd140:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd141:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd2;
        register_47 <= 16'd10;
      end

      16'd142:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd143:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_10;
        register_47 <= 16'd11;
      end

      16'd144:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd145:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_11;
        register_47 <= 16'd12;
      end

      16'd146:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd147:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_12;
        register_47 <= 16'd13;
      end

      16'd148:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd149:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_31;
        register_47 <= 16'd14;
      end

      16'd150:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd151:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= register_32;
        register_47 <= 16'd15;
      end

      16'd152:
      begin
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd153:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd11;
        register_47 <= 16'd16;
      end

      16'd154:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd155:
      begin
        address <= register_46;
      end

      16'd156:
      begin
        register_46 <= data_out;
      end

      16'd157:
      begin
        register_46 <= data_out;
      end

      16'd158:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd12;
        register_47 <= 16'd17;
      end

      16'd159:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd160:
      begin
        address <= register_46;
      end

      16'd161:
      begin
        register_46 <= data_out;
      end

      16'd162:
      begin
        register_46 <= data_out;
      end

      16'd163:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd13;
        register_47 <= 16'd18;
      end

      16'd164:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd165:
      begin
        address <= register_46;
      end

      16'd166:
      begin
        register_46 <= data_out;
      end

      16'd167:
      begin
        register_46 <= data_out;
      end

      16'd168:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd14;
        register_47 <= 16'd19;
      end

      16'd169:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd170:
      begin
        address <= register_46;
      end

      16'd171:
      begin
        register_46 <= data_out;
      end

      16'd172:
      begin
        register_46 <= data_out;
      end

      16'd173:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
        register_46 <= 16'd15;
        register_47 <= 16'd20;
      end

      16'd174:
      begin
        register_46 <= $signed(register_46) + $signed(register_35);
        register_47 <= $signed(register_47) + $signed(register_36);
      end

      16'd175:
      begin
        address <= register_46;
      end

      16'd176:
      begin
        register_46 <= data_out;
      end

      16'd177:
      begin
        register_46 <= data_out;
      end

      16'd178:
      begin
        address <= register_47;
        data_in <= register_46;
        write_enable <= 1'b1;
      end

      16'd179:
      begin
        address <= register_24;
      end

      16'd180:
      begin
        register_24 <= data_out;
      end

      16'd181:
      begin
        register_24 <= data_out;
      end

      16'd182:
      begin
        address <= register_25;
      end

      16'd183:
      begin
        register_25 <= data_out;
      end

      16'd184:
      begin
        register_25 <= data_out;
      end

      16'd185:
      begin
        address <= register_26;
      end

      16'd186:
      begin
        register_26 <= data_out;
      end

      16'd187:
      begin
        register_26 <= data_out;
        program_counter <= 16'd74;
        register_20 <= 16'd188;
      end

      16'd188:
      begin
        register_46 <= register_21;
        program_counter <= 16'd192;
      end

      16'd189:
      begin
        register_40 <= 16'd94;
      end

      16'd190:
      begin
        register_2 <= register_40;
        program_counter <= 16'd2;
        register_0 <= 16'd191;
      end

      16'd191:
      begin
        register_46 <= register_1;
      end

      16'd192:
      begin
        program_counter <= 16'd114;
      end

      16'd193:
      begin
        register_34 <= register_23;
        program_counter <= register_33;
      end

      16'd194:
      begin
        register_43 <= 16'd0;
        register_44 <= 16'd100;
        register_46 <= 16'd13;
      end

      16'd195:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 195;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 196;
        end
      end

      16'd196:
      begin
        register_46 <= 16'd10;
      end

      16'd197:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 197;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 198;
        end
      end

      16'd198:
      begin
        register_45 <= 16'd1124;
      end

      16'd199:
      begin
        register_2 <= register_45;
        program_counter <= 16'd2;
        register_0 <= 16'd200;
      end

      16'd200:
      begin
        register_46 <= register_1;
      end

      16'd201:
      begin
        register_46 <= 16'd13;
      end

      16'd202:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 202;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 203;
        end
      end

      16'd203:
      begin
        register_46 <= 16'd10;
      end

      16'd204:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 204;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 205;
        end
      end

      16'd205:
      begin
        register_35 <= register_44;
        program_counter <= 16'd111;
        register_33 <= 16'd206;
      end

      16'd206:
      begin
        register_46 <= register_34;
      end

      16'd207:
      begin
        register_46 <= 16'd5;
      end

      16'd208:
      begin
        s_output_leds <= register_46;
        program_counter <= 208;
        s_output_leds_stb <= 1'b1;
        if (s_output_leds_stb == 1'b1 && output_leds_ack == 1'b1) begin
          s_output_leds_stb <= 1'b0;
          program_counter <= 209;
        end
      end

      16'd209:
      begin
        register_46 <= 16'd0;
      end

      16'd210:
      begin
        s_output_eth_tx <= register_46;
        program_counter <= 210;
        s_output_eth_tx_stb <= 1'b1;
        if (s_output_eth_tx_stb == 1'b1 && output_eth_tx_ack == 1'b1) begin
          s_output_eth_tx_stb <= 1'b0;
          program_counter <= 211;
        end
      end

      16'd211:
      begin
        register_46 <= input_eth_rx;
        program_counter <= 211;
        s_input_eth_rx_ack <= 1'b1;
       if (s_input_eth_rx_ack == 1'b1 && input_eth_rx_stb == 1'b1) begin
          s_input_eth_rx_ack <= 1'b0;
          program_counter <= 16'd212;
        end
      end

      16'd212:
      begin
        register_46 <= 16'd1;
      end

      16'd213:
      begin
        s_output_rs232_tx <= register_46;
        program_counter <= 213;
        s_output_rs232_tx_stb <= 1'b1;
        if (s_output_rs232_tx_stb == 1'b1 && output_rs232_tx_ack == 1'b1) begin
          s_output_rs232_tx_stb <= 1'b0;
          program_counter <= 214;
        end
      end

      16'd214:
      begin
        register_46 <= input_rs232_rx;
        program_counter <= 214;
        s_input_rs232_rx_ack <= 1'b1;
       if (s_input_rs232_rx_ack == 1'b1 && input_rs232_rx_stb == 1'b1) begin
          s_input_rs232_rx_ack <= 1'b0;
          program_counter <= 16'd215;
        end
      end

      16'd215:
      begin
        register_42 <= 16'd0;
        program_counter <= register_41;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end
  assign input_eth_rx_ack = s_input_eth_rx_ack;
  assign input_rs232_rx_ack = s_input_rs232_rx_ack;
  assign output_rs232_tx_stb = s_output_rs232_tx_stb;
  assign output_rs232_tx = s_output_rs232_tx;
  assign output_leds_stb = s_output_leds_stb;
  assign output_leds = s_output_leds;
  assign output_eth_tx_stb = s_output_eth_tx_stb;
  assign output_eth_tx = s_output_eth_tx;

endmodule
