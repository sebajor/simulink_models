import corr, time, numpy, struct, sys,socket
import matplotlib.pyplot as plt


#pkt_period = 8192#100  #in FPGA clocks (200MHz) la cague
#payload_len = 40#50   #in 64bit words
pkt_size = 36*220-2
idle = 100
n_pkt = 200




#gen_rate = 1.*payload_len/pkt_period*135
#tge_rate = gen_rate/(8./10*156.25)*10
#print('data rate: %.2f GSa/s' %(tge_rate))

dest_ip = 10*(2**24) + 0*(2**16) + 0*(2**8)+29 #192*(2**24) + 168*(2**16) + 1*(2**8)+29
fabric_port=1234

source_ip= 10*(2**24) + 0*(2**16) + 0*(2**8)+45 #192*(2**24) + 168*(2**16) + 1*(2**8)+45 #10.0.0.20



tx_core_name = 'one_GbE'
mac_base=(2<<40) + (2<<32)

fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'pack_gbe.bof.gz'

fpga.upload_program_bof(bof,3000)
time.sleep(1)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
time.sleep(1)

fpga.write_int('en',2)
fpga.write_int('n_pkt', n_pkt)
fpga.write_int('idle', idle)
fpga.write_int('pkt_size', pkt_size)
fpga.write_int('dest_ip', dest_ip)
fpga.write_int('dest_port', fabric_port)
fpga.write_int('en',0)
fpga.write_int('en',8)
fpga.write_int('en',12)
fpga.write_int('en',5)




