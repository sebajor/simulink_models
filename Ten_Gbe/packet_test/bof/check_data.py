#!/usr/bin/env python2
import numpy as np
import struct, os

def search_headers(data, header):
    index = np.argwhere(data==header[0])
    mask = np.zeros(len(index))
    for ind in range(len(index)):
        match = (data[int(index[ind]):int(index[ind]+len(header))] == header).all()
        mask[ind] = match
    return index[mask.astype(bool)]



filename = 'udp_data'
size = os.path.getsize(filename)
f = file(filename, 'r')
chunk = 4*2**14          ##we will read 16384 words per iter

n_words = 512           #this is without the header

#here we write 32bits words

##search for the starting header
header = [0xaabbccdd, 0xaabbccdd,0xaabbccdd,0xaabbccdd]
for i in range(size//chunk):
    data = np.frombuffer(f.read(chunk), dtype='>I')
    start = search_headers(data, header)
    if(len(start)==0):
        next
    else:
        break

f.seek(int(start[0]))
chunk = (n_words*4+4)*4   #header +payload
for i in range(size//chunk):
    data = np.frombuffer(f.read(chunk), dtype='>I')
    data = data.reshape([-1,2])[:,::-1].flatten()   ##even and odd numbers are in the wrong order 
    assert np.array(data[:4] == header).all()
    assert np.array(data[4:] == np.arange(n_words*4)).all()
     
print('All looks good :)') 
