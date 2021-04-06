import numpy as np
import corr
import time
import struct
import matplotlib.pyplot as plt

roach_ip = '192.168.0.40'
boffile = 'pack_test_hdl.bof.gz'#'pack_test_8.fpg'

fpga = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
fpga.upload_program_bof(boffile, 3000)

time.sleep(1)
fpga.write_int('rst',1)
fpga.write_int('tge_rst',1)

##init tge

source=([192,168,2,3], 1234)
dest=([192,168,2,10], 1234)

dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
port = source[1]
mac_base = (2<<40)+(2<<32)

tx_core='ten_Gbe_v2'

fpga.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)
time.sleep(2)
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',port)

fpga.write_int('pkt_size', 1024)
#fpga.write_int('fft_size', 512)
fpga.write_int('fft_size', 513)
fpga.write_int('idle_cycle', 2**13)

#fpga.write_int('pkt_period', 512*128)#1024)
fpga.write_int('pkt_period', 512*2**14)#1024)

fpga.write_int('rst_bram',2)
fpga.write_int('rst_bram',1)


fpga.write_int('tge_rst',0)
fpga.write_int('rst',0)

fpga.write_int('en_pkt',1)


