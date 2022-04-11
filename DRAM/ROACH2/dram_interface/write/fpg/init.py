import calandigital as calan
import numpy as np
import time

### Hyperparameters
roach_ip = '192.168.1.168'
boffile = 'write_intf.fpg'

dout_regs = ['dout0','dout1','dout2','dout3','dout4',
             'dout5','dout6','dout7','dout8']

#np.random.seed(23)
samples = 100
###

roach = calan.initialize_roach(ip=roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach.write_int('write',1)
roach.write_int('write_en',1)

time.sleep(1)

#start reading data
roach.write_int('write',0)

index = np.random.randint(2**25, size=samples)
index = np.hstack([index, 2**25-1])

for ind in index:
    gold = ind*9+np.arange(9)
    roach.write_int('addr', ind)
    for dout_reg, gold_data in zip(dout_regs, gold):
        dout = roach.read_int(dout_reg)
        print("fpga:%i \t gold:%i" %(dout, gold_data))
        assert (dout==gold_data)

print('Everything looks right! :)')

