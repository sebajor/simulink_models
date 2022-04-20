import socket, corr
import sys, os
import time, datetime
import multiprocessing
import ipdb
import calandigital as calan
import numpy as np

def write_data(filename, sock, pkt_size):
    with open(filename, 'ab') as f:
        while(1):
            try:
                while(1):
                    data = sock.recv(pkt_size)
                    f.write(data[:])
            finally:
                f.close()

##address, port
roach_ip = '192.168.1.18'
roach = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(2)
detect_count =0
server_address = ('192.168.2.10', 1234)
time_per_file = 2      ##minutes
pkt_size = 2**8*2**10   ##256kB

os.mkdir('log')
os.chdir('log')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

corr_bram = ['corr0', 'corr1', 'corr2', 'corr3'] #64
spec_bram = ['mul0', 'mul1', 'mul2', 'mul3']
dtypes = ['>u4', '>u4', '>u4']
bitsize = [32, 32,32]

config = 'data/cfg1_'
os.mkdir('data')
#filenames = ['spect_mult.txt', 'cross.txt', 'score.txt' ,'time.txt']
filenames = ['score.txt' ,'time.txt']




f = file('detections','w')
cycle=0
while(1):
    try:
        filename = str(datetime.datetime.now())
        p = multiprocessing.Process(target=write_data, name="tge", args=(filename, sock, pkt_size, ))
        p.start()
        start = time.time()
        while(1):
            date = datetime.datetime.now()
            #det = roach.read_int('frb_detector')
            #corr_vals = calan.read_interleave_data(roach, corr_bram, 9, 32, '>u4')
            #spec = calan.read_interleave_data(roach, spec_bram, 9, 32, '>u4')
            #rfi_rank = calan.read_data(roach, 'rfi', 11, 16, '>h')/2.**12#/2.**13
            #t = [date.hour, date.minute, date.second, date.microsecond]
            #data_array = [spec, corr_vals, rfi_rank, t]
            #data_array = [rfi_rank, t]
            #for filename, data in zip(filenames, data_array):
                #fr = open(config+filename, 'ab')
                #np.savetxt(fr, [data])
                #fr.close()
            #if(det!=0):
                #f.write(str(date)+"\n")
                #detect_count +=1
                #roach.write_int('cnt_rst',2)
                #roach.write_int('cnt_rst',0)
            ex_time = time.time()-start
            if(ex_time>(time_per_file*60)):
                break
        p.terminate()
        p.join()
        cycle +=1
        print('cycle: '+str(cycle))
        print('detections: '+str(detect_count))
    except:
        print('Fail!')
        print('detections: '+str(detect_count))
        p.terminate()
        sock.close()
        f.close()
        break

"""
    ipdb.set_trace()
    try:
        filename = str(datetime.datetime.now())
        p = multiprocessing.Process(target=write_data, name="tge", args=(filename, sock, pkt_size, ))
        p.start()
        start = time.time()
        while(1):
            date = datetime.datetime.now()
            det = roach.read_int('frb_detector')
            corr_vals = calan.read_interleave_data(roach, corr_bram, 9, 32, '>u4')
            spec = calan.read_interleave_data(roach, spec_bram, 9, 32, '>u4')
            rfi_rank = calan.read_data(roach, 'rfi', 11, 16, '>h')/2.**12#/2.**13
            data_array = [spec, corr_vals, rfi_rank, date]
            for filename, data in zip(filenames, data_array):
                fr = open(config+filename, 'ab')
                np.savetxt(f, [data])
                fr.close()
            if(det!=0):
                f.write(str(date)+"\n")
                detect_count +=1
                roach.write_int('cnt_rst',2)
                roach.write_int('cnt_rst',0)
            ex_time = time.time()-start
            if(ex_time>(time_per_file*60)):
                break
        #time.sleep(time_per_file*60)
        p.terminate()
        p.join()
        cycle +=1
        print('cycle: '+str(cycle))
        print('detections: '+str(detect_count))
    except:
        print('Fail!')
        print('detections: '+str(detect_count))
        p.terminate()
        sock.close()
        f.close()
        break
"""



