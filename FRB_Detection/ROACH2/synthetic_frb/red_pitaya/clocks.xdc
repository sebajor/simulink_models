##check this, I think they come from the bd design
create_clock -period 8.000 -name adc_clk [get_ports adc_clk_p_i]

set_input_delay -clock adc_clk -max 3.400 [get_ports {adc_dat_a_i[*]}]
set_input_delay -clock adc_clk -max 3.400 [get_ports {adc_dat_b_i[*]}]

create_clock -period 4.000 -name rx_clk [get_ports {daisy_p_i[1]}]


#bajo esta linea son contrains que puse yo!

#create_clock -period 4.000 -name clk_out_adc [get_ports {adc_enc_p_o}]
#set_output_delay -clock clk_fpga_1 -max 8. [get_ports {adc_enc_p_o}]  
#set_output_delay -clock clk_fpga_1 -max 8. [get_ports {adc_enc_n_o}]  

set_false_path -from [get_clocks clk_fpga_0] -to [get_clocks adc_clk]
set_false_path -from [get_clocks adc_clk] -to [get_clocks clk_fpga_0]
#set_false_path -from [get_clocks clk_fpga_1] -to [get_clocks adc_clk]
#set_false_path -from [get_clocks adc_clk] -to [get_clocks clk_fpga_1]
