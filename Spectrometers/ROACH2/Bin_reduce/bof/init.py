import corr
import numpy as np
import matplotlib.pyplot as plt
import time 
from plot2 import plot_spect

IP = '192.168.0.40'
bof = 'spec.bof.gz'
fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(1) 


fpga.write_int('cnt_rst',1)
fpga.write_int('acc_len', 1024)
fpga.write_int('cnt_rst',0)

plot_spect(fpga, 1080)
