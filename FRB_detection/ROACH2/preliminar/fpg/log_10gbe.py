import socket, corr, sys, os
import time, datetime, multiprocessing
import calandigital as calan
import numpy as np
import argparse

def write_10gbe_rawdata(filename, sock, pkt_size):
    """ 
    Function to receive data from the sock socket and write it to a file.
    Is meanted to be forked by a main process that could do other stuffs in
    the meanwhile.
    filename:   File where we the data is saved
    sock    :   Socket where the roach is streaming 
    pkt_size:   size to read in each iteration
    """
    with open(filename, 'ab') as f:
        while(1):
            try:
                while(1):
                    data = sock.recv(pkt_size)
                    f.write(data[:])
            finally:
                f.close()


def receive_10gbe_data(folder, file_time ,ip_addr='192.168.2.10', port=1234):
    

    
