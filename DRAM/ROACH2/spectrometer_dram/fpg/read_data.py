import struct
import numpy as np
import matplotlib.pyplot as plt


f = file('data','rb')
iters = 762
fft_chunk = 18*4*1024
n_ffts = 1024
bw = 1080

count = []
spect_mat = np.zeros([8192,n_ffts])

freq = np.linspace(0, 1080, 8192, endpoint=0)


for i in range(n_ffts):
    raw_data = f.read(fft_chunk)
    dat = np.array(struct.unpack(str(fft_chunk/4)+'I', raw_data))
    dat_ord = dat.reshape([-1,9])
    count.append(dat_ord[:,8])
    dat_chan = dat_ord[:,:8].flatten().reshape([-1,2])
    spect = dat_chan[:,0]+(dat_chan[:,1].astype(np.uint64)<<32)
    spect_mat[:,i] = spect



plt.plot(freq, 10*np.log10(spect+1))
plt.show()




