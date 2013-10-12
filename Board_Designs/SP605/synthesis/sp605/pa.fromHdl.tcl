
# PlanAhead Launch Script for Pre-Synthesis Floorplanning, created by Project Navigator

create_project -name sp605 -dir "/media/sdb1/Projects/Chips-2.0/Board_Designs/SP605/synthesis/sp605/planAhead_run_1" -part xc6slx45tfgg484-3
set_param project.pinAheadLayout yes
set srcset [get_property srcset [current_run -impl]]
set_property target_constrs_file "SP605.ucf" [current_fileset -constrset]
set hdlfile [add_files [list {../../source/user_design.v}]]
set_property file_type Verilog $hdlfile
set_property library work $hdlfile
set hdlfile [add_files [list {../../source/gigabit_ethernet.vhd}]]
set_property file_type VHDL $hdlfile
set_property library work $hdlfile
set hdlfile [add_files [list {../../source/sp605.vhd}]]
set_property file_type VHDL $hdlfile
set_property library work $hdlfile
set_property top SP605 $srcset
add_files [list {SP605.ucf}] -fileset [get_property constrset [current_run]]
open_rtl_design -part xc6slx45tfgg484-3
