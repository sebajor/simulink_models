import numpy as np
import calandigital as calan
import time
from utils import *
from control import roach_control

roach_ip = '192.168.0.168'
boffile = 'rfi_detection.bof.gz'
rfi_acc = 256
rfi_thresh = 0.6

###
### to work you have to flag the channels with evident rfi
###
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1) 
time.sleep(1)

roach_control = roach_control(roach)

roach_control.set_accumulation(1024)
roach_control.set_snap_trigger()
roach.write_int('rfi_acc_len', rfi_acc)
roach.write_int('threshold', calan.float2fixed(np.array(rfi_thresh),32,13))

roach_control.reset_accumulators()

roach.write_int('rfi_en',1)

##now it should be runnign

