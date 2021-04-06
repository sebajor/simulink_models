import corr, time
import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
from geth_module import config_tge


roach_ip ='192.168.0.40'
boffile = 'spec_tge_1in_acc.fpg'

gain = 1024

#roach = corr.katcp_wrapper.FpgaClient(roach_ip)
#time.sleep(1)
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(2)

roach.write_int('cnt_rst',1)


log_time = 10.*10**-3        ##log time
clk_freq = 150.*10**6        ##
tot_chann = 2.**11/4
acc_len = int(round(log_time/tot_chann*clk_freq))

config_tge(roach)
time.sleep(1)

roach.write_int('acc_len',acc_len)
roach.write_int('cnt_rst',0)


