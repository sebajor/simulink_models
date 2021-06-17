create_project -force -part xc7z010clg400-1  fpga
add_files -fileset sources_1 defines.v
add_files -fileset sources_1 ../rtl/fpga.v
add_files -fileset sources_1 ../rtl/s_axi_lite_reg.v
add_files -fileset sources_1 ../rtl/addr_counter.v
add_files -fileset sources_1 ../rtl/dac_rp.v
add_files -fileset sources_1 ../rtl/true_dual_port_ram.v
add_files -fileset constrs_1 ../fpga.xdc
source ../ip/bd_design.tcl
exit
