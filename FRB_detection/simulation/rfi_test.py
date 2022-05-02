import numpy as np
import h5py
import matplotlib.pyplot as plt

###
### Author: Sebastian Jorquera
### We collect the complex output of the FFTs for the arte project in using the
### fft log model and with that data we made simulation to validate our algorithms
### and to make the best usage of the bit representation 
###

acc_len = 64


freq = np.linspace(1200, 1800,2048, endpoint=0)

f = h5py.File('tone.hdf5', 'r')
adc0 = np.array(f['adc0'])
adc1 = np.array(f['adc1'])
adc2 = np.array(f['adc2'])
adc3 = np.array(f['adc3'])

beam = adc0+adc1
pow_data = (beam*np.conj(beam))*(adc3*np.conj(adc3))
corr_data = beam*np.conj(adc3)

### We accumulate the power and the complex of the correlation between the 
### synth and the reference antenna.
pow_mean = np.mean(pow_data[:,:acc_len], axis=1)
corr_mean = np.mean(corr_data[:,:acc_len], axis=1)

corr_pow = corr_mean*np.conj(corr_mean)

score = corr_pow.real/pow_mean.real
approx = np.arctan2(corr_pow.real, pow_mean.real)

plt.plot(freq,score, label='gold')
plt.plot(freq, approx, label='atan')
plt.grid()
plt.ylabel('Score')
plt.xlabel('MHz')
plt.title('RFI score')
plt.legend()
plt.show()









