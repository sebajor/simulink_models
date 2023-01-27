import time
import serial
import numpy as np
from calandigital.instruments import generator, sva1075x
import matplotlib.pyplot as plt

###
### Hyperparameters
###
serial_port = '/dev/ttyUSB1'
sa_ip = '192.168.1.64'
gen_info = {'type':'visa',
            'connection': 'TCPIP::192.168.1.39::INSTR',
            'def_freq': 1450,
            'def_power':20
            }
integ_time = 1e-2   ##intergration time
points = 361        ## points for the measurement
step = 1
freq_ind = 300     ##channel number, 1575
gen_power = 20     ##power of the feed


res_bw = 3*1e6#1e3#600*1e6/2048
video_bw = 3*1e6#1e2#1./integ_time
pts = 751
span = [1200*1e3,1800*1e3]

###
###
###

ser = serial.Serial(serial_port)
gen = generator.create_generator(gen_info)
sa = sva1075x.sva1075x('TCPIP::'+sa_ip+'::INSTR')

#sa.configure_spectrum(span, pts, res_bw, video_bw)

##configure roach

time.sleep(0.1)
freq = np.linspace(1200,1800,pts, endpoint=False)
gen.set_freq_mhz(freq[freq_ind])
gen.set_power_dbm(gen_power)

###varibles
channel_data = np.zeros(points)
trace_data = np.zeros((751,points))

theta = np.linspace(0,points*step-1,points)*np.pi/180
gen.turn_output_on()

##plot variables
plt.ion()
fig = plt.figure()
ax = plt.subplot(111, polar=True)

data, = ax.plot([],[])
##measure variables

#make the first one out of the loop
ser.write("%d\n" %step)
time.sleep(0.5)
spect = sa.get_spectra()
channel_data[0] = spect[freq_ind]
trace_data[:,0] = spect

for i in range(1,points):
    ser.write("%d\n" %step)
    time.sleep(1.5)
    spect = sa.get_spectra()
    channel_data[i] = spect[freq_ind]
    trace_data[:,i] = spect
    ax.cla()
    ax.plot(theta[:i], channel_data[:i])
    fig.canvas.draw()
    #time.sleep(0.5)
    
gen.turn_output_off()

np.savez('pattern_data_sa.npz',
         theta = theta,
         channel = channel_data,
         trace = trace_data
         )
