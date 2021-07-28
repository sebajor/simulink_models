import numpy as np
import calandigital as calan
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

boffile='qdr_test2.bof.gz'
roach_ip = '192.168.0.40'

acc_len = 64#128
qdr_period = 2**14*8-1


roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=True)
time.sleep(0.5)

roach.write_int('cnt_rst', 1)

print('Calibrating qdrs')
qdr_name = ['qdr0', 'qdr1', 'qdr2', 'qdr3']
for name in qdr_name:
    print('Calibrating '+name)
    qdr = calan.Qdr(roach, name)
    qdr.qdr_reset()
    qdr.qdr_cal(fail_hard=True, verbosity=0)
    time.sleep(0.2)

print('Finish calbration')
roach.write_int('acc_len', acc_len)
roach.write_int('period', qdr_period)
roach.write_int('en',1)
roach.write_int('cnt_rst',0)

time.sleep(5)

#read spectrum
spect_brams = ['dout0_0', 'dout0_1', 'dout0_2', 'dout0_3',
               'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7']
qdr_brams = ['dat0', 'dat1', 'dat2', 'dat3']

spect = calan.read_interleave_data(roach, spect_brams, 7, 64, '>u8')

qdr_data = np.zeros([4, 2**14*4])
for i in range(qdr_data.shape[0]):
    data = calan.read_data(roach, qdr_brams[i], 16, 16, '>i2')
    qdr_data[i,:] = data


#np.save('qdr_data', qdr_data)
#np.save('spect', spect)


