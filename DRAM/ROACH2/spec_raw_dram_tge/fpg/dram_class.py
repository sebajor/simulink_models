import numpy as np
import socket, struct, sys,time

class dram_ring():

    def __init__(self, fpga, fpga_addr=('10.0.0.45',1234), sock_addr=('10.0.0.29', 1234), tx_core_name = 'one_GbE'):
        """sock address = (gbe ip address, port)
        """
        self.fpga = fpga
        self.pkt_sock = 36*220
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sock_addr)

        ##gbe ethernet module parameters
        pkt_size = 36*220-2
        idle = 25000
        self.n_pkt = 10

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
        
        fpga.write_int('control',2)
        fpga.write_int('control',1)
        
        #configure the ring buffer
        fpga.write_int('ring_configuration', 0b101100) #rst everything
        fpga.write_int('ring_n_pkt', self.n_pkt)
        fpga.write_int('ring_gbe_idle', idle)


    def init_ring(self):
        self.fpga.write_int('ring_configuration',0)     
        self.fpga.write_int('ring_configuration',1)     ##start writing
        self.fpga.write_int('control',1)    


    def reading_dram(self, filename='data'):
        f = file(filename, 'wb')            ##CHANGE TO APPEND!!
        start = time.time()
        self.fpga.write_int('ring_configuration', 0b110000)
        self.fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220
        for i in range(762*20):
            data = ""
            for j in range(self.n_pkt+1):
                data =data+self.sock.recv(self.pkt_sock)
            f.write(data[:])
            print(str(i)+"\t "+str(len(data)))
            if(i%50==1):
                time.sleep(0.2)
            self.fpga.write_int('ring_configuration', 0b110000)
            self.fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220 
    #if(i%30==1):
        #time.sleep(1)
        end = time.time()
        print("took %.4f secs read dram" %(end-start))
        f.close()
    
    def open_sock(self, sock_addr=('10.0.0.29', 1234)): 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(sock_addr)

    def close_socket(self):
        self.sock.close()
