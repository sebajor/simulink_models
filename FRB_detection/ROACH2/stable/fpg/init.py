import sys
sys.path.append('codes/')

import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt 
import calandigital as calan
import dedisp_config, gps_config
from geth_module import config_tge
from plot_dedisp_pow import plot_dedisp_pow
from test_theta import test_theta
from flag_channels import flag_channels

#hyper parameters
#################################################################

roach_ip ='192.168.1.168'#'10.17.89.168'#168'#'192.168.1.14'
boffile = 'arte_preliminar2.fpg'

gain = 1#2**12       #2**2 receiver   #for requant of the ffts
gain_adc = 2**14                    #for requant of the dram ring buffer

#rfi ranking parameters
rfi_gain = 2**9
rfi_acc = 1024

##vals for 5std with the receiver on:
## DM:100   theta:2.5   off:0.2
## DM:200, 300, 400 works good with those too
##for 3std  theta:2.5   off:0.1

DMs = [100, 200, 300, 400]


##threshold = avg + theta*var+ offset
theta = np.array([5*0.5, 5*0.4, 5*0.3, 5*0.2])
#theta = np.array([5*0.5*100, 5*0.4*100, 5*0.3*100, 5*0.2*100])
#offset = np.array([2.5,3,3,3])
offset = np.array([1.1,1.1,1.1,1.1])

theta_fix = calan.float2fixed(theta, 32, 12, signed=0)
off_fix = calan.float2fixed(offset, 32,13,signed=0)

adc_bits = 8
bw = 600.
fcenter = 1500
nchnls = 2048
count_reg = 'cnt_rst'
bram_list = ["ACC0", "ACC1", "ACC2", "ACC3"]
thresh_brams = ["thresh0", "thresh1", "thresh2", "thresh3"]

acc_addr_width = 10
acc_word_width = 32
acc_data_type = '>u4'


##flag parameters
flags = np.arange(71).tolist()
flags = flags+[1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024,
               1025, 1026, 1027, 1028, 1029, 1030]

rfi_thresh = 0.9    #if some channel cross this threshold dont allow detection
rfi_thresh_fix = calan.float2fixed(np.array([rfi_thresh]), 16,13)
rfi_count = 2**12   #the not allowing lapse this cycles


#ring buffer paramters
sock_addr = ('10.0.0.29', 1234)     #your ip addr, port
                                    #by default the roach has the ip 10.0.0.45

#10Gbe log time 
log_time = 10.*10**-3        ##log time
#the 10Gbe ip addr, sock are 192.168.2.10, 1234, you could modify though..

################################################################
roach = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
try:
    roach.upload_program_bof(boffile, 3000, timeout=10)
    #time.sleep(2)
except:
    print("programming roach raise an exception :(")

time.sleep(5)
##configure the DMs and the std coeficient for the dedispersor
dedisp_config.dedisp_config(roach, DMs, theta_fix,off_fix, fcenter=fcenter, bw=bw, nchnls=nchnls)


roach.write_int('cnt_rst',3)    #bit0: rst accumulations, 1:rst the detection flag
"""
#initialize the ringbuffer
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()
roach.write_int('control1', 5)
"""
#initialize gps
gps_config.init_gps(roach)
gps_config.gps_read(roach)     #get the time 

#flag channels
flag_channels(roach, flags)

#rfi parameters
roach.write_int('rfi_thresh', 2**31+rfi_thresh_fix)
roach.write_int('rfi_thresh', 2**30+rfi_count)

#tge parameters
clk_freq = 150.*10**6        ##
tot_chann = 2.**11/4
acc_len = int(round(log_time/tot_chann*clk_freq))
time.sleep(1)
config_tge(roach)       #sets the roach in 192.168.2.3 and the dest is 192.168.2.10


#set gains and accumulation
roach.write_int('gain_adc', gain_adc)
roach.write_int('gain', gain)
roach.write_int('acc_len',acc_len)
roach.write_int('gain_rfi', rfi_gain)
roach.write_int('acc_len_rfi', rfi_acc)

roach.write_int('cnt_rst',0)


#plot dedispersed power and statistics
plot_dedisp_pow(roach, DMs, bram_list, thresh_brams)

#dump data the collected data in the dram ringbuffer
dump = raw_input('dump the data collected?(y/n)')
if(dump=='y'):
    print("reading dram data")
    roach.write_int('control1', 0)
    dram_ring.reading_dram()

dram_ring.close_socket()

