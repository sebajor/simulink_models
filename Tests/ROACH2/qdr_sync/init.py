import numpy as np
import calandigital as calan
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

boffile='qdr_sync.bof.gz'
roach_ip = '192.168.0.40'

qdr_period = 2**14*8-1
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=True)
time.sleep(0.5)

roach.write_int('cnt_rst', 1)
print('Calibrating qdr0')
qdr = calan.Qdr(roach, 'qdr0')
qdr.qdr_reset()
qdr.qdr_cal(fail_hard=True, verbosity=0)
time.sleep(0.2)

roach.write_int('period', qdr_period)
roach.write_int('en',1)
roach.write_int('cnt_rst',0)

time.sleep(3)
qdr_data = calan.read_data(roach, 'dat0', 16, 16, '>i2')
qdr_first = calan.read_data(roach, 'dat1', 18, 16, '>i2')

qdr_din = calan.read_data(roach, 'dat2', 10, 32, '>i4')

np.savetxt('qdr_data', qdr_data)
np.savetxt('qdr_first', qdr_first)
np.savetxt('qdr_din', qdr_din)

