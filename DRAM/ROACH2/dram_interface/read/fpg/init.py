import calandigital as calan
import calandigital as calan
import numpy as np
import time

def read_dout(roach, dut_brams, burst_len):
    dout = np.zeros([burst_len,len(dut_brams)])
    for i in range(len(dut_brams)):
        dout[:,i] = calan.read_data(roach, dout_brams[i], 10, 32,'>I')[:burst_len]
    dout = dout.flatten()
    return dout

### Hyperparameters
roach_ip = '192.168.1.168'
boffile = 'read_intf.fpg'

dout_brams = ['dout0','dout1','dout2','dout3','dout4',
             'dout5','dout6','dout7','dout8']
burst_len = 1024
dram_addrs = 2**25

###

roach = calan.initialize_roach(ip=roach_ip, boffile=boffile, upload=1)
time.sleep(1)
roach.write_int('burst_len', burst_len-1)

roach.write_int('write',1)
roach.write_int('write_en',1)

time.sleep(1)

#start reading data
roach.write_int('write_en',0)
roach.write_int('write',0)

time.sleep(1)
roach.write_int('read_en',1)

##read the dram
n_burst = dram_addrs/burst_len
for i in range(n_burst):
    print("%.4f"%(100.*i/n_burst))
    #generate a burst request
    roach.write_int('burst_config', 0)
    roach.write_int('burst_config', 1)
    data = read_dout(roach, dout_brams, burst_len) 
    assert (data == (np.arange(burst_len*9)+i*burst_len*9)).all()


roach.write_int('burst_config', 0)
roach.write_int('burst_config', 1)

data = read_dout(roach, dout_brams, burst_len) 


