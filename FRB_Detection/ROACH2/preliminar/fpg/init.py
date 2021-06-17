import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt 
import calandigital as calan
import dedisp_config, gps_config
from geth_module import config_tge
from plot_dedisp_pow import plot_dedisp_pow
from test_theta import test_theta

#hyper parameters
#################################################################

roach_ip = '192.168.0.40'#'192.168.1.14'
boffile = 'arte_preliminar.fpg'
gain = 2**2#2**12                    #for requant of the ffts
gain_adc = 2**14                #for requant of the dram ring buffer
#those two gain must be calibrated


DMs = [100, 200, 300, 400]
theta = np.array([5*0.5, 5*0.4, 5*0.3, 5*0.2])
#theta = np.array([5*0.5*100, 5*0.4*100, 5*0.3*100, 5*0.2*100])
offset = np.array([2.5,3,3,3])
#offset = np.array([10,10,10,10])

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


#ring buffer paramters
sock_addr = ('10.0.0.29', 1234)     #ip addr, port


#10Gbe log time 
log_time = 10.*10**-3        ##log time
#the 10Gbe ip addr, sock are 192.168.2.10, 1234, you could modify though..

################################################################
roach = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
try:
    roach.upload_program_bof(boffile, 1000, timeout=10)
    time.sleep(2)
except:
    print("programming roach raise an exception :(")


##configure the DMs and the std coeficient for the dedispersor
dedisp_config.dedisp_config(roach, DMs, theta_fix,off_fix, fcenter=fcenter, bw=bw, nchnls=nchnls)


roach.write_int('cnt_rst',3)    #bit0: rst accumulations, 1:rst the detection flag

#initialize the ringbuffer
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()
roach.write_int('control1', 5)

#initialize gps
gps_config.init_gps(roach)
gps_config.gps_read(roach)     #get the time 

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

