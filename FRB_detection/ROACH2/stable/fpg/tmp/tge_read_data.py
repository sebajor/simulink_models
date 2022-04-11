import numpy as np
import struct, re
import matplotlib.pyplot as plt


filename = 'udp_data'

##########################################################3
start_symbol = 6*'\xaa\xbb\xcc\xdd'
f = file(filename, 'rb')

channels = 2048
chunk = (2048*4*4+64)*33*8  #?
frames_chunk = 33*8-1

iters = 1
spec_mat = np.zeros([iters*frames_chunk, channels])

secs = []
subsecs = []

freq = np.linspace(0, 600, 2048, endpoint=0)

for i in range(iters):
    raw_data = f.read(chunk)
    ind = [m.start() for m in re.finditer(start_symbol, raw_data)]
    for j in range(frames_chunk):
        sec, subsec = struct.unpack('>2I',raw_data[ind[j]-8:ind[j]])
        secs.append(sec); subsecs.append(subsec)
        raw_spec = raw_data[ind[j]+24:ind[j+1]-8]
        dat = np.array(struct.unpack('>'+str(2048)+'Q',raw_spec))
        spec = dat.reshape([-1,4]) 
        spec = spec[:,::-1].flatten()
        spec_mat[frames_chunk*i+j,:] = spec

f.close()
