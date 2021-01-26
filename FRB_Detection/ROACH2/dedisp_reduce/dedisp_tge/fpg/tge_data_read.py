import numpy as np
import struct
import re
import matplotlib.pyplot as plt

"""
script to read the 10gbe data from 4 adc with 32 bits per channel
plus an gps timestamp at the begining of the frame
"""

start_symbol = 14*'\xaa\xbb\xcc\xdd'
f = file('udp_data', 'rb')

channels = 2048
chunk = 8192*4*32
frames_chunk = 27   ##frames per chunk, after some playing we arrive to 
                    ##this value
iters = 32
spec0_mat = np.zeros([iters*frames_chunk, channels])
spec1_mat = np.zeros([iters*frames_chunk, channels])

secs = []
subsecs = []
for i in range(iters):
    raw_data = f.read(chunk)
    ind = [m.start() for m in re.finditer(start_symbol, raw_data)]
    #print(ind)
    #for i in range(len(ind)-1):
    for j in range(frames_chunk):
        ##you could review that ind[i+1]-ind[i]=2048*4*4+64, if this is right
        ##the spectrum is complete
        sec, subsec = struct.unpack('>2I',raw_data[ind[j]-8:ind[j]])
        secs.append(sec); subsecs.append(subsec)
        raw_spec = raw_data[ind[j]+56:ind[j+1]-8]
        dat = np.array(struct.unpack('>'+str(2048*4)+'I',raw_spec))
        dat_ord = dat.reshape([-1,16])
        spec3 = dat_ord[:,:4].flatten()
        spec2 = dat_ord[:,4:8].flatten()
        spec1 = dat_ord[:,8:12].flatten()
        spec0 = dat_ord[:,12:].flatten()
        ##found that the even and odd data are swapped
        ##because we send packets of 64 bits so we have 2 word swaped :P
        aux = spec3.reshape([-1,2])
        spec3 = aux[:,::-1].flatten()
        aux = spec2.reshape([-1,2])
        spec2= aux[:,::-1].flatten()
        aux = spec1.reshape([-1,2])
        spec1= aux[:,::-1].flatten()
        aux = spec0.reshape([-1,2])
        spec0= aux[:,::-1].flatten()
        ##the matrix
        spec0_mat[frames_chunk*i+j,:] = spec0 
        spec1_mat[frames_chunk*i+j,:] = spec1

f.close()
#plt.plot(freq, 10*np.log10(spec0))
#plt.show()
t_log = 10.**-2
t = np.arange(frames_chunk*iters)*t_log
frec = np.linspace(1200, 1800, channels ,endpoint=False)
plt.pcolormesh(t,frec, 10*np.log10(spec0_mat+1).T)
plt.show()

