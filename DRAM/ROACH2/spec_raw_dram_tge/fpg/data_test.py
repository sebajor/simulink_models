import ctypes, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

lib = ctypes.CDLL('./parse_data2.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None 

f = file('data','rb')

data = f.read(12*2**16)

dat_4raw = lib.parse_data(data, len(data)) 
dat_4char = np.array(struct.unpack(str(len(data)*2)+'B', dat_4raw[0:len(data)*2]))
lib.freeptr(dat_4raw)

##test  ----> reorder the data in the c code!!!
#odd = dat_4char[1::2]
#ev = dat_4char[::2]
#aux = np.vstack([odd, ev])
#dat_4char = aux.T.flatten()

dat4 = dat_4char.reshape(len(dat_4char)/24,24)
dat0 = dat4[:,:8]
dat0_flat = dat0.flatten()
dat1 = dat4[:,8:16]
dat1_flat = dat1.flatten()
dat2 = dat4[:,16:24]
dat2_flat = dat2.flatten()

ind = 0

spect0 = fft(dat0_flat[16384*ind:16384*(ind+1)])
spect1 = fft(dat1_flat[16384*ind:16384*(ind+1)])
spect2 = fft(dat2_flat[16384*ind:16384*(ind+1)])
freq = np.linspace(0,600, 8192, endpoint=False) 

plt.plot(freq, 20*np.log10(np.abs(spect0[:8192]+1)), label='0')
plt.plot(freq, 20*np.log10(np.abs(spect1[:8192]+1)), label='1')
plt.plot(freq, 20*np.log10(np.abs(spect2[:8192]+1)), label='2')

plt.legend()
plt.show()
