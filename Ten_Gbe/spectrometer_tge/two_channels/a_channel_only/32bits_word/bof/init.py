import calandigital as calan
import time
import numpy as np
###
### Hyperparameters
###

roach_ip = '192.168.1.18'
boffile = 'spectrometer_tge.bof.gz'

source = ([192,168,2,3], 1234)  #source ip, source port
dest = ([192,168,2,10], 1234)   #dest ip, source port
tx_core = 'ten_Gbe_v2'

tge_pkt = 1024
sleep_cycles = 50

fpga_clk = 150.*10**6
acc_time = 10.*10**-3

fft_chnls = 2048    ##fft channels
parallel_out = 4    ##simultaneous fft outputs

gain = 1.0
###
###
###

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1) 
time.sleep(1)

dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
port = source[1]
mac_base = (2<<40)+(2<<32)

#configure the 10Gbe module
roach.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)

roach.write_int('ip', dest_ip)
roach.write_int('port', port)

#configure packetizer
roach.write_int('pkt_len', tge_pkt)
roach.write_int('sleep_cycles', sleep_cycles)


#set acc_len
T = 1./fpga_clk
fft_time = fft_chnls/parallel_out*T     ##time that takes one FFT
acc = acc_time//fft_time

roach.write_int('cnt_rst',1)
roach.write_int('acc_len', acc)
roach.write_int('cnt_rst',0)
#set the gain
#fix_gain = calan.float2fixed(np.array(gain), nbits=32, binpt=15, signed=False)

#start transmission
time.sleep(2)
roach.write_int('en_tge',1)

