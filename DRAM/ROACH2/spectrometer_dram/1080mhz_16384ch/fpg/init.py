import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan


#roach parameters
roach_ip = '192.168.1.14'
boffile = 'spect_dram_14_2.fpg'#'test.fpg'
acc_len = 128


##ring buffer parameters
#direct cable between fpga and pc
sock_addr = ('10.0.0.29', 1234)    ##your pc address 
fpga_addr = ('10.0.0.45', 1234)  
#switch in the middle (remember with the switch yu need to set the ppc via minicom)
#sock_addr = ('192.168.1.40', 1234)    
#fpga_addr = ('192.168.1.3', 1234)

#initialize roach and upload the boffile
#roach = corr.katcp_wrapper.FpgaClient(roach_ip)
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(2)
roach.write_int('fft_gain',2**15-1)


#reset system, create the dram_class object and initialize it
roach.write_int('cnt_rst',1)

print("Initializing DRAM")
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr,fpga_addr=fpga_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()

roach.write_int('control1', 5)      ##allow the writing of the dram
roach.write_int('acc_len',acc_len)

##un-reset the system, ie it start to pass the
##data to the dram 
roach.write_int('cnt_rst',0)  


dump = raw_input('dump the data collected?(y/n)')
if(dump=='y'):
    print("reading dram data")
    roach.write_int('control1', 0)  ##dont allow write the dram data
    dram_ring.reading_dram()
    ## The dram class 

dram_ring.close_socket()

