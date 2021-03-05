import numpy as np
import calandigital 
import matplotlib.pyplot as plt
import struct
import matplotlib.animation as animation

def plot_snap(_fpga):
    global fpga, data
    fpga = _fpga;
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    ax1.set_ylim(-128,128)
    ax2.set_ylim(-128,128)
    ax3.set_ylim(-128,128)
    ax4.set_ylim(-128,128)
    
    ax1.set_xlim(0,1024*8)
    ax2.set_xlim(0,1024*8)
    ax3.set_xlim(0,1024*8)
    ax4.set_xlim(0,1024*8)

    ax1.grid();ax2.grid();ax3.grid();ax4.grid()

    line1, = ax1.plot([],[])
    line2, = ax2.plot([],[])
    line3, = ax3.plot([],[])
    line4, = ax4.plot([],[])
    data = [line1, line2, line3, line4]
    ani = animation.FuncAnimation(fig, animate,init_func=init, interval=50, blit=True)
    plt.show()

def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    data[2].set_data([],[])
    data[3].set_data([],[])
    return data

def animate(i):
    snap_data = calandigital.read_snapshots(fpga,
            ['adcsnap0','adcsnap1','adcsnap2','adcsnap3'],
            dtype='>8192b')
    xvals = np.arange(8192)
    data[0].set_data(xvals,snap_data[0])
    data[1].set_data(xvals,snap_data[1])
    data[2].set_data(xvals,snap_data[2])
    data[3].set_data(xvals,snap_data[3])
    return data

