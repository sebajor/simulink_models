import numpy as np
import calandigital as calan
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

boffile = 'qdr_ct4.bof.gz'
roach_ip = '192.168.0.40'

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=True)
time.sleep(0.5)

qdr_name = ['qdr0', 'qdr1', 'qdr2', 'qdr3']

roach.write_int('qdr_en', 2)
time.sleep(0.5)

for name in qdr_name:
    print('Calibrating '+name)
    qdr = calan.Qdr(roach, name)
    qdr.qdr_reset()
    qdr.qdr_cal(fail_hard=True, verbosity=0)
    time.sleep(0.2)

roach.write_int('qdr_en', 2)
time.sleep(0.5)
roach.write_int('qdr_en', 1)

time.sleep(5)
#read the transposed data

#qdr0
brams = ['transpose', 'transpose2', 'transpose3', 'transpose4']
for i in range(4):
    print('Check QDR'+str(i))
    dat = calan.read_data(roach, brams[i], 16, 32, '>u4')
    dat_mat = dat.reshape([-1, 256])
    x_check = np.diff(dat_mat, axis=1)
    x_val = np.sum((x_check!=256))
    print('xval: '+str(x_val))
    y_check = np.diff(dat_mat, axis=0)
    y_val = np.sum(y_check!=1)
    print('xval: '+str(y_val))

dat = calan.read_data(roach, 'transpose', 16, 32, '>u4')
dat1 = calan.read_data(roach, 'transpose2', 16, 32, '>u4')
dat2 = calan.read_data(roach, 'transpose3', 16, 32, '>u4')
dat3 = calan.read_data(roach, 'transpose4', 16, 32, '>u4')

qdr0 = dat.reshape([-1,256])
qdr1 = dat.reshape([-1,256])
qdr2 = dat.reshape([-1,256])
qdr3 = dat.reshape([-1,256])



