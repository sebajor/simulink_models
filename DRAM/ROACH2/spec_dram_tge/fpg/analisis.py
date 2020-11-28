import numpy as np
import matplotlib.pyplot as plt
import struct


f = file('data', 'rb')

total_size = 2**20*2000#574#311  ##311MB
chunk = 8192*8*1024*4

print(total_size/chunk)
for i in range(total_size/chunk):
    raw_data = f.read(chunk)
    dat = np.array(struct.unpack('>'+str(chunk/8)+'Q', raw_data))
    dat_ord = dat.reshape([-1,16])
    spec0 = dat_ord[:,:8]
    spec1 = dat_ord[:,8:16]
    #spec0_flat = spec0[:,::-1].flatten()
    #spec1_flat = spec1[:,::-1].flatten()
    spec0_mat = spec0[:,::-1].reshape([-1,4096])
    spec1_mat = spec1[:,::-1].reshape([-1,4096])
    plt.imshow(10*np.log10(spec0_mat))
    plt.show()
    plt.imshow(10*np.log10(spec1_mat))
    plt.show()



f.close()
plt.imshow(10*np.log10(spec0_mat))
plt.show()
plt.imshow(10*np.log10(spec1_mat))
plt.show()

freq = np.linspace(0,1080, 4096, endpoint=False)



