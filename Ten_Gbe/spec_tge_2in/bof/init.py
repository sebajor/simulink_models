import numpy as np
import matplotlib.pyplot as plt
import corr, struct, time
from spect import plot_spect

roach_ip = '192.168.0.40'
bof ='spec_tge.bof.gz'

dest_ip = 192*(2**24)+168*(2**16)+2*(2**8)+10   #pc ip
source_ip = 192*(2**24)+168*(2**16)+2*(2**8)+3  #roach ip
fabric_port = 1234
mac_base = (2<<40)+(2<<32)
tx_core_name = 'ten_Gbe_v2'


acc = 2**12#2000
idle_cycle = 64
pkt_size = 1024-4
pkt_period = 512*acc

fpga = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
fpga.upload_program_bof(bof, 3000)

time.sleep(1)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)


fpga.write_int('cnt_rst',1)
#fpga.write_int('Subsystem_pkt_size', pkt_size) ##change the name of the ssubsys!!!!
#fpga.write_int('Subsystem_idle_cycle', idle_cycle)

fpga.write_int('geth_pack_pkt_size', pkt_size) ##change the name of the ssubsys!!!!
fpga.write_int('geth_pack_idle_cycle', idle_cycle)



fpga.write_int('acc_len', acc)

###prepare the pc to receive the data from the tge!!!

fpga.write_int('cnt_rst',0) ##we should set this to zero when we are ready to save the data

plot_spect(fpga)

freq = np.linspace(0,1080, 4096, endpoint=False)

fpga.write_int('cnt_rst',1)



