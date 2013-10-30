//name : count_revs
//tag : c components
//input : input_seconds:16
//input : input_sensor:16
//output : output_speed:16
//source_file : count_revs.c
///Count_Revs
///==========
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module count_revs(input_seconds,input_sensor,input_seconds_stb,input_sensor_stb,output_speed_ack,clk,rst,output_speed,output_speed_stb,input_seconds_ack,input_sensor_ack);
  input     [15:0] input_seconds;
  input     [15:0] input_sensor;
  input     input_seconds_stb;
  input     input_sensor_stb;
  input     output_speed_ack;
  input     clk;
  input     rst;
  output    [15:0] output_speed;
  output    output_speed_stb;
  output    input_seconds_ack;
  output    input_sensor_ack;
  reg       [15:0] timer;
  reg       [28:0] program_counter;
  reg       [15:0] address;
  reg       [15:0] data_out;
  reg       [15:0] data_in;
  reg       write_enable;
  reg       [15:0] register_0;
  reg       [15:0] register_1;
  reg       [15:0] register_2;
  reg       [15:0] register_3;
  reg       [15:0] s_output_speed_stb;
  reg       [15:0] s_output_speed;
  reg       [15:0] s_input_seconds_ack;
  reg       [15:0] s_input_sensor_ack;
  reg       [15:0] a;
  reg       [15:0] b;
  reg       [15:0] z;
  reg       [15:0] divisor;
  reg       [15:0] dividend;
  reg       [15:0] quotient;
  reg       [15:0] remainder;
  reg       [15:0] modulo;
  reg       mod_sign;
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
        register_3 <= 16'd0;
      end

      16'd4:
      begin
        register_2 <= register_3;
      end

      16'd5:
      begin
        register_3 <= 16'd0;
        register_3[0] <= input_seconds_stb;
      end

      16'd6:
      begin
        register_3 <= $signed(register_3) == $signed(16'd0);
      end

      16'd7:
      begin
        if (register_3 == 16'h0000)
          program_counter <= 22;
      end

      16'd8:
      begin
        register_3 <= input_sensor;
        program_counter <= 8;
        s_input_sensor_ack <= 1'b1;
       if (s_input_sensor_ack == 1'b1 && input_sensor_stb == 1'b1) begin
          s_input_sensor_ack <= 1'b0;
          program_counter <= 16'd9;
        end
      end

      16'd9:
      begin
        if (register_3 == 16'h0000)
          program_counter <= 11;
      end

      16'd10:
      begin
        register_3 <= register_2;
        program_counter <= 16'd12;
      end

      16'd11:
      begin
        program_counter <= 16'd13;
      end

      16'd12:
      begin
        program_counter <= 16'd8;
      end

      16'd13:
      begin
        register_3 <= input_sensor;
        program_counter <= 13;
        s_input_sensor_ack <= 1'b1;
       if (s_input_sensor_ack == 1'b1 && input_sensor_stb == 1'b1) begin
          s_input_sensor_ack <= 1'b0;
          program_counter <= 16'd14;
        end
      end

      16'd14:
      begin
        register_3 <= $signed(register_3) == $signed(16'd0);
      end

      16'd15:
      begin
        if (register_3 == 16'h0000)
          program_counter <= 17;
      end

      16'd16:
      begin
        register_3 <= register_2;
        program_counter <= 16'd18;
      end

      16'd17:
      begin
        program_counter <= 16'd19;
      end

      16'd18:
      begin
        program_counter <= 16'd13;
      end

      16'd19:
      begin
        register_3 <= register_2;
      end

      16'd20:
      begin
        register_3 <= $signed(register_3) + $signed(16'd1);
      end

      16'd21:
      begin
        register_2 <= register_3;
        program_counter <= 16'd5;
      end

      16'd22:
      begin
        register_3 <= input_seconds;
        program_counter <= 22;
        s_input_seconds_ack <= 1'b1;
       if (s_input_seconds_ack == 1'b1 && input_seconds_stb == 1'b1) begin
          s_input_seconds_ack <= 1'b0;
          program_counter <= 16'd23;
        end
      end

      16'd23:
      begin
        register_3 <= register_2;
      end

      16'd24:
      begin
        register_3 <= $signed(register_3) * $signed(16'd1112);
      end

      16'd25:
      begin
        divisor  <= $signed(register_3);
        dividend <= $signed(16'd500);
        register_3 <= quotient;
        stb <= 1'b0;
        if (ack != 1'b1) begin
          program_counter <= 25;
          stb <= 1'b1;
        end
      end

      16'd26:
      begin
        s_output_speed <= register_3;
        program_counter <= 26;
        s_output_speed_stb <= 1'b1;
        if (s_output_speed_stb == 1'b1 && output_speed_ack == 1'b1) begin
          s_output_speed_stb <= 1'b0;
          program_counter <= 27;
        end
      end

      16'd27:
      begin
        program_counter <= 16'd3;
      end

      16'd28:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
      stb <= 1'b0;
    end
  end
  assign input_seconds_ack = s_input_seconds_ack;
  assign input_sensor_ack = s_input_sensor_ack;
  assign output_speed_stb = s_output_speed_stb;
  assign output_speed = s_output_speed;

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
        mod_sign  <= divisor[15];
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
        modulo <= mod_sign?-(remainder/2):(remainder/2);
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
