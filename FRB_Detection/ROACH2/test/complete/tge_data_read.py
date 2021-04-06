import numpy as np
import struct
import re
import matplotlib.pyplot as plt


"""
script to read 10gbe log data from the synthesized beam
plus a gps timestamp at the begining of the frame
"""

start_symbol = 6*'\xaa\xbb\xcc\xdd'
f = file('udp_data', 'rb')

channels = 2048
chunk = (2048*4*4+64)*33*8#8192*4*32
frames_chunk = 33*8-1   ##frames per chunk, after some playing we arrive to 
                    ##this value

##the whole spectrum+start symbol+clock data= 2048*8+256/8 bytes so its a way
##to check if the data is corrupted

iters = 1
spec0_mat = np.zeros([iters*frames_chunk, channels])
f.seek(chunk*63)
secs = []
subsecs = []
