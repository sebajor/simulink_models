import calandigital as calan
import numpy as np
import time

roach_ip = '192.168.0.40'
boffile = 'autoscale.bof.gz'#.fpg'

mul_val = 2**16

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach.write_int('rst',1)
roach.write_int('en',0)
roach.write_int('rst',0)
roach.write_int('en',1)

time.sleep(0.5)
out_data = calan.read_data(roach, 'out', 8, 16, '>H')

iters = 2**8
x=0
y=iters-1
for i in range(iters):
    gold = np.arctan2(y,x)
    print('gold:%.4f \t fpga:%.4f'%(gold, out_data[i]/2.**13))
    y = y-1
    x= x+1

