//name : display_driver
//tag : c components
//input : input_speed:16
//output : output_digit:16
//output : output_digit_select:16
//source_file : display_driver.c
///Display_Driver
///==============
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module display_driver(input_speed,input_speed_stb,output_digit_ack,output_digit_select_ack,clk,rst,output_digit,output_digit_select,output_digit_stb,output_digit_select_stb,input_speed_ack);
  input     [15:0] input_speed;
  input     input_speed_stb;
  input     output_digit_ack;
  input     output_digit_select_ack;
  input     clk;
  input     rst;
  output    [15:0] output_digit;
  output    [15:0] output_digit_select;
  output    output_digit_stb;
  output    output_digit_select_stb;
  output    input_speed_ack;
  reg       [15:0] timer;
  reg       [163:0] program_counter;
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
  reg       [15:0] s_output_digit_stb;
  reg       [15:0] s_output_digit_select_stb;
  reg       [15:0] s_output_digit;
  reg       [15:0] s_output_digit_select;
  reg       [15:0] s_input_speed_ack;
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
        program_counter <= 16'd63;
        register_3 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_11 <= register_2;
      end

      16'd3:
      begin
        register_11 <= $signed(register_11) == $signed(16'd0);
      end

      16'd4:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 8;
      end

      16'd5:
      begin
        register_11 <= 16'd126;
      end

      16'd6:
      begin
        s_output_digit <= register_11;
        program_counter <= 6;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 7;
        end
      end

      16'd7:
      begin
        program_counter <= 16'd62;
      end

      16'd8:
      begin
        register_11 <= register_2;
      end

      16'd9:
      begin
        register_11 <= $signed(register_11) == $signed(16'd1);
      end

      16'd10:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 14;
      end

      16'd11:
      begin
        register_11 <= 16'd48;
      end

      16'd12:
      begin
        s_output_digit <= register_11;
        program_counter <= 12;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 13;
        end
      end

      16'd13:
      begin
        program_counter <= 16'd62;
      end

      16'd14:
      begin
        register_11 <= register_2;
      end

      16'd15:
      begin
        register_11 <= $signed(register_11) == $signed(16'd2);
      end

      16'd16:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 20;
      end

      16'd17:
      begin
        register_11 <= 16'd109;
      end

      16'd18:
      begin
        s_output_digit <= register_11;
        program_counter <= 18;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 19;
        end
      end

      16'd19:
      begin
        program_counter <= 16'd62;
      end

      16'd20:
      begin
        register_11 <= register_2;
      end

      16'd21:
      begin
        register_11 <= $signed(register_11) == $signed(16'd3);
      end

      16'd22:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 26;
      end

      16'd23:
      begin
        register_11 <= 16'd121;
      end

      16'd24:
      begin
        s_output_digit <= register_11;
        program_counter <= 24;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 25;
        end
      end

      16'd25:
      begin
        program_counter <= 16'd62;
      end

      16'd26:
      begin
        register_11 <= register_2;
      end

      16'd27:
      begin
        register_11 <= $signed(register_11) == $signed(16'd4);
      end

      16'd28:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 32;
      end

      16'd29:
      begin
        register_11 <= 16'd51;
      end

      16'd30:
      begin
        s_output_digit <= register_11;
        program_counter <= 30;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 31;
        end
      end

      16'd31:
      begin
        program_counter <= 16'd62;
      end

      16'd32:
      begin
        register_11 <= register_2;
      end

      16'd33:
      begin
        register_11 <= $signed(register_11) == $signed(16'd5);
      end

      16'd34:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 38;
      end

      16'd35:
      begin
        register_11 <= 16'd91;
      end

      16'd36:
      begin
        s_output_digit <= register_11;
        program_counter <= 36;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 37;
        end
      end

      16'd37:
      begin
        program_counter <= 16'd62;
      end

      16'd38:
      begin
        register_11 <= register_2;
      end

      16'd39:
      begin
        register_11 <= $signed(register_11) == $signed(16'd6);
      end

      16'd40:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 44;
      end

      16'd41:
      begin
        register_11 <= 16'd95;
      end

      16'd42:
      begin
        s_output_digit <= register_11;
        program_counter <= 42;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 43;
        end
      end

      16'd43:
      begin
        program_counter <= 16'd62;
      end

      16'd44:
      begin
        register_11 <= register_2;
      end

      16'd45:
      begin
        register_11 <= $signed(register_11) == $signed(16'd7);
      end

      16'd46:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 50;
      end

      16'd47:
      begin
        register_11 <= 16'd112;
      end

      16'd48:
      begin
        s_output_digit <= register_11;
        program_counter <= 48;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 49;
        end
      end

      16'd49:
      begin
        program_counter <= 16'd62;
      end

      16'd50:
      begin
        register_11 <= register_2;
      end

      16'd51:
      begin
        register_11 <= $signed(register_11) == $signed(16'd8);
      end

      16'd52:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 56;
      end

      16'd53:
      begin
        register_11 <= 16'd127;
      end

      16'd54:
      begin
        s_output_digit <= register_11;
        program_counter <= 54;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 55;
        end
      end

      16'd55:
      begin
        program_counter <= 16'd62;
      end

      16'd56:
      begin
        register_11 <= register_2;
      end

      16'd57:
      begin
        register_11 <= $signed(register_11) == $signed(16'd9);
      end

      16'd58:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 62;
      end

      16'd59:
      begin
        register_11 <= 16'd123;
      end

      16'd60:
      begin
        s_output_digit <= register_11;
        program_counter <= 60;
        s_output_digit_stb <= 1'b1;
        if (s_output_digit_stb == 1'b1 && output_digit_ack == 1'b1) begin
          s_output_digit_stb <= 1'b0;
          program_counter <= 61;
        end
      end

      16'd61:
      begin
        program_counter <= 16'd62;
      end

      16'd62:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

      16'd63:
      begin
        register_5 <= 16'd0;
        register_6 <= 16'd0;
        register_7 <= 16'd0;
        register_8 <= 16'd0;
        register_9 <= 16'd0;
        register_10 <= 16'd0;
      end

      16'd64:
      begin
        register_11 <= 16'd0;
        register_11[0] <= input_speed_stb;
      end

      16'd65:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 106;
      end

      16'd66:
      begin
        register_11 <= input_speed;
        program_counter <= 66;
        s_input_speed_ack <= 1'b1;
       if (s_input_speed_ack == 1'b1 && input_speed_stb == 1'b1) begin
          s_input_speed_ack <= 1'b0;
          program_counter <= 16'd67;
        end
      end

      16'd67:
      begin
        register_6 <= register_11;
        register_11 <= 16'd0;
      end

      16'd68:
      begin
        register_7 <= register_11;
      end

      16'd69:
      begin
        register_11 <= register_6;
      end

      16'd70:
      begin
        register_11 <= $signed(register_11) > $signed(16'd200);
      end

      16'd71:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 78;
      end

      16'd72:
      begin
        register_11 <= register_7;
      end

      16'd73:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd74:
      begin
        register_7 <= register_11;
      end

      16'd75:
      begin
        register_11 <= register_6;
      end

      16'd76:
      begin
        register_11 <= $signed(register_11) - $signed(16'd200);
      end

      16'd77:
      begin
        register_6 <= register_11;
        program_counter <= 16'd69;
      end

      16'd78:
      begin
        register_11 <= 16'd0;
      end

      16'd79:
      begin
        register_8 <= register_11;
      end

      16'd80:
      begin
        register_11 <= register_6;
      end

      16'd81:
      begin
        register_11 <= $signed(register_11) > $signed(16'd20);
      end

      16'd82:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 89;
      end

      16'd83:
      begin
        register_11 <= register_8;
      end

      16'd84:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd85:
      begin
        register_8 <= register_11;
      end

      16'd86:
      begin
        register_11 <= register_6;
      end

      16'd87:
      begin
        register_11 <= $signed(register_11) - $signed(16'd20);
      end

      16'd88:
      begin
        register_6 <= register_11;
        program_counter <= 16'd80;
      end

      16'd89:
      begin
        register_11 <= 16'd0;
      end

      16'd90:
      begin
        register_9 <= register_11;
      end

      16'd91:
      begin
        register_11 <= register_6;
      end

      16'd92:
      begin
        register_11 <= $signed(register_11) > $signed(16'd2);
      end

      16'd93:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 100;
      end

      16'd94:
      begin
        register_11 <= register_9;
      end

      16'd95:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd96:
      begin
        register_9 <= register_11;
      end

      16'd97:
      begin
        register_11 <= register_6;
      end

      16'd98:
      begin
        register_11 <= $signed(register_11) - $signed(16'd2);
      end

      16'd99:
      begin
        register_6 <= register_11;
        program_counter <= 16'd91;
      end

      16'd100:
      begin
        register_11 <= register_6;
      end

      16'd101:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 103;
      end

      16'd102:
      begin
        register_11 <= 16'd5;
      end

      16'd103:
      begin
        if (register_11 != 16'h0000)
          program_counter <= 16'd105;
      end

      16'd104:
      begin
        register_11 <= 16'd0;
      end

      16'd105:
      begin
        register_10 <= register_11;
        program_counter <= 16'd106;
      end

      16'd106:
      begin
        register_11 <= 16'd1;
      end

      16'd107:
      begin
        s_output_digit_select <= register_11;
        program_counter <= 107;
        s_output_digit_select_stb <= 1'b1;
        if (s_output_digit_select_stb == 1'b1 && output_digit_select_ack == 1'b1) begin
          s_output_digit_select_stb <= 1'b0;
          program_counter <= 108;
        end
      end

      16'd108:
      begin
        register_2 <= register_7;
        program_counter <= 16'd2;
        register_0 <= 16'd109;
      end

      16'd109:
      begin
        register_11 <= register_1;
      end

      16'd110:
      begin
        register_11 <= 16'd0;
      end

      16'd111:
      begin
        register_5 <= register_11;
      end

      16'd112:
      begin
        register_11 <= register_5;
      end

      16'd113:
      begin
        register_11 <= $signed(register_11) < $signed(16'd50);
      end

      16'd114:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 120;
      end

      16'd115:
      begin
        register_11 <= 16'd10000;
      end

      16'd116:
      begin
        if (timer < register_11) begin
          program_counter <= program_counter;
          timer <= timer+1;
        end
      end

      16'd117:
      begin
        register_11 <= register_5;
      end

      16'd118:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd119:
      begin
        register_5 <= register_11;
        program_counter <= 16'd112;
      end

      16'd120:
      begin
        register_11 <= 16'd2;
      end

      16'd121:
      begin
        s_output_digit_select <= register_11;
        program_counter <= 121;
        s_output_digit_select_stb <= 1'b1;
        if (s_output_digit_select_stb == 1'b1 && output_digit_select_ack == 1'b1) begin
          s_output_digit_select_stb <= 1'b0;
          program_counter <= 122;
        end
      end

      16'd122:
      begin
        register_2 <= register_8;
        program_counter <= 16'd2;
        register_0 <= 16'd123;
      end

      16'd123:
      begin
        register_11 <= register_1;
      end

      16'd124:
      begin
        register_11 <= 16'd0;
      end

      16'd125:
      begin
        register_5 <= register_11;
      end

      16'd126:
      begin
        register_11 <= register_5;
      end

      16'd127:
      begin
        register_11 <= $signed(register_11) < $signed(16'd50);
      end

      16'd128:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 134;
      end

      16'd129:
      begin
        register_11 <= 16'd10000;
      end

      16'd130:
      begin
        if (timer < register_11) begin
          program_counter <= program_counter;
          timer <= timer+1;
        end
      end

      16'd131:
      begin
        register_11 <= register_5;
      end

      16'd132:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd133:
      begin
        register_5 <= register_11;
        program_counter <= 16'd126;
      end

      16'd134:
      begin
        register_11 <= 16'd4;
      end

      16'd135:
      begin
        s_output_digit_select <= register_11;
        program_counter <= 135;
        s_output_digit_select_stb <= 1'b1;
        if (s_output_digit_select_stb == 1'b1 && output_digit_select_ack == 1'b1) begin
          s_output_digit_select_stb <= 1'b0;
          program_counter <= 136;
        end
      end

      16'd136:
      begin
        register_2 <= register_9;
        program_counter <= 16'd2;
        register_0 <= 16'd137;
      end

      16'd137:
      begin
        register_11 <= register_1;
      end

      16'd138:
      begin
        register_11 <= 16'd0;
      end

      16'd139:
      begin
        register_5 <= register_11;
      end

      16'd140:
      begin
        register_11 <= register_5;
      end

      16'd141:
      begin
        register_11 <= $signed(register_11) < $signed(16'd50);
      end

      16'd142:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 148;
      end

      16'd143:
      begin
        register_11 <= 16'd10000;
      end

      16'd144:
      begin
        if (timer < register_11) begin
          program_counter <= program_counter;
          timer <= timer+1;
        end
      end

      16'd145:
      begin
        register_11 <= register_5;
      end

      16'd146:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd147:
      begin
        register_5 <= register_11;
        program_counter <= 16'd140;
      end

      16'd148:
      begin
        register_11 <= 16'd8;
      end

      16'd149:
      begin
        s_output_digit_select <= register_11;
        program_counter <= 149;
        s_output_digit_select_stb <= 1'b1;
        if (s_output_digit_select_stb == 1'b1 && output_digit_select_ack == 1'b1) begin
          s_output_digit_select_stb <= 1'b0;
          program_counter <= 150;
        end
      end

      16'd150:
      begin
        register_2 <= register_10;
        program_counter <= 16'd2;
        register_0 <= 16'd151;
      end

      16'd151:
      begin
        register_11 <= register_1;
      end

      16'd152:
      begin
        register_11 <= 16'd0;
      end

      16'd153:
      begin
        register_5 <= register_11;
      end

      16'd154:
      begin
        register_11 <= register_5;
      end

      16'd155:
      begin
        register_11 <= $signed(register_11) < $signed(16'd50);
      end

      16'd156:
      begin
        if (register_11 == 16'h0000)
          program_counter <= 162;
      end

      16'd157:
      begin
        register_11 <= 16'd10000;
      end

      16'd158:
      begin
        if (timer < register_11) begin
          program_counter <= program_counter;
          timer <= timer+1;
        end
      end

      16'd159:
      begin
        register_11 <= register_5;
      end

      16'd160:
      begin
        register_11 <= $signed(register_11) + $signed(16'd1);
      end

      16'd161:
      begin
        register_5 <= register_11;
        program_counter <= 16'd154;
      end

      16'd162:
      begin
        program_counter <= 16'd64;
      end

      16'd163:
      begin
        register_4 <= 16'd0;
        program_counter <= register_3;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end
  assign input_speed_ack = s_input_speed_ack;
  assign output_digit_stb = s_output_digit_stb;
  assign output_digit = s_output_digit;
  assign output_digit_select_stb = s_output_digit_select_stb;
  assign output_digit_select = s_output_digit_select;

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
