import calandigital as calan
import numpy as np
import sys, time
sys.path.append('codes')
import utils, control

roach_ip = '10.17.89.168'#'192.168.1.18'
boffile = 'arte.fpg'

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach_control = control.roach_control(roach)

#roach.write_int('control_acc_len', 1024)

roach_control.set_accumulation(1024)                    #10bgbe accumulation
roach_control.set_accumulation(1024, thresh=0, num=1)   #dedispersor


roach_control.reset_accumulators()
roach_control.set_snap_trigger()
