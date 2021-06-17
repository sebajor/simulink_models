set cur_dir [pwd]
puts $cur_dir
set bd_dir $cur_dir/fpga.srcs/sources_1/bd/system

create_bd_design system
###check all!!

#instantite ps
startgroup
    create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7 processing_system7_0
    set_property -dict [list CONFIG.PCW_USE_S_AXI_HP0 {0}] [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_IMPORT_BOARD_PRESET ../ip/red_pitaya.xml] [get_bd_cells processing_system7_0]
endgroup

apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7_0]


#interconnect with 2 slave and one master
startgroup
	create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_0
	set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {2}] [get_bd_cells axi_interconnect_0]
endgroup

#connect clocks
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/processing_system7_0/FCLK_CLK0 (125 MHz)" }  [get_bd_pins axi_interconnect_0/ACLK]
#apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/processing_system7_0/FCLK_CLK0 (125 MHz)" }  [get_bd_pins axi_interconnect_0/M00_ACLK]

#set zynq ps as master
connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axi_interconnect_0/S00_AXI] [get_bd_intf_pins processing_system7_0/M_AXI_GP0]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/processing_system7_0/FCLK_CLK0 (125 MHz)" }  [get_bd_pins axi_interconnect_0/S00_ACLK]


#axi clock
create_bd_port -dir O -type clk axi_clock
startgroup
connect_bd_net [get_bd_ports axi_clock] [get_bd_pins processing_system7_0/FCLK_CLK0]
endgroup


#create axi lite interface 
startgroup
	make_bd_intf_pins_external  [get_bd_intf_pins axi_interconnect_0/M00_AXI]
endgroup

set_property CONFIG.PROTOCOL AXI4LITE [get_bd_intf_ports /M00_AXI_0]
set_property CONFIG.ASSOCIATED_BUSIF {M00_AXI_0} [get_bd_ports /axi_clock]

#insert bram controller
startgroup
    create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.1 axi_bram_ctrl_0
endgroup

set_property -dict [list CONFIG.PROTOCOL {AXI4LITE} CONFIG.SINGLE_PORT_BRAM {1} CONFIG.ECC_TYPE {0}] [get_bd_cells axi_bram_ctrl_0]

#insert memory
startgroup
    create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen:8.4 blk_mem_gen_0
endgroup
set_property -dict [list CONFIG.Memory_Type {True_Dual_Port_RAM} CONFIG.Assume_Synchronous_Clk {true} CONFIG.Enable_B {Use_ENB_Pin} CONFIG.Use_RSTB_Pin {true} CONFIG.Port_B_Clock {100} CONFIG.Port_B_Write_Rate {50} CONFIG.Port_B_Enable_Rate {100}] [get_bd_cells blk_mem_gen_0]

#startgroup
#    set_property -dict [list CONFIG.Enable_32bit_Address {true} CONFIG.Use_Byte_Write_Enable {true} CONFIG.Byte_Size {8} CONFIG.Assume_Synchronous_Clk {true} CONFIG.Register_PortA_Output_of_Memory_Primitives {false} CONFIG.Register_PortB_Output_of_Memory_Primitives {false} CONFIG.Use_RSTA_Pin {true} CONFIG.Use_RSTB_Pin {true} CONFIG.use_bram_block {Stand_Alone} CONFIG.EN_SAFETY_CKT {true}] [get_bd_cells blk_mem_gen_0]
#endgroup


connect_bd_intf_net [get_bd_intf_pins axi_bram_ctrl_0/BRAM_PORTA] [get_bd_intf_pins blk_mem_gen_0/BRAM_PORTA]

startgroup
    apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/processing_system7_0/FCLK_CLK0 (125 MHz)} Clk_slave {Auto} Clk_xbar {/processing_system7_0/FCLK_CLK0 (125 MHz)} Master {/processing_system7_0/M_AXI_GP0} Slave {/axi_bram_ctrl_0/S_AXI} intc_ip {/axi_interconnect_0} master_apm {0}}  [get_bd_intf_pins axi_bram_ctrl_0/S_AXI]
#    apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "Auto" }  [get_bd_intf_pins axi_bram_ctrl_0/BRAM_PORTA]
endgroup

#make one of the ports of the bram external (to be read by the hdl)
startgroup
    make_bd_intf_pins_external  [get_bd_intf_pins blk_mem_gen_0/BRAM_PORTB]
    set_property -dict [list CONFIG.READ_WRITE_MODE {READ_WRITE}] [get_bd_intf_ports BRAM_PORTB_0]
endgroup

apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/processing_system7_0/FCLK_CLK0 (51 MHz)" }  [get_bd_pins axi_interconnect_0/M00_ACLK]

#set address of the axi intf 
assign_bd_address [get_bd_addr_segs {M00_AXI_0/Reg }]
set_property offset 0x41c00000 [get_bd_addr_segs {processing_system7_0/Data/SEG_M00_AXI_0_Reg}]
set_property range 8K [get_bd_addr_segs {processing_system7_0/Data/SEG_M00_AXI_0_Reg}]

#set bram address
set_property offset 0x41100000 [get_bd_addr_segs {processing_system7_0/Data/SEG_axi_bram_ctrl_0_Mem0}]
set_property range 8K [get_bd_addr_segs {processing_system7_0/Data/SEG_M00_AXI_0_Reg}]

#create hdl wrapper
make_wrapper -files [get_files $bd_dir/system.bd] -top
import_files -force -norecurse $bd_dir/hdl/system_wrapper.v



