import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb


def plot_frb(_fpga, theta):
    global data, fpga
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    line1, = ax1.plot([],[], lw=2)
    line2, = ax2.plot([],[], lw=2)
    line3, = ax3.plot([],[], lw=2)
    line4, = ax4.plot([],[], lw=2)
    data = [line1, line2, line3, line4]
    ax1.set_title('DM = 100')
    ax2.set_title('DM = 200')
    ax3.set_title('DM = 300')
    ax4.set_title('DM = 400')
    ax1.set_ylim(30, 70) #check
    ax1.set_xlim(0, 2**10)   #check
    ax1.grid()
    ax1.axhline(theta[0], color='red')
    ax2.axhline(theta[1], color='red')
    ax3.axhline(theta[2], color='red')
    ax4.axhline(theta[3], color='red')
    ax2.set_ylim(30, 70) #check
    ax2.set_xlim(0, 2**10)   #check
    ax2.grid()
    ax3.set_ylim(30, 70) #check
    ax3.set_xlim(0, 2**10)   #check
    ax3.grid()
    ax4.set_ylim(30, 70) #check
    ax4.set_xlim(0, 2**10)   #check
    ax4.grid()
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    data[2].set_data([],[])
    data[3].set_data([],[])
    return data

def animate(i):
    dat1 = np.array(struct.unpack('>1024I', fpga.read('ACC0', 1024*4)))
    dat2 = np.array(struct.unpack('>1024I', fpga.read('ACC1', 1024*4)))
    dat3 = np.array(struct.unpack('>1024I', fpga.read('ACC2', 1024*4)))
    dat4 = np.array(struct.unpack('>1024I', fpga.read('ACC3', 1024*4)))
    pow_dat1 = 10*np.log10(dat1+1)
    pow_dat2 = 10*np.log10(dat2+1)
    pow_dat3 = 10*np.log10(dat3+1)
    pow_dat4 = 10*np.log10(dat4+1)
    data[0].set_data(np.arange(2**10), pow_dat1)
    data[1].set_data(np.arange(2**10), pow_dat2)
    data[2].set_data(np.arange(2**10), pow_dat3)
    data[3].set_data(np.arange(2**10), pow_dat4)
    return data 
