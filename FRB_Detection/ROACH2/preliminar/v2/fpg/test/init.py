import sys 
sys.path.append('..')
sys.path.append('../codes/')
import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt 
import calandigital as calan
import dedisp_config, gps_config
from geth_module import config_tge
from plot_dedisp_pow import plot_dedisp_pow
from test_theta import test_theta
import subprocesss

def runcmd(cmd):
    command = "exec "+cmd
    cmd_proc = subprocess.Popen( cmd, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, shell=1)
    return cmd_proc


roach_ip = '192.168.1.14'
boffile = 'arte_preliminar.fpg'

gain = 2**12
gain_adc = 2**14

DMs = [100, 200, 300, 400]
theta = np.array([5*0.5, 5*0.4, 5*0.3, 5*0.2])
offset = np.array([2.5,3,3,3])

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

#ring buffer
sock_addr = ('10.0.0.29', 1234)

#tge log
log_time = 10.*10**-3

#####init program

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

gps_config.init_gps(roach)
gps_config.gps_read(roach)

#tge parameters
clk_freq = 150.*10**6        ##
tot_chann = 2.**11/4
acc_len = int(round(log_time/tot_chann*clk_freq))
time.sleep(1)
config_tge(roach)       #sets the roach in 192.168.2.3 and the dest is 192.168.2.10

##sync_gen = 4096*9

#start receiving the 10gbe log
print('start receive 10gbe data')
tge_cmd = runcmd('python tge_log.py')
time.sleep(8)

#set gains and accumulation
roach.write_int('gain_adc', gain_adc)
roach.write_int('gain', gain)
roach.write_int('acc_len',acc_len)
roach.write_int('gain_rfi', rfi_gain)
roach.write_int('acc_len_rfi', rfi_acc)

roach.write_int('cnt_rst',0)

print('Taking data :)')

end = raw_input('Finish? y/n')
if(end=='y'):
    tge_cmd.terminate()
else:
    print('The pid of the tge is: '+str(tge_cmd.pid))


