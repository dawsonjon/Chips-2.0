//name : test
//tag : c components
//source_file : socket_access_tb.c
///Test
///====
///
///*Created by C2CHIP*

  
`timescale 1ns/1ps
module test;
  integer file_count;
  reg       [15:0] timer;
  reg       [5:0] program_counter;
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
  reg       clk;
  reg       rst;
  reg [15:0] memory [-1:0];

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
  // MEMORY INITIALIZATION                                                      
  //                                                                            
  // In order to reduce program size, array contents have been stored into      
  // memory at initialization. In an FPGA, this will result in the memory being 
  // initialized when the FPGA configures.                                      
  // Memory will not be re-initialized at reset.                                
  // Dissable this behaviour using the no_initialize_memory switch              
  
  initial
  begin
  end

  
  initial
  begin
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
    timer <= 16'h0000;

    case(program_counter)

      16'd0:
      begin
        program_counter <= 16'd1;
        program_counter <= 16'd44;
        register_11 <= 16'd1;
      end

      16'd1:
      begin
        program_counter <= 16'd3;
        $finish;
        program_counter <= program_counter;
      end

      16'd3:
      begin
        program_counter <= 16'd2;
        register_13 <= register_2;
        register_1 <= 16'd0;
      end

      16'd2:
      begin
        program_counter <= 16'd6;
        $display ("%d (report at line: 4 in file: socket_access.h)", $signed(register_13));
        program_counter <= register_0;
      end

      16'd6:
      begin
        program_counter <= 16'd7;
        register_6 <= 16'd48;
        register_7 <= 16'd48;
        register_8 <= 16'd48;
        register_9 <= 16'd48;
        register_10 <= 16'd48;
      end

      16'd7:
      begin
        program_counter <= 16'd5;
        register_15 <= register_5;
      end

      16'd5:
      begin
        program_counter <= 16'd4;
        register_14 <= $unsigned(register_15) >= $unsigned(16'd10000);
      end

      16'd4:
      begin
        program_counter <= 16'd12;
        if (register_14 == 16'h0000)
          program_counter <= 14;
      end

      16'd12:
      begin
        program_counter <= 16'd13;
        register_17 <= register_10;
        register_19 <= register_5;
      end

      16'd13:
      begin
        program_counter <= 16'd15;
        register_16 <= $signed(register_17) + $signed(16'd1);
        register_18 <= $unsigned(register_19) - $unsigned(16'd10000);
      end

      16'd15:
      begin
        program_counter <= 16'd14;
        register_10 <= register_16;
        register_5 <= register_18;
        program_counter <= 16'd10;
      end

      16'd14:
      begin
        program_counter <= 16'd10;
        program_counter <= 16'd11;
      end

      16'd10:
      begin
        program_counter <= 16'd11;
        program_counter <= 16'd7;
      end

      16'd11:
      begin
        program_counter <= 16'd9;
        register_2 <= register_10;
        program_counter <= 16'd3;
        register_0 <= 16'd9;
      end

      16'd9:
      begin
        program_counter <= 16'd8;
        register_20 <= register_1;
      end

      16'd8:
      begin
        program_counter <= 16'd24;
        register_22 <= register_5;
      end

      16'd24:
      begin
        program_counter <= 16'd25;
        register_21 <= $unsigned(register_22) >= $unsigned(16'd1000);
      end

      16'd25:
      begin
        program_counter <= 16'd27;
        if (register_21 == 16'h0000)
          program_counter <= 31;
      end

      16'd27:
      begin
        program_counter <= 16'd26;
        register_24 <= register_9;
        register_26 <= register_5;
      end

      16'd26:
      begin
        program_counter <= 16'd30;
        register_23 <= $signed(register_24) + $signed(16'd1);
        register_25 <= $unsigned(register_26) - $unsigned(16'd1000);
      end

      16'd30:
      begin
        program_counter <= 16'd31;
        register_9 <= register_23;
        register_5 <= register_25;
        program_counter <= 16'd29;
      end

      16'd31:
      begin
        program_counter <= 16'd29;
        program_counter <= 16'd28;
      end

      16'd29:
      begin
        program_counter <= 16'd28;
        program_counter <= 16'd8;
      end

      16'd28:
      begin
        program_counter <= 16'd20;
        register_2 <= register_9;
        program_counter <= 16'd3;
        register_0 <= 16'd20;
      end

      16'd20:
      begin
        program_counter <= 16'd21;
        register_27 <= register_1;
      end

      16'd21:
      begin
        program_counter <= 16'd23;
        register_29 <= register_5;
      end

      16'd23:
      begin
        program_counter <= 16'd22;
        register_28 <= $unsigned(register_29) >= $unsigned(16'd100);
      end

      16'd22:
      begin
        program_counter <= 16'd18;
        if (register_28 == 16'h0000)
          program_counter <= 16;
      end

      16'd18:
      begin
        program_counter <= 16'd19;
        register_31 <= register_8;
        register_33 <= register_5;
      end

      16'd19:
      begin
        program_counter <= 16'd17;
        register_30 <= $signed(register_31) + $signed(16'd1);
        register_32 <= $unsigned(register_33) - $unsigned(16'd100);
      end

      16'd17:
      begin
        program_counter <= 16'd16;
        register_8 <= register_30;
        register_5 <= register_32;
        program_counter <= 16'd48;
      end

      16'd16:
      begin
        program_counter <= 16'd48;
        program_counter <= 16'd49;
      end

      16'd48:
      begin
        program_counter <= 16'd49;
        program_counter <= 16'd21;
      end

      16'd49:
      begin
        program_counter <= 16'd51;
        register_2 <= register_8;
        program_counter <= 16'd3;
        register_0 <= 16'd51;
      end

      16'd51:
      begin
        program_counter <= 16'd50;
        register_34 <= register_1;
      end

      16'd50:
      begin
        program_counter <= 16'd54;
        register_36 <= register_5;
      end

      16'd54:
      begin
        program_counter <= 16'd55;
        register_35 <= $unsigned(register_36) >= $unsigned(16'd10);
      end

      16'd55:
      begin
        program_counter <= 16'd53;
        if (register_35 == 16'h0000)
          program_counter <= 61;
      end

      16'd53:
      begin
        program_counter <= 16'd52;
        register_38 <= register_7;
        register_40 <= register_5;
      end

      16'd52:
      begin
        program_counter <= 16'd60;
        register_37 <= $signed(register_38) + $signed(16'd1);
        register_39 <= $unsigned(register_40) - $unsigned(16'd10);
      end

      16'd60:
      begin
        program_counter <= 16'd61;
        register_7 <= register_37;
        register_5 <= register_39;
        program_counter <= 16'd63;
      end

      16'd61:
      begin
        program_counter <= 16'd63;
        program_counter <= 16'd62;
      end

      16'd63:
      begin
        program_counter <= 16'd62;
        program_counter <= 16'd50;
      end

      16'd62:
      begin
        program_counter <= 16'd58;
        register_2 <= register_7;
        program_counter <= 16'd3;
        register_0 <= 16'd58;
      end

      16'd58:
      begin
        program_counter <= 16'd59;
        register_41 <= register_1;
      end

      16'd59:
      begin
        program_counter <= 16'd57;
        register_43 <= register_5;
      end

      16'd57:
      begin
        program_counter <= 16'd56;
        register_42 <= $unsigned(register_43) >= $unsigned(16'd1);
      end

      16'd56:
      begin
        program_counter <= 16'd40;
        if (register_42 == 16'h0000)
          program_counter <= 42;
      end

      16'd40:
      begin
        program_counter <= 16'd41;
        register_45 <= register_6;
        register_47 <= register_5;
      end

      16'd41:
      begin
        program_counter <= 16'd43;
        register_44 <= $signed(register_45) + $signed(16'd1);
        register_46 <= $unsigned(register_47) - $unsigned(16'd1);
      end

      16'd43:
      begin
        program_counter <= 16'd42;
        register_6 <= register_44;
        register_5 <= register_46;
        program_counter <= 16'd46;
      end

      16'd42:
      begin
        program_counter <= 16'd46;
        program_counter <= 16'd47;
      end

      16'd46:
      begin
        program_counter <= 16'd47;
        program_counter <= 16'd59;
      end

      16'd47:
      begin
        program_counter <= 16'd45;
        register_2 <= register_6;
        program_counter <= 16'd3;
        register_0 <= 16'd45;
      end

      16'd45:
      begin
        program_counter <= 16'd44;
        register_48 <= register_1;
        register_4 <= 16'd0;
        program_counter <= register_3;
      end

      16'd44:
      begin
        program_counter <= 16'd36;
        register_5 <= 16'd25;
        program_counter <= 16'd6;
        register_3 <= 16'd36;
      end

      16'd36:
      begin
        program_counter <= 16'd37;
        register_49 <= register_4;
        register_12 <= 16'd0;
        program_counter <= register_11;
      end

    endcase
    if (rst == 1'b1) begin
      program_counter <= 0;
    end
  end

endmodule
