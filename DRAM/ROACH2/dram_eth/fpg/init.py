import corr, time, struct, sys
import numpy as np
import matplotlib.pyplot as plt
import socket

##initialize socket
pkt_sock = 36*220
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.0.0.29', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
f = open('data', 'wb')


##gbe parameters
pkt_size = 36*220-2
idle =25000#20000
n_pkt = 10

dest_ip = 10*(2**24) + 0*(2**16) + 0*(2**8)+29 #192*(2**24) + 168*(2**16) + 1*(2**8)+29
fabric_port=1234
source_ip= 10*(2**24) + 0*(2**16) + 0*(2**8)+45 #192*(2**24) + 168*(2**16) + 1*(2**8)+45 #10.0.0.20

tx_core_name = 'one_GbE'
mac_base=(2<<40) + (2<<32)

##connect and upload model
fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'dram_eth3.fpg'#'dram_eth2.fpg'#'dram_eth.fpg'

fpga.upload_program_bof(bof,3000)
time.sleep(1)

##initialize parameters
## write_read: write, read, rst, rst_read, gbe_auto, rst_pkt
##

fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
time.sleep(1)
fpga.write_int('write_read', 0b101100) #rst everything
fpga.write_int('n_pkt', n_pkt)

fpga.write_int('gbe_dest_ip', dest_ip)
fpga.write_int('gbe_dest_port', fabric_port)
fpga.write_int('rst_brams',1); fpga.write_int('rst_brams',0)

fpga.write_int('gbe_idle', idle)
fpga.write_int('gbe_pkt_size', pkt_size)

fpga.write_int('write_read',0)
fpga.write_int('write_read', 1) #writing
time.sleep(1)
start = time.time()
#fpga.write_int('write_read', 0b10000)
#fpga.write_int('write_read', 0b10010) #read 1 burst of 220 

#time.sleep(0.5)
#data = sock.recv(pkt_sock)


time.sleep(0.2)
fpga.write_int('write_read', 0b110000)
fpga.write_int('write_read', 0b010010) #read 1 burst of 220 
"""
for i in range(n_pkt+1):
    print(i)
    data = sock.recv(pkt_sock)
    f.write(data[:])
"""

#read whole dram
#takes 3 minutes!
for i in range(762*20):
    data = ""
    for j in range(n_pkt+1):
        data =data+sock.recv(pkt_sock)
    f.write(data[:])
    print(str(i)+"\t "+str(len(data)))
    if(i%50==1):
        time.sleep(0.2)
    fpga.write_int('write_read', 0b110000)
    fpga.write_int('write_read', 0b010010) #read 1 burst of 220 
    #if(i%30==1):
        #time.sleep(1)
end = time.time()
print("took %.4f secs read dram" %(end-start))


sock.close()
f.close()


