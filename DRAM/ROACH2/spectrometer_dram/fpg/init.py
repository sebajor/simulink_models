import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan


roach_ip = '192.168.0.40'
boffile = 'spec2in.fpg'#'test.fpg'
acc_len = 128


##ring buffer parameters
sock_addr = ('10.0.0.29', 1234)


#roach = corr.katcp_wrapper.FpgaClient(roach_ip)
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(2)

roach.write_int('cnt_rst',1)

print("Initializing DRAM")
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()
roach.write_int('control1', 5)


roach.write_int('acc_len',acc_len)
roach.write_int('cnt_rst',0)


dump = raw_input('dump the data collected?(y/n)')
if(dump=='y'):
    print("reading dram data")
    roach.write_int('control1', 0)
    dram_ring.reading_dram()

dram_ring.close_socket()

