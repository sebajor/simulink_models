import numpy as np
import socket, struct, sys,time
import ipdb

class dram_ring():
    """ 
        Class to control the dram ring buffer for the roach2 of the model
        https://github.com/sebajor/simulink_models/tree/stable/DRAM/ROACH2/spectrometer_dram
        
        The fpga model cascade a dram with a 1Gb/s ethernet. This class enables
        and disable the writing/reading of the dram and also handle the communication
        between the fpga and the computer.

    """
    def __init__(self, fpga, fpga_addr=('10.0.0.45',1234), sock_addr=('10.0.0.29', 1234), tx_core_name = 'one_GbE', pkt_sock = 7920,n_pkt=10):
        """
            fpga:   corr or calandigital object
            fpga_addr: ip_address, port
            sock_ddres: ip_address, port of the computer 
                        (of the interface connected to the roach)
            tx_core_name: Name of the yellow block in the simulink design
            n_pkt: number of packets you send in each burst, the packet length
                    is 8192 so the computer expect 8192*n_pkt before send the 
                    next burst.
        """
        self.fpga = fpga
        self.pkt_sock = pkt_sock#36*220
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sock_addr)

        ##gbe ethernet module parameters
        pkt_size = pkt_sock#36*220-2 should be multiple of 36?
        idle = 25000
        self.n_pkt = n_pkt

        source_ip = fpga_addr[0].rsplit('.')
        dest_ip = sock_addr[0].rsplit('.')  
        source_ip = int(source_ip[0])*2**24+int(source_ip[1])*2**16+int(source_ip[2])*2**8+int(source_ip[3])
        dest_ip = int(dest_ip[0])*2**24+int(dest_ip[1])*2**16+int(dest_ip[2])*2**8+int(dest_ip[3])
        fabric_port = fpga_addr[1] 
        mac_base=(2<<40) + (2<<32)
        
        ##configure ethernet fpga module
        fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
        time.sleep(1)
        fpga.write_int('gbe_dest_ip', dest_ip)
        fpga.write_int('gbe_dest_port', fabric_port)
        
        fpga.write_int('control1',2)
        fpga.write_int('control1',1)
        
        #configure the ring buffer
        fpga.write_int('ring_configuration', 0b101100) #rst everything
        fpga.write_int('ring_pkt_size', (pkt_size-2))
        fpga.write_int('ring_n_pkt', self.n_pkt)
        fpga.write_int('ring_gbe_idle', idle)


    def init_ring(self):
        """
        initialize the dram ring buffer, ie rst counters and stuffs
        """
        self.fpga.write_int('ring_configuration',0)     
        self.fpga.write_int('ring_configuration',1)     ##start writing
        self.fpga.write_int('control1',1)    


    def reading_dram(self, filename='data'):
        """ Reads the ring buffer starting from the address where it stops
        writting.
        For how it was implemented the pc will wait for the n_pkt*8192 bits
        before allowing sending the next packet. This could hung the
        communication if the parameters are not well suited.
        """
        full_bytes = 2.**22*288
        iters = full_bytes/(self.pkt_sock*self.n_pkt)
        iters = int(iters)+1
        f = file(filename, 'wb')            ##CHANGE TO APPEND!!
        start = time.time()
        self.fpga.write_int('ring_configuration', 0b110000)
        self.fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220
        #ipdb.set_trace()
        ##we have 2**25*288/8 bytes of info

        for i in range(iters):#int(762*205/self.n_pkt)):     ##why this number?
            data = ""
            for j in range(self.n_pkt+1):
                data =data+self.sock.recv(int(self.pkt_sock))
            f.write(data[:])
            print(str(i)+"\t "+str(len(data)))
            if(i%50==1):   #direct cable
                time.sleep(0.2)    #direct cable
            #if(i%10==1):   #switch
            #    time.sleep(0.5)     #switch
            self.fpga.write_int('ring_configuration', 0b110000)
            self.fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220 
        end = time.time()
        print("took %.4f secs read dram" %(end-start))
        f.close()
    
    def open_sock(self, sock_addr=('10.0.0.29', 1234)): 
        """ 
        Open the socket that receives the data from the fpga
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sock_addr)

    def close_socket(self):
        """
            Close the socket that receives the data from the fpga
            You need to have the socket closed before opening again.
        """
        self.sock.close()
