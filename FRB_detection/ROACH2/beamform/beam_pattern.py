import time
import serial
import numpy as np
from calandigital.instruments import generator
import control, utils
import corr
import calandigital as calan
import matplotlib.pyplot as plt

###
### Hyperparameters
###
serial_port = '/dev/ttyUSB0'
roach_ip = '192.168.1.12'
gen_info = {'type':'visa',
            'connection': 'TCPIP::192.168.1.39::INSTR',
            'def_freq': 1450,
            'def_power':20
            }
integ_time = 1e-2   ##intergration time
points = 361        ## points for the measurement
step = 1
freq_ind = 1280     ##channel number, 1575
gen_power = 20     ##power of the feed
###
###
###

ser = serial.Serial(serial_port)
gen = generator.create_generator(gen_info)
roach = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)

##configure roach
acc = int(round(integ_time/(2048/4)*150*1e6))
print("acc %i" %acc)
roach_control = control.roach_control(roach)
roach_control.set_snap_trigger()
roach_control.set_accumulation(acc)
roach_control.reset_accumulators()

time.sleep(0.1)
freq = np.linspace(1200,1800,2048, endpoint=False)

gen.set_freq_mhz(freq[freq_ind])
gen.set_power_dbm(gen_power)

###varibles
channel_data = np.zeros(points)
trace_data = np.zeros((2048,points))
snap_data = np.zeros((4, 2048, points))
antennas_data = np.zeros((4,2048, points))

theta = np.linspace(0,points*step-1,points)*np.pi/180
gen.turn_output_on()


##plot variables
plt.ion()
fig = plt.figure()
ax = plt.subplot(111, polar=True)

data, = ax.plot([],[])

##make the first one out of the loop
ser.write("%d\n" %step)
time.sleep(0.5)
beam = utils.get_beam(roach)
antennas = utils.get_antennas(roach)
snaps = roach_control.get_sync_snapshots(['adcsnap0', 'adcsnap1', 'adcsnap2', 'adcsnap3'])
channel_data[0] = beam[freq_ind]
trace_data[:,0] = beam
snap_data[:,:,0] = snaps
antennas_data[:,:,0] = antennas


for i in range(1,points):
    ser.write("%d\n" %step)
    time.sleep(1.5)
    beam = utils.get_beam(roach)
    antennas = utils.get_antennas(roach)
    snaps = roach_control.get_sync_snapshots(['adcsnap0', 'adcsnap1', 'adcsnap2', 'adcsnap3'])
    channel_data[i] = beam[freq_ind]
    trace_data[:,i] = beam
    snap_data[:,:,i] = snaps
    antennas_data[:,:,i] = antennas
    ax.cla()
    ax.plot(theta[:i], 10*np.log10(channel_data[:i]+1)-100)
    fig.canvas.draw()



np.savez('pattern_data.npz',
         theta = theta,
         channel = channel_data,
         trace = trace_data,
         snaps = snap_data,
         antennas = antennas_data
         )
