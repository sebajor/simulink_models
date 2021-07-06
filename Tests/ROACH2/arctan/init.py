import calandigital as calan
import numpy as np
import time

roach_ip = '192.168.0.40'
boffile = 'arctan.bof.gz'#.fpg'

iters = 100
np.random.seed(10)

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

y = np.random.random(iters)
x = np.random.random(iters)
gold = np.arctan2(y,x)

y_fix = calan.float2fixed(y, 32, 30)
x_fix = calan.float2fixed(x, 32, 30)
roach.write_int('en',1)
for i in range(iters):
    roach.write_int('x', x_fix[i])
    roach.write_int('y', y_fix[i])
    out = roach.read_int('out')/2.**12
    print("gold: %.4f \t fpga:%.4f" %(gold[i], out))
