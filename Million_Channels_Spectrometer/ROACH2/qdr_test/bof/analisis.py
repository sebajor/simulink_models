import numpy as np
import matplotlib.pyplot as plt


spect = np.load('spect.npy')
qdr_data  = np.load('qdr_data.npy')

freq = np.linspace(0, 1080, 1024)

aux = qdr_data[0,:].reshape([-1,4])
val0 = aux[:,0]+1j*aux[:,1]
val1 = aux[:,2]+1j*aux[:,3]

val0 = val0.reshape([-1,128])
val1 = val1.reshape([-1,128])

aux = qdr_data[1,:].reshape([-1,4])
val2 = aux[:,0]+1j*aux[:,1]
val3 = aux[:,2]+1j*aux[:,3]

val2 = val2.reshape([-1,128])
val3 = val3.reshape([-1,128])

aux = qdr_data[2,:].reshape([-1,4])
val4 = aux[:,0]+1j*aux[:,1]
val5 = aux[:,2]+1j*aux[:,3]

val4 = val4.reshape([-1,128])
val5 = val5.reshape([-1,128])

aux = qdr_data[3,:].reshape([-1,4])
val6 = aux[:,0]+1j*aux[:,1]
val7 = aux[:,2]+1j*aux[:,3]

val6 = val6.reshape([-1,128])
val7 = val7.reshape([-1,128])

mat = np.zeros([1024,128], dtype=complex)

for i in range(1024/8):
    mat[8*i,:]   = val0[i,:]
    mat[8*i+1,:] = val1[i,:]
    mat[8*i+2,:] = val2[i,:]
    mat[8*i+3,:] = val3[i,:]
    mat[8*i+4,:] = val4[i,:]
    mat[8*i+5,:] = val5[i,:]
    mat[8*i+6,:] = val6[i,:]
    mat[8*i+7,:] = val7[i,:]


for i in range(64):
    plt.plot(freq,10*np.log10(np.abs(mat[:,i])+1))

plt.show()





