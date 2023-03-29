import multiprocessing, subprocess
import calandigital as calan
import time, socket, os
import numpy as np
import logging, itertools

def search_headers(data, header):
    index = np.argwhere(data==header[0])
    mask = np.zeros(len(index))
    for ind in range(len(index)):
        match = (data[int(index[ind]):int(index[ind]+len(header))] == header).all()
        mask[ind] = match
    return index[mask.astype(bool)]


def review_recv_data(filename, chunk=4*2**14, n_words=512):
    """
    n_words == write_burst (?)
    """
    f = file(filename, 'r')
    size = os.path.getsize(filename)
    header = [0xaabbccdd, 0xaabbccdd,0xaabbccdd,0xaabbccdd]
    for i in range(size//chunk):
        data = np.frombuffer(f.read(chunk), dtype='>I')
        start = search_headers(data, header)
        if(len(start)==0):
            next
        else:
            break
    f.seek(int(start[0]))
    chunk = (n_words*4+4)*4 #header+payload

    for i in range(size//chunk):
        data = np.frombuffer(f.read(chunk), dtype='>I')
        data = data.reshape([-1,2])[:,::-1].flatten() #even and odd numbers are in the wrong order
        if(not (np.array(data[:4] == header).all())):
            return 1
        if(not (np.array(data[4:] == np.arange(n_words*4)).all())):
            return 1
    f.close()
    return 0


def recive_10gbe(filename, sock, pkt_size,run):
    """
    Function to receive data from the sock socket and write it to a file.
    Is meanted to be forked by a main process that could do other stuffs in
    the meanwhile.
    filename:   File where we the data is saved
    sock    :   Socket where the roach is streaming
    pkt_size:   size to read in each iteration
    """
    with open(filename, 'wb') as f:
        while(run.is_set()):
            data = sock.recv(pkt_size)
            f.write(data[:])


def single_test(log,roach_ip, boffile, source,dest,tx_core,tge_pkt,
                read_sleep,write_burst,write_sleep,
                test_time=60, filename='udp_data'):
    """
    roach_ip:   roach ip for the ppc interface
    boffile
    source:     roach 10gbe ip
    dest:       computer ip
    tx_core:    name of the TX core block in simulink
    tge_pkt:    size of the package in multiples of 8bytes
    read_sleep: number of cycles between the roach send another packet
    write_burst: number of samples 
    write_sleep: cycles between two sucessive write_burst

    """
    log.info("Programing FPGA")
    roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1) 
    time.sleep(0.5)
    log.info("Configuring the FPGA model")
    dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
    source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
    port = source[1]
    mac_base = (2<<40)+(2<<32)

    #configure 10GBe module
    roach.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)

    roach.write_int('ip', dest_ip)
    roach.write_int('port', port)

    #configure the packetizer
    roach.write_int('pkt_len', tge_pkt)
    roach.write_int('read_sleep', read_sleep)

    #configure the sample generator 
    roach.write_int('write_burst', write_burst-1)
    roach.write_int('write_sleep', write_sleep)

    #create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_addr = str(dest[0][0])+'.'+str(dest[0][1])+'.'+str(dest[0][2])+'.'+str(dest[0][3])
    port = dest[1]
    sock.bind((ip_addr, port))
    time.sleep(0.5)
    
    #start the process to acquire data
    run = multiprocessing.Event()
    run.set()
    tge_process = multiprocessing.Process(target=recive_10gbe, name="tge", args=(filename, sock, tge_pkt, run,))
    tge_process.start()
    
    #start test
    log.info('Start test')
    roach.write_int('rst',0)
    roach.write_int('en_write', 1)

    time.sleep(test_time)
    #finish the test
    log.info('Finish test')
    run.clear()
    tge_process.join()

    roach.stop()
    sock.close()

    #review the received data
    log.info('Reviewing data')
    error = review_recv_data(filename)
    subprocess.call(['rm', filename])
    if(error):
        log.warning('tge_pkt {:}, read_sleep {:}, write_burst {:}, write_sleep {:}'.format(
                tge_pkt,read_sleep,write_burst,write_sleep))
    return error


if __name__ == '__main__':
    ###
    ### Hyper parameters
    ###
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    
    ##file handler
    #fh = logging.FileHandler('test.log', mode='w', encoding='utf-8')
    #fh.setLevel(logging.DEBUG)
    #fh.setFormatter(formatter)
    #log.addHandler(fh)

    ##stream display
    #formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    subprocess.call('./init_tge.sh')
    roach_ip = '192.168.1.18'
    boffile = 'packet_test.bof.gz'

    source = ([192,168,2,3], 1234)  #source ip, source port
    dest = ([192,168,2,10], 1234)   #dest ip, source port
    tx_core = 'ten_Gbe_v2'

    #values to test
    tge_pkt = [1024]
    read_sleep = np.arange(100,1000,100)#[100]

    write_burst = [512]
    write_sleep = [512*512]

    fpga_clk = 150*1e6
    test_time = 30

    ###
    ###create iterators
    ###
    read_iter = list(itertools.product(tge_pkt, read_sleep))
    write_iter = list(itertools.product(write_burst, write_sleep))
    errors = []
    for read in read_iter:
        for write in write_iter:
            error = single_test(log,roach_ip, boffile, source,dest,tx_core,read[0],
                            read[1],write[0],write[1],
                            test_time=test_time, filename='udp_data')
            if(error):
                errors.append([read, write])
    print('Errors:')
    for error in errors:
        print('tge pkt:{:} \t read sleep: {:} \t write burst: {:} \t write sleep: {:}'.format(error[0][0], error[0][1], error[1][0], error[1][1]))





       

