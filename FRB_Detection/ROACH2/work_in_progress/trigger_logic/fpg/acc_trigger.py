import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
import matplotlib.patches as mpatches

def plot_frb(_fpga, _theta):
    global data, fpga, stat, theta, ani, legend
    theta = _theta
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    bl_patch = mpatches.Patch(color='blue', label='dedisp')
    or_patch = mpatches.Patch(color='orange', label='sw avg+$ \\alpha \\cdot$std')
    gr_patch = mpatches.Patch(color='green', label='hw avg+$ \\beta \\cdot$var')
    fig.legend(handles=[bl_patch, or_patch, gr_patch],loc='upper left')
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot([],[], lw=2)
    avg1, = ax1.plot([],[], lw=2)
    var1, = ax1.plot([],[], lw=2)
    line2, = ax2.plot([],[], lw=2)
    avg2, = ax2.plot([],[],lw=2)
    var2, = ax2.plot([],[],lw=2)
    data = [line1, line2 ]
    stat = [avg1, avg2, var1,var2]
    ani = data+stat
    ax1.set_title('DM = 100')
    ax2.set_title('DM = 300')
    ax1.set_ylim(0, 40) #check
    ax1.set_xlim(0, 2**10)   #check
    ax1.grid()
    ax2.set_ylim(0, 40) #check
    ax2.set_xlim(0, 2**10)   #check
    ax2.grid()

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    ani[0].set_data([],[])
    ani[1].set_data([],[])
    ani[2].set_data([],[])
    ani[3].set_data([],[])
    ani[4].set_data([],[])
    ani[5].set_data([],[])
    return ani

def animate(i):
    dat1 = np.array(struct.unpack('>1024I', fpga.read('ACC0', 1024*4)))
    dat2 = np.array(struct.unpack('>1024I', fpga.read('ACC1', 1024*4)))
    
    avg0 = np.array(struct.unpack('>1024I', fpga.read('avg0', 1024*4)))
    avg1 = np.array(struct.unpack('>1024I', fpga.read('avg1', 1024*4)))
    var0 = np.array(struct.unpack('>1024I', fpga.read('var0', 1024*4)))
    var1 = np.array(struct.unpack('>1024I', fpga.read('var1', 1024*4)))
    
    hw_thresh0 = np.array(struct.unpack('>1024I', fpga.read('thresh0', 1024*4)))
    hw_thresh1 = np.array(struct.unpack('>1024I', fpga.read('thresh1', 1024*4)))
    
    hw_thresh0 = hw_thresh0/2.**12
    hw_thresh1 = hw_thresh1/2.**12

    dat1 = dat1/2.**13
    dat2 = dat2/2.**13
    
    avg0 = avg0/2.**13
    avg1 = avg1/2.**13
    var0 = np.sqrt(var0/2.**26)
    var1 = np.sqrt(var1/2.**26)
    #avg0 = avg0+var0*theta
    #avg3 = avg3+var3*theta
    
    pow_dat1 = 10*np.log10(dat1+1)
    pow_dat2 = 10*np.log10(dat2+1)
    sw_pow0 = 10*np.log10(avg0+theta*var0+1)
    sw_pow1 = 10*np.log10(avg1+theta*var1+1)
    hw_pow0 = 10*np.log10(hw_thresh0+1)
    hw_pow1 = 10*np.log10(hw_thresh1+1)

    ani[0].set_data(np.arange(2**10), pow_dat1)#dat1)
    ani[1].set_data(np.arange(2**10), pow_dat2)#dat2)
    ani[2].set_data(np.arange(2**10), sw_pow0)#avg0+theta*var0)
    ani[3].set_data(np.arange(2**10), sw_pow1)#avg1+theta*var1)
    ani[4].set_data(np.arange(2**10), hw_pow0)#hw_thresh0)
    ani[5].set_data(np.arange(2**10), hw_pow1)#hw_thresh1)
    
    return ani
