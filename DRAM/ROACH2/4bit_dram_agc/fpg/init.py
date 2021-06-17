import corr, time, struct, dram_class
import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


roach_ip = '192.168.0.40'
boffile = 'dram_agc_2.fpg'

#eth parameters
sock_addr = ('10.0.0.29', 1234)    ##your pc address
fpga_addr = ('10.0.0.45', 1234)

#configure settings 
#ref_pow = fix16_14; error_coef = fix16_8
ref_pow = np.array(0.025)#np.array(0.025)	#this is the reference power ie A**2/2
error_coef = np.array(2)


#model paramters
adc_snap = ['adc0a_snap', 'adc0c_snap', 'adc1a_snap']
snap_red = ['adc0a_red', 'adc0c_red', 'adc1a_red']

snap_dtype = '>i1'
nsamples = 128

snap_width = 8
snap_pt = 7


##init roach
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)


#create plot
fig, axes = plt.subplots(*(3,2), squeeze=False)
fig.set_tight_layout(True)

lines = []
for snap, ax in zip(adc_snap, axes[:,0]):
    ax.set_xlim(0, nsamples)
    ax.set_ylim(-128,128)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitud [au]")
    ax.set_title(snap)
    ax.grid()
    line, = ax.plot([],[], animated=True)
    lines.append(line)

for snap, ax in zip(snap_red, axes[:,1]):
    ax.set_xlim(0, nsamples)
    ax.set_ylim(-128,128)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitud [au]")
    ax.set_title(snap)
    ax.grid()
    line, = ax.plot([],[], animated=True)
    lines.append(line)


roach.write_int('control', 1)   #rst

##write reference power and error coeficient (learning rate)
ref_pow_fix = calan.float2fixed(ref_pow, 16,14)
error_coef_fix = calan.float2fixed(error_coef, 16,8)

roach.write_int('ref_pow', ref_pow_fix)
roach.write_int('error_coef', error_coef_fix)
time.sleep(1)

#initialize the dram
print("Initializing DRAM")
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr,fpga_addr=fpga_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()
roach.write_int('control_dram', 5)      ##allow the writing of the dram




#enable triggers and agc
roach.write_int('snap_trig', 1)
roach.write_int('control', 0)
roach.write_int('control', 2)   #enable agc


def animate(_):
    adc_data = calan.read_snapshots(roach,adc_snap, snap_dtype)
    red_data = calan.read_snapshots(roach,snap_red, snap_dtype)
    for i in range(3):
        #lines[i].set_data(range(nsamples), adc_data[0][:nsamples]/2.**snap_pt)
        #lines[i+3].set_data(range(nsamples), red_data[0][:nsamples]/2.**snap_pt)
        lines[i].set_data(range(nsamples), adc_data[i][:nsamples])
        lines[i+3].set_data(range(nsamples), red_data[i][:nsamples])
    gain_0a = roach.read_int('gain_adc0a') 
    gain_0c = roach.read_int('gain_adc0c') 
    gain_1a = roach.read_int('gain_adc1a') 
    print("gain0a:%.4f \t gain0c:%.4f \t gain1a:%.4f"%(gain_0a/2.**7, gain_0c/2.**7,gain_1a/2.**7))
    return lines

ani = FuncAnimation(fig, animate, blit=True)
plt.show()


dump = raw_input('dump the data collected?(y/n)')
if(dump=='y'):
    print("reading dram data")
    roach.write_int('control_dram', 0)  ##dont allow write the dram data
    dram_ring.reading_dram()
    ## The dram class 

dram_ring.close_socket()

