import numpy as np
import matplotlib.pyplot as plt


spect = np.load('spect.npy')
dat  = np.load('qdr_data.npy')

aux = qdr_data[0,:].reshape([-1,4])
val0 = aux[:,0]+1j*aux[:,1]
val1 = aux[:,2]+1j*aux[:,3]

val0 = val0.reshape([-1,64])
val1 = val1.reshape([-1,64])

aux = qdr_data[1,:].reshape([-1,4])
val2 = aux[:,0]+1j*aux[:,1]
val3 = aux[:,2]+1j*aux[:,3]

val2 = val2.reshape([-1,64])
val3 = val3.reshape([-1,64])

aux = qdr_data[2,:].reshape([-1,4])
val4 = aux[:,0]+1j*aux[:,1]
val5 = aux[:,2]+1j*aux[:,3]

val4 = val4.reshape([-1,64])
val5 = val5.reshape([-1,64])

aux = qdr_data[3,:].reshape([-1,4])
val6 = aux[:,0]+1j*aux[:,1]
val7 = aux[:,2]+1j*aux[:,3]

val6 = val6.reshape([-1,64])
val7 = val7.reshape([-1,64])

mat = np.zeros([64,64])

for i in range(64):






