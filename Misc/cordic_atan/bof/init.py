import numpy as np
import calandigital as calan
import time, struct

###
### Author: Sebastian Jorquera
###

roach_ip = '192.168.1.18'
boffile = 'cordic_atan.bof.gz'
write_len = 32           ##should write 4*write_len 
seed = 10
thresh = 0.01

###
###
np.random.seed(seed)

roach = calan.initialize_roach(ip=roach_ip, boffile=boffile, upload=1)
time.sleep(0.5)

roach.write_int('rst',1)
roach.write_int('write_len', write_len)

x = (np.random.random(write_len*4)-0.5)*0.1
x_flip = x.reshape([-1,4])[:,::-1].flatten()
x_b = calan.float2fixed(x_flip, 16,15)

y = (np.random.random(write_len*4)-0.5)*0.1
y_flip = y.reshape([-1,4])[:,::-1].flatten()
y_b = calan.float2fixed(y_flip, 16,15)

roach.write('x', x_b.tobytes(),0)
roach.write('y', y_b.tobytes(),0)

roach.write_int('rst',0)
roach.write_int('en',0)
roach.write_int('en',1)
time.sleep(1)

#dout = calan.read_data(roach, 'Shared_BRAM', write_len*4, 16, '>h')
dout = np.frombuffer(roach.read('dout', (write_len)*4*2, 0), '>h')/2.**15
gold = np.arctan2(y,x)/np.pi

assert ((np.abs(gold-dout)<thresh).all()), "Error :("



