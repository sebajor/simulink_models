import calandigital as calan
import numpy as np
from numpy.linalg import eigh
import matplotlib.pyplot as plt
import socket, telnetlib, time,os
import ipdb

###
### Author: Sebastian Jorquera
###

def upload_code(roach_ip, filename, _sleep_time=0.2):
    tn = telnetlib.Telnet(roach_ip)
    time.sleep(_sleep_time)
    tn.read_very_eager()
    tn.write('root\n')
    time.sleep(_sleep_time)
    tn.write('cd /var/tmp \n')
    time.sleep(_sleep_time)
    tn.read_very_eager()
    #ipdb.set_trace()
    tn.write('nc -l -p 1234 > '+filename+'\n')
    time.sleep(_sleep_time)
    os.system('nc -w 3 '+roach_ip+' 1234 < '+filename)
    time.sleep(1)
    tn.read_very_eager()
    tn.write('find . -name '+filename+'\n')
    time.sleep(_sleep_time)
    ans = tn.read_very_eager()
    time.sleep(_sleep_time)
    tn.write('chmod +x '+filename+'\n')
    time.sleep(_sleep_time)
    tn.close()
    return ans.find(filename)
    
    
def run_code(code_name='uesprit_la', _sleep_time=0.2):
    tn = telnetlib.Telnet(roach_ip)
    time.sleep(_sleep_time)
    tn.read_very_eager()
    tn.write('root\n')
    time.sleep(_sleep_time)
    tn.write('cd /var/tmp \n')
    time.sleep(_sleep_time)
    tn.read_very_eager()
    tn.write('busybox nohup ./'+codename+' &\n') 
    time.sleep(_sleep_time)
    tn.read_very_eager()
    time.sleep(1)
    #tn.close()
    #for some reason if you close the connection the code stop
    #send data 
    return tn
    
def kill_process(tn, code_name='uesprit_la', _sleep_time=0.2):
    tn.read_very_eager()
    tn.write('busybox pgrep '+code_name+' \n')
    time.sleep(_sleep_time)
    pid = tn.read_very_eager()
    time.sleep(_sleep_time)
    ind1 = pid.find('\n')
    ind2 = pid.find('\n')
    #ipdb.set_trace()
    pid = pid[ind1+1:ind1+ind2]
    print(pid)
    tn.write('kill '+pid+' \n')
    time.sleep(_sleep_time)
    
    

roach_ip = '192.168.1.18'
boffile = '../eigen_test.bof.gz'
pc_ip = '192.168.1.100'
port = 4567

struct_size = 4+4+16*4+12*8 
pkt_len = 9*struct_size

###
### The struct is:
###     -4bytes of header (int)             : 0xAABBCCDD
###     -4bytes numbe of sources(int)       : d
###     -16*4bytes eigenvalues (16 float)   : 
###     -12*8bytes doa  (12*2 floats)       : real, imag
###

filename = 'data'
codename = 'uesprit_la'

n = 16
seed = 10
read_size = n*(n+1)/2
iters = 100

##initialize the FPGA
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach.write_int('rst',1)
roach.write_int('seed', seed)
roach.write_int('read_size', read_size)

roach.write_int('rst',0)

roach.write_int('en',1)
time.sleep(1)

#upload code
print('uploading code')
upload_code(roach_ip, codename)

#create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((pc_ip, port))
f = open(filename, 'wb')

time.sleep(0.5)
tn = run_code(codename)
print('runing')
for i in range(iters):
    print(i)
    raw_data = sock.recv(pkt_len)
    f.write(raw_data[:])
    data = np.frombuffer(raw_data, '>f')
    frame = data.reshape([-1,42]) 
    header = frame[:,0]
    sources = frame[:,1]
    eigval = frame[:,2:18]
    doa_re = frame[:,18::2]
    doa_im = frame[:,19::2]
f.close()
sock.close()
kill_process(tn)
tn.close()

