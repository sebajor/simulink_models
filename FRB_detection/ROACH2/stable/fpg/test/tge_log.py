import socket 
import sys, os
import time, datetime
import multiprocessing


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
server_address = ('192.168.2.10', 1234)
time_per_file = 30      ##minutes
pkt_size = 2**8*2**10   ##256kB

os.mkdir('log')
os.chdir('log')


sock.bind(server_address)
while(1):
    try:
        filename = str(datetime.datetime.now())
        p = multiprocessing.Process(target=write_data, name="tge", args=(filename, sock, pkt_size, ))
        p.start()
        time.sleep(time_per_file*60)
        p.terminate()
        p.join()
    except:
        print('Fail!')
        p.terminate()
        sock.close()




