//name : subtractor_test
//tag : c components
//input : input_a:16
//output : output_a:16
//output : output_b:16
//source_file : subtractor_test.c
///Subtractor_Test
///===============
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module subtractor_test(input_a,input_a_stb,output_a_ack,output_b_ack,clk,rst,output_a,output_b,output_a_stb,output_b_stb,input_a_ack);
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
  reg       [63:0] program_counter;
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
        register_2 <= 16'd0;
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
        register_2 <= 16'd1;
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
          $display("Assertion failed at line: 5 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd0;
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
        register_2 <= 16'd2;
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
        register_2 <= $signed(register_2) == $signed(16'd65534);
      end

      16'd14:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 6 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd0;
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
        register_2 <= 16'd3;
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
        register_2 <= $signed(register_2) == $signed(16'd65533);
      end

      16'd20:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 7 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32768;
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
        register_2 <= 16'd0;
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
        register_2 <= $signed(register_2) == $signed(16'd32768);
      end

      16'd26:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 8 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32768;
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
        register_2 <= 16'd1;
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
        register_2 <= $signed(register_2) == $signed(16'd32767);
      end

      16'd32:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 9 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd32768;
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
        register_2 <= 16'd2;
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
        register_2 <= $signed(register_2) == $signed(16'd32766);
      end

      16'd38:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 10 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd0;
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
        register_2 <= 16'd0;
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
        register_2 <= $signed(register_2) == $signed(16'd0);
      end

      16'd44:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 11 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd0;
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
        register_2 <= 16'd1;
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
          $display("Assertion failed at line: 12 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd0;
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
        register_2 <= 16'd2;
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
        register_2 <= $signed(register_2) == $signed(16'd65534);
      end

      16'd56:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 13 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd1;
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
        register_2 <= 16'd1;
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
        register_2 <= $signed(register_2) == $signed(16'd0);
        register_1 <= 16'd0;
      end

      16'd62:
      begin
        if (register_2 == 16'h0000) begin
          $display("Assertion failed at line: 14 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c");
          $finish_and_return(1);
        end
        register_2 <= 16'd1;
      end

      16'd63:
      begin
        $display ("%d (report at line: 15 in file: /home/jon/Projects/Chips-2.0/test_suite/toolbox_tests/subtractor_test.c)", $signed(register_2));
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
