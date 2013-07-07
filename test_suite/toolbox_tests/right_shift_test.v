//name : right_shift_test
//tag : c components
//input : input_a:16
//output : output_a:16
//output : output_b:16
//source_file : right_shift_test.c
///Right_Shift_Test
///================
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module right_shift_test(input_a,input_a_stb,output_a_ack,output_b_ack,clk,rst,output_a,output_b,output_a_stb,output_b_stb,input_a_ack);
  input     [15:0] input_a;
  input     input_a_stb;
  input     output_a_ack;
  input     output_b_ack;
  input     clk;
  input     rst;
  output    [15:0] output_a;
  output    [15:0] output_b;
  output    output_a_stb;
  output    output_b_stb;
  output    input_a_ack;
  reg       [15:0] timer;
  reg       [201:0] program_counter;
  reg       [15:0] address;
  reg       [15:0] data_out;
  reg       [15:0] data_in;
  reg       write_enable;
  reg       [15:0] register_0;
  reg       [15:0] register_1;
  reg       [15:0] register_2;
  reg       [15:0] s_output_a_stb;
  reg       [15:0] s_output_b_stb;
  reg       [15:0] s_output_a;
  reg       [15:0] s_output_b;
  reg       [15:0] s_input_a_ack;
  reg       [15:0] a;
  reg       [15:0] b;
  reg       [15:0] z;
  reg       [15:0] divisor;
  reg       [15:0] dividend;
  reg       [15:0] quotient;
  reg       [15:0] remainder;
  reg       [15:0] modulo;
  reg       [4:0] count;
  reg       [1:0] state;
  reg       stb;
  reg       ack;
  reg       sign;
  wire      [15:0] difference;
  parameter [1:0] start= 2'd0;
  parameter [1:0] calculate= 2'd1;
  parameter [1:0] finish= 2'd2;
  parameter [1:0] acknowledge= 2'd3;
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
        program_counter <= 16'd2;
        register_0 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_2 <= 16'd65535;
      end

      16'd3:
      begin
        s_output_a <= register_2;
        program_counter <= 3;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 4;
        end
      end

      16'd4:
      begin
        register_2 <= 16'd0;
      end

      16'd5:
      begin
        s_output_b <= register_2;
        program_counter <= 5;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 6;
        end
      end

      16'd6:
      begin
        register_2 <= input_a;
        program_counter <= 6;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd7;
        end
      end

      16'd7:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd8:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 5 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd9:
      begin
        s_output_a <= register_2;
        program_counter <= 9;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 10;
        end
      end

      16'd10:
      begin
        register_2 <= 16'd1;
      end

      16'd11:
      begin
        s_output_b <= register_2;
        program_counter <= 11;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 12;
        end
      end

      16'd12:
      begin
        register_2 <= input_a;
        program_counter <= 12;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd13;
        end
      end

      16'd13:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd14:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 6 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd15:
      begin
        s_output_a <= register_2;
        program_counter <= 15;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 16;
        end
      end

      16'd16:
      begin
        register_2 <= 16'd2;
      end

      16'd17:
      begin
        s_output_b <= register_2;
        program_counter <= 17;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 18;
        end
      end

      16'd18:
      begin
        register_2 <= input_a;
        program_counter <= 18;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd19;
        end
      end

      16'd19:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd20:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 7 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd21:
      begin
        s_output_a <= register_2;
        program_counter <= 21;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 22;
        end
      end

      16'd22:
      begin
        register_2 <= 16'd3;
      end

      16'd23:
      begin
        s_output_b <= register_2;
        program_counter <= 23;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 24;
        end
      end

      16'd24:
      begin
        register_2 <= input_a;
        program_counter <= 24;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd25;
        end
      end

      16'd25:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd26:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 8 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd27:
      begin
        s_output_a <= register_2;
        program_counter <= 27;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 28;
        end
      end

      16'd28:
      begin
        register_2 <= 16'd4;
      end

      16'd29:
      begin
        s_output_b <= register_2;
        program_counter <= 29;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 30;
        end
      end

      16'd30:
      begin
        register_2 <= input_a;
        program_counter <= 30;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd31;
        end
      end

      16'd31:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd32:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 9 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd33:
      begin
        s_output_a <= register_2;
        program_counter <= 33;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 34;
        end
      end

      16'd34:
      begin
        register_2 <= 16'd5;
      end

      16'd35:
      begin
        s_output_b <= register_2;
        program_counter <= 35;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 36;
        end
      end

      16'd36:
      begin
        register_2 <= input_a;
        program_counter <= 36;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd37;
        end
      end

      16'd37:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd38:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 10 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd39:
      begin
        s_output_a <= register_2;
        program_counter <= 39;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 40;
        end
      end

      16'd40:
      begin
        register_2 <= 16'd6;
      end

      16'd41:
      begin
        s_output_b <= register_2;
        program_counter <= 41;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 42;
        end
      end

      16'd42:
      begin
        register_2 <= input_a;
        program_counter <= 42;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd43;
        end
      end

      16'd43:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd44:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 11 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd45:
      begin
        s_output_a <= register_2;
        program_counter <= 45;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 46;
        end
      end

      16'd46:
      begin
        register_2 <= 16'd7;
      end

      16'd47:
      begin
        s_output_b <= register_2;
        program_counter <= 47;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 48;
        end
      end

      16'd48:
      begin
        register_2 <= input_a;
        program_counter <= 48;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd49;
        end
      end

      16'd49:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd50:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 12 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd51:
      begin
        s_output_a <= register_2;
        program_counter <= 51;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 52;
        end
      end

      16'd52:
      begin
        register_2 <= 16'd8;
      end

      16'd53:
      begin
        s_output_b <= register_2;
        program_counter <= 53;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 54;
        end
      end

      16'd54:
      begin
        register_2 <= input_a;
        program_counter <= 54;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd55;
        end
      end

      16'd55:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd56:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 13 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd57:
      begin
        s_output_a <= register_2;
        program_counter <= 57;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 58;
        end
      end

      16'd58:
      begin
        register_2 <= 16'd9;
      end

      16'd59:
      begin
        s_output_b <= register_2;
        program_counter <= 59;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 60;
        end
      end

      16'd60:
      begin
        register_2 <= input_a;
        program_counter <= 60;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd61;
        end
      end

      16'd61:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd62:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 14 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd63:
      begin
        s_output_a <= register_2;
        program_counter <= 63;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 64;
        end
      end

      16'd64:
      begin
        register_2 <= 16'd10;
      end

      16'd65:
      begin
        s_output_b <= register_2;
        program_counter <= 65;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 66;
        end
      end

      16'd66:
      begin
        register_2 <= input_a;
        program_counter <= 66;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd67;
        end
      end

      16'd67:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd68:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 15 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd69:
      begin
        s_output_a <= register_2;
        program_counter <= 69;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 70;
        end
      end

      16'd70:
      begin
        register_2 <= 16'd11;
      end

      16'd71:
      begin
        s_output_b <= register_2;
        program_counter <= 71;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 72;
        end
      end

      16'd72:
      begin
        register_2 <= input_a;
        program_counter <= 72;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd73;
        end
      end

      16'd73:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd74:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 16 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd75:
      begin
        s_output_a <= register_2;
        program_counter <= 75;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 76;
        end
      end

      16'd76:
      begin
        register_2 <= 16'd12;
      end

      16'd77:
      begin
        s_output_b <= register_2;
        program_counter <= 77;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 78;
        end
      end

      16'd78:
      begin
        register_2 <= input_a;
        program_counter <= 78;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd79;
        end
      end

      16'd79:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd80:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 17 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd81:
      begin
        s_output_a <= register_2;
        program_counter <= 81;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 82;
        end
      end

      16'd82:
      begin
        register_2 <= 16'd13;
      end

      16'd83:
      begin
        s_output_b <= register_2;
        program_counter <= 83;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 84;
        end
      end

      16'd84:
      begin
        register_2 <= input_a;
        program_counter <= 84;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd85;
        end
      end

      16'd85:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd86:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 18 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd87:
      begin
        s_output_a <= register_2;
        program_counter <= 87;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 88;
        end
      end

      16'd88:
      begin
        register_2 <= 16'd14;
      end

      16'd89:
      begin
        s_output_b <= register_2;
        program_counter <= 89;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 90;
        end
      end

      16'd90:
      begin
        register_2 <= input_a;
        program_counter <= 90;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd91;
        end
      end

      16'd91:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd92:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 19 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd93:
      begin
        s_output_a <= register_2;
        program_counter <= 93;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 94;
        end
      end

      16'd94:
      begin
        register_2 <= 16'd15;
      end

      16'd95:
      begin
        s_output_b <= register_2;
        program_counter <= 95;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 96;
        end
      end

      16'd96:
      begin
        register_2 <= input_a;
        program_counter <= 96;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd97;
        end
      end

      16'd97:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd98:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 20 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd65535;
      end

      16'd99:
      begin
        s_output_a <= register_2;
        program_counter <= 99;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 100;
        end
      end

      16'd100:
      begin
        register_2 <= 16'd16;
      end

      16'd101:
      begin
        s_output_b <= register_2;
        program_counter <= 101;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 102;
        end
      end

      16'd102:
      begin
        register_2 <= input_a;
        program_counter <= 102;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd103;
        end
      end

      16'd103:
      begin
        register_2 <= $signed(register_2) == $signed(16'd65535);
      end

      16'd104:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 21 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd105:
      begin
        s_output_a <= register_2;
        program_counter <= 105;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 106;
        end
      end

      16'd106:
      begin
        register_2 <= 16'd0;
      end

      16'd107:
      begin
        s_output_b <= register_2;
        program_counter <= 107;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 108;
        end
      end

      16'd108:
      begin
        register_2 <= input_a;
        program_counter <= 108;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd109;
        end
      end

      16'd109:
      begin
        register_2 <= $signed(register_2) == $signed(16'd32767);
      end

      16'd110:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 22 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd111:
      begin
        s_output_a <= register_2;
        program_counter <= 111;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 112;
        end
      end

      16'd112:
      begin
        register_2 <= 16'd1;
      end

      16'd113:
      begin
        s_output_b <= register_2;
        program_counter <= 113;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 114;
        end
      end

      16'd114:
      begin
        register_2 <= input_a;
        program_counter <= 114;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd115;
        end
      end

      16'd115:
      begin
        register_2 <= $signed(register_2) == $signed(16'd16383);
      end

      16'd116:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 23 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd117:
      begin
        s_output_a <= register_2;
        program_counter <= 117;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 118;
        end
      end

      16'd118:
      begin
        register_2 <= 16'd2;
      end

      16'd119:
      begin
        s_output_b <= register_2;
        program_counter <= 119;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 120;
        end
      end

      16'd120:
      begin
        register_2 <= input_a;
        program_counter <= 120;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd121;
        end
      end

      16'd121:
      begin
        register_2 <= $signed(register_2) == $signed(16'd8191);
      end

      16'd122:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 24 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd123:
      begin
        s_output_a <= register_2;
        program_counter <= 123;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 124;
        end
      end

      16'd124:
      begin
        register_2 <= 16'd3;
      end

      16'd125:
      begin
        s_output_b <= register_2;
        program_counter <= 125;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 126;
        end
      end

      16'd126:
      begin
        register_2 <= input_a;
        program_counter <= 126;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd127;
        end
      end

      16'd127:
      begin
        register_2 <= $signed(register_2) == $signed(16'd4095);
      end

      16'd128:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 25 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd129:
      begin
        s_output_a <= register_2;
        program_counter <= 129;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 130;
        end
      end

      16'd130:
      begin
        register_2 <= 16'd4;
      end

      16'd131:
      begin
        s_output_b <= register_2;
        program_counter <= 131;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 132;
        end
      end

      16'd132:
      begin
        register_2 <= input_a;
        program_counter <= 132;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd133;
        end
      end

      16'd133:
      begin
        register_2 <= $signed(register_2) == $signed(16'd2047);
      end

      16'd134:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 26 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd135:
      begin
        s_output_a <= register_2;
        program_counter <= 135;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 136;
        end
      end

      16'd136:
      begin
        register_2 <= 16'd5;
      end

      16'd137:
      begin
        s_output_b <= register_2;
        program_counter <= 137;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 138;
        end
      end

      16'd138:
      begin
        register_2 <= input_a;
        program_counter <= 138;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd139;
        end
      end

      16'd139:
      begin
        register_2 <= $signed(register_2) == $signed(16'd1023);
      end

      16'd140:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 27 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd141:
      begin
        s_output_a <= register_2;
        program_counter <= 141;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 142;
        end
      end

      16'd142:
      begin
        register_2 <= 16'd6;
      end

      16'd143:
      begin
        s_output_b <= register_2;
        program_counter <= 143;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 144;
        end
      end

      16'd144:
      begin
        register_2 <= input_a;
        program_counter <= 144;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd145;
        end
      end

      16'd145:
      begin
        register_2 <= $signed(register_2) == $signed(16'd511);
      end

      16'd146:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 28 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd147:
      begin
        s_output_a <= register_2;
        program_counter <= 147;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 148;
        end
      end

      16'd148:
      begin
        register_2 <= 16'd7;
      end

      16'd149:
      begin
        s_output_b <= register_2;
        program_counter <= 149;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 150;
        end
      end

      16'd150:
      begin
        register_2 <= input_a;
        program_counter <= 150;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd151;
        end
      end

      16'd151:
      begin
        register_2 <= $signed(register_2) == $signed(16'd255);
      end

      16'd152:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 29 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd153:
      begin
        s_output_a <= register_2;
        program_counter <= 153;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 154;
        end
      end

      16'd154:
      begin
        register_2 <= 16'd8;
      end

      16'd155:
      begin
        s_output_b <= register_2;
        program_counter <= 155;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 156;
        end
      end

      16'd156:
      begin
        register_2 <= input_a;
        program_counter <= 156;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd157;
        end
      end

      16'd157:
      begin
        register_2 <= $signed(register_2) == $signed(16'd127);
      end

      16'd158:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 30 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd159:
      begin
        s_output_a <= register_2;
        program_counter <= 159;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 160;
        end
      end

      16'd160:
      begin
        register_2 <= 16'd9;
      end

      16'd161:
      begin
        s_output_b <= register_2;
        program_counter <= 161;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 162;
        end
      end

      16'd162:
      begin
        register_2 <= input_a;
        program_counter <= 162;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd163;
        end
      end

      16'd163:
      begin
        register_2 <= $signed(register_2) == $signed(16'd63);
      end

      16'd164:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 31 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd165:
      begin
        s_output_a <= register_2;
        program_counter <= 165;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 166;
        end
      end

      16'd166:
      begin
        register_2 <= 16'd10;
      end

      16'd167:
      begin
        s_output_b <= register_2;
        program_counter <= 167;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 168;
        end
      end

      16'd168:
      begin
        register_2 <= input_a;
        program_counter <= 168;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd169;
        end
      end

      16'd169:
      begin
        register_2 <= $signed(register_2) == $signed(16'd31);
      end

      16'd170:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 32 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd171:
      begin
        s_output_a <= register_2;
        program_counter <= 171;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 172;
        end
      end

      16'd172:
      begin
        register_2 <= 16'd11;
      end

      16'd173:
      begin
        s_output_b <= register_2;
        program_counter <= 173;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 174;
        end
      end

      16'd174:
      begin
        register_2 <= input_a;
        program_counter <= 174;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd175;
        end
      end

      16'd175:
      begin
        register_2 <= $signed(register_2) == $signed(16'd15);
      end

      16'd176:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 33 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd177:
      begin
        s_output_a <= register_2;
        program_counter <= 177;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 178;
        end
      end

      16'd178:
      begin
        register_2 <= 16'd12;
      end

      16'd179:
      begin
        s_output_b <= register_2;
        program_counter <= 179;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 180;
        end
      end

      16'd180:
      begin
        register_2 <= input_a;
        program_counter <= 180;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd181;
        end
      end

      16'd181:
      begin
        register_2 <= $signed(register_2) == $signed(16'd7);
      end

      16'd182:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 34 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd183:
      begin
        s_output_a <= register_2;
        program_counter <= 183;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 184;
        end
      end

      16'd184:
      begin
        register_2 <= 16'd13;
      end

      16'd185:
      begin
        s_output_b <= register_2;
        program_counter <= 185;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 186;
        end
      end

      16'd186:
      begin
        register_2 <= input_a;
        program_counter <= 186;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd187;
        end
      end

      16'd187:
      begin
        register_2 <= $signed(register_2) == $signed(16'd3);
      end

      16'd188:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 35 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd189:
      begin
        s_output_a <= register_2;
        program_counter <= 189;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 190;
        end
      end

      16'd190:
      begin
        register_2 <= 16'd14;
      end

      16'd191:
      begin
        s_output_b <= register_2;
        program_counter <= 191;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 192;
        end
      end

      16'd192:
      begin
        register_2 <= input_a;
        program_counter <= 192;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd193;
        end
      end

      16'd193:
      begin
        register_2 <= $signed(register_2) == $signed(16'd1);
      end

      16'd194:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 36 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32767;
      end

      16'd195:
      begin
        s_output_a <= register_2;
        program_counter <= 195;
        s_output_a_stb <= 1'b1;
        if (s_output_a_stb == 1'b1 && output_a_ack == 1'b1) begin
          s_output_a_stb <= 1'b0;
          program_counter <= 196;
        end
      end

      16'd196:
      begin
        register_2 <= 16'd15;
      end

      16'd197:
      begin
        s_output_b <= register_2;
        program_counter <= 197;
        s_output_b_stb <= 1'b1;
        if (s_output_b_stb == 1'b1 && output_b_ack == 1'b1) begin
          s_output_b_stb <= 1'b0;
          program_counter <= 198;
        end
      end

      16'd198:
      begin
        register_2 <= input_a;
        program_counter <= 198;
        s_input_a_ack <= 1'b1;
       if (s_input_a_ack == 1'b1 && input_a_stb == 1'b1) begin
          s_input_a_ack <= 1'b0;
          program_counter <= 16'd199;
        end
      end

      16'd199:
      begin
        register_2 <= $signed(register_2) == $signed(16'd0);
        register_1 <= 16'd0;
      end

      16'd200:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 37 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd1;
      end

      16'd201:
      begin
        $display ("%d (report at line: 38 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/right_shift_test.c)", $signed(register_2));
        program_counter <= register_0;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
      stb <= 1'b0;
    end
  end
  assign input_a_ack = s_input_a_ack;
  assign output_a_stb = s_output_a_stb;
  assign output_a = s_output_a;
  assign output_b_stb = s_output_b_stb;
  assign output_b = s_output_b;

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

  always @(posedge clk)
  begin

    ack <= 1'b0;

    case (state)

      start: begin

        a <= divisor[15]?-divisor:divisor;
        b <= dividend[15]?-dividend:dividend;
        remainder <= 15'd0;
        z <= 15'd0;
        sign  <= divisor[15] ^ dividend[15];
        count <= 5'd16;

        if( stb == 1'b1 ) begin
          state <= calculate;
        end

      end //start

      calculate: begin

        if( difference[15] == 0 ) begin //if remainder > b
          z <= z * 2 + 1;
          remainder <= {difference[14:0], a[15]};
        end else begin
          z <= z * 2;
          remainder <= {remainder[14:0], a[15]};
        end

        a <= a * 2;
        if( count == 5'd0 ) begin
          state <= finish;
        end else begin
          count <= count - 1;
        end

      end //calculate

      finish: begin

        quotient <= sign?-z:z;
        modulo <= divisor[15]?-modulo:modulo;
        ack      <= 1'b1;
        state    <= acknowledge;

      end //finish

      acknowledge: begin

        ack      <= 1'b0;
        state    <= start;

      end //wait

    endcase

    if( rst == 1'b1 ) begin
      ack   <= 1'b0;
      state <= start;
    end //if
  end

  assign difference = remainder - b;


endmodule
