import numpy as np
import corr, struct, time
import matplotlib.pyplot as plt
from plot_snapshots import plot_snap
from plot_spectrum import plot_spect
import dram_class

roach_ip = '192.168.0.40'
bof = 'dram_spect_tge.fpg'

##10Gbe parameters
dest_ip = 192*(2**24)+168*(2**16)+2*(2**8)+10   #pc ip
source_ip = 192*(2**24)+168*(2**16)+2*(2**8)+3  #roach ip
fabric_port = 1234
mac_base = (2<<40)+(2<<32)
tx_core_name = 'ten_Gbe_v2'


##sys params..
acc = 2**12#2000
idle_cycle = 64
pkt_size = 1024-4
pkt_period = 512*acc

fpga = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
fpga.upload_program_bof(bof, 3000)
time.sleep(2)

fpga.write_int('acc_len',1)

plot_snap(fpga)
plot_spect(fpga)


##intialize 10Gbe
time.sleep(1)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)
fpga.write_int('cnt_rst',1)

fpga.write_int('tge_pack_pkt_size', pkt_size) ##change the name of the ssubsys!!!!
fpga.write_int('tge_pack_idle_cycle', idle_cycle)

time.sleep(1)
fpga.write_int('acc_len', acc)

##set up dram
dram_ring = dram_class.dram_ring(fpga)
time.sleep(1)
dram_ring.init_ring()

##start
fpga.write_int('cnt_rst',0)


time.sleep(10)
fpga.write_int('control',0)
print("reading dram")

dram_ring.reading_dram()

dram_ring.close_socket()











