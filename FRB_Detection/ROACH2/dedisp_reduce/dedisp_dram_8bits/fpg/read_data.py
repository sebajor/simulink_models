import ctypes, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import spectrogram


#lib = ctypes.CDLL('./parse_data.so')

#lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
#lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
#lib.freeptr.argtype = ctypes.c_void_p
#lib.freeptr.restype = None 

#f = file('data_1_chann','rb')
f = file('data', 'rb')
iters = 762
byte_chunk =220*200*36
chunk = byte_chunk/4#220*200*9


fft_size = 2**15
spect0 = np.zeros([iters, fft_size])
#spect1 = np.zeros([iters, fft_size])
#spect2 = np.zeros([iters, fft_size])

for i in range(iters):
    raw_data = f.read(byte_chunk)
    #raw_data = f.read(3*8*fft_size)
    dat = np.array(struct.unpack(str(len(raw_data))+'b', raw_data))
    dat_ = dat.reshape([-1,12])
    dat0 = dat_[:,4:]
    dat0 = dat0[:,::-1]
    dat0_flat = dat0.flatten()
    aux = fft(dat0_flat[0:2*fft_size])
    spect0[i,:] = 20*np.log10(np.abs(aux[:fft_size])+1) 
    f.seek(byte_chunk-3*2*fft_size,1) ##1 is move respect currnt position

f.close()

ts = 1./(150.*10**6)
t_iters = ts*byte_chunk/12   #96/8 = numb of bytes per fpga cycle in the dram

t = np.arange(iters)*t_iters
frec = np.linspace(1200, 1800, fft_size, endpoint=False)
plt.pcolormesh(t[300:],frec[::16], (spect0[300:,::16].T))
plt.show()

    


#ex spectrometer
#frec,t,Sxx = spectrogram(dat2_flat, 1200*10**6)
#plt.pcolormesh(t*10**6,frec/10**6,Sxx)
#plt.show()


