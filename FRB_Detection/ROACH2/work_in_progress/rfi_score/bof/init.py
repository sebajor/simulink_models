import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time

roach_ip = '192.168.0.40'
boffile = 'rfi_test3.bof.gz'
acc = 1024
gain = 2**7

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach.write_int('cnt_rst',1)
roach.write_int('acc_len',acc)
roach.write_int('gain', gain)
roach.write_int('cnt_rst',0)


