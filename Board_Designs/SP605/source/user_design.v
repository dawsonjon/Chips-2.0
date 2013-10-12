//name : user_design
//tag : c components
//source_file : test.c
///User_Design
///===========
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module user_design;
  reg       [15:0] timer;
  reg       [23:0] program_counter;
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
  reg       clk;
  reg       rst;
  reg [15:0] memory [4:0];

  //////////////////////////////////////////////////////////////////////////////
  // CLOCK AND RESET GENERATION                                                 
  //                                                                            
  // This file was generated in test bench mode. In this mode, the verilog      
  // output file can be executed directly within a verilog simulator.           
  // In test bench mode, a simulated clock and reset signal are generated within
  // the output file.                                                           
  // Verilog files generated in testbecnch mode are not suitable for synthesis, 
  // or for instantiation within a larger design.
  
initial
  begin
    rst <= 1'b1;
    #50 rst <= 1'b0;
  end

  
initial
  begin
    clk <= 1'b0;
    while (1) begin
      #5 clk <= ~clk;
    end
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
        program_counter <= 16'd17;
        register_4 <= 16'd1;
      end

      16'd1:
      begin
        $finish;
        program_counter <= program_counter;
      end

      16'd2:
      begin
        register_3 <= 16'd0;
        register_7 <= 16'd0;
      end

      16'd3:
      begin
        register_3 <= register_7;
      end

      16'd4:
      begin
        register_7 <= register_3;
      end

      16'd5:
      begin
        register_7 <= $signed(register_7) < $signed(16'd5);
      end

      16'd6:
      begin
        if (register_7 == 16'h0000)
          program_counter <= 16;
      end

      16'd7:
      begin
        register_7 <= register_3;
      end

      16'd8:
      begin
        register_7 <= $signed(register_7) + $signed(register_2);
      end

      16'd9:
      begin
        address <= register_7;
      end

      16'd10:
      begin
        register_7 <= data_out;
      end

      16'd11:
      begin
        register_7 <= data_out;
      end

      16'd12:
      begin
        $display ("%d (report at line: 5 in file: test.c)", $signed(register_7));
      end

      16'd13:
      begin
        register_7 <= register_3;
      end

      16'd14:
      begin
        register_7 <= $signed(register_7) + $signed(16'd1);
      end

      16'd15:
      begin
        register_3 <= register_7;
        program_counter <= 16'd4;
      end

      16'd16:
      begin
        register_1 <= 16'd0;
        program_counter <= register_0;
      end

      16'd17:
      begin
        register_6 <= 16'd0;
        register_7 <= 16'd0;
      end

      16'd18:
      begin
        register_7 <= $signed(register_7) + $signed(register_6);
        register_2 <= register_6;
      end

      16'd19:
      begin
        address <= register_7;
      end

      16'd20:
      begin
        register_7 <= data_out;
      end

      16'd21:
      begin
        register_7 <= data_out;
      end

      16'd22:
      begin
        $display ("%d (report at line: 12 in file: test.c)", $signed(register_7));
        program_counter <= 16'd2;
        register_0 <= 16'd23;
      end

      16'd23:
      begin
        register_7 <= register_1;
        register_5 <= 16'd0;
        program_counter <= register_4;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end

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
