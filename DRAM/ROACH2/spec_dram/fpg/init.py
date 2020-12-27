import numpy as np
import corr, struct, time
import matplotlib.pyplot as plt
from plot_snapshots import plot_snap
from plot_spectrum import plot_spect
import dram_class

roach_ip = '192.168.1.14'
bof = 'spect_dram.fpg'


fpga = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)

fpga.upload_program_bof(bof,3000)
time.sleep(2)

fpga.write_int('cnt_rst',1)
fpga.write_int('acc_len', 128)
fpga.write_int('cnt_rst',0)

plot_snap(fpga)
plot_spect(fpga)

"""
dram_ring = dram_class.dram_ring(fpga)
time.sleep(1)
dram_ring.init_ring()
time.sleep(1)
fpga.write_int('control',0) ##this should be done in hardware! jus add an or at 
                            ##at the input to stop the writing and look for the
                            ##flag to start the reading!
dram_ring.reading_dram()

"""


