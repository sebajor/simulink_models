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

chunk = 8192*4*32
iters = 1

secs = []
subsecs = []
for i in range(iters):
    raw_data = f.read(chunk)
    ind = [m.start() for m in re.finditer(start_symbol, raw_data)]
    print(ind)
    for i in range(len(ind)-1):
        ##you could review that ind[i+1]-ind[i]=2048*4*4+64, if this is right
        ##the spectrum is complete
        print(i)
        sec, subsec = struct.unpack('>2I',raw_data[ind[i]-8:ind[i]])
        secs.append(secs); subsecs.append(subsec)
        raw_spec = raw_data[ind[i]+56:ind[i+1]-8]
        dat = np.array(struct.unpack('>'+str(2048*4)+'I',raw_spec))
        dat_ord = dat.reshape([-1,16])
        spec3 = dat_ord[:,:4].flatten()
        spec2 = dat_ord[:,4:8].flatten()
        spec1 = dat_ord[:,8:12].flatten()
        spec0 = dat_ord[:,12:].flatten()


###carefull, in the frb tge we discover that the even and odd data are swapped
##maybe here also happend, if its the case check the code 
##TODO: review that!!

f.close()
freq = np.linspace(0, 600, 2048, endpoint=False)
plt.plot(freq, 10*np.log10(spec0))
plt.show()




