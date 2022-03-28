import corr, time
import calandigital as calan
import socket, threading, os
from itertools import cycle
import numpy as np

###
### Hyperparameters
###
roach_ip = '192.168.1.168'
boffile = 'pack_test.bof.gz'

source = ([10,0,0,3], 1234)  #source ip, source port
dest = ([10,0,0,9], 1234)   #dest ip, source port
tx_core = 'one_GbE'

gbe_pkt = 128
read_sleep = 512

write_burst = 512
write_sleep = 512*1024

fpga_clk = 100.*10**6

filename = 'data'  ##temporary file where we save the incoming data

recv_time = 20          ##time that we are running the rec process

###
###
###

def receive_packet(pkt_size, dest_ip, dest_port, filename='data'):
    global stop_thread
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((dest_ip, dest_port))
    f = open(filename, 'wb')
    while(1):
        try:
            if(stop_thread):
                break
            while(1):
                if(stop_thread):
                    break
                data = sock.recv(pkt_size)
                f.write(data[:])
        except:
            pass
    print('Thread stopped')
    f.close()
    sock.close()

roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
port = source[1]
mac_base = (2<<40)+(2<<32)

#configure 1Gbe module
roach.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)

roach.write_int('ip', dest_ip)
roach.write_int('port', port)

#configure packetizer
roach.write_int('pkt_len', gbe_pkt-1)
roach.write_int('sleep_cycles', read_sleep-1)

#configure the sample generator
roach.write_int('burst_len', write_burst-1)
roach.write_int('sleep_write', write_sleep)

#call a thread to receive the data
print('Start reception process')
stop_thread = False
ip_str = str(dest[0][0])+'.'+str(dest[0][1])+'.'+str(dest[0][2])+'.'+str(dest[0][3])
worker = threading.Thread(target=receive_packet, args=(gbe_pkt*8, ip_str, 
                port, filename))

worker.start()
time.sleep(1)

#start test
print('start transmission')

roach.write_int('rst',0)
roach.write_int('en', 1)

time.sleep(recv_time)
print('stop reception')
stop_thread = True


###
### review the received data
###
print('Reviewing the received data')
gold = np.arange(write_burst*16)%256
gold = np.hstack(([ 0xdd,0xdd,0xdd,0xdd,
                        0xdd,0xdd,0xdd,0xdd,
                        0xdd,0xdd,0xdd,0xdd,
                        0xdd,0xdd,0xdd,0xdd], gold.flatten()))
size = os.path.getsize(filename)
chunks = (write_burst+1)*16
f = open(filename, 'rb')

for i in range(size//chunks):
    data = np.frombuffer(f.read(chunks), 'B')
    assert (data == gold).all()

f.close()
print('All looks good')
os.system('rm '+filename)
