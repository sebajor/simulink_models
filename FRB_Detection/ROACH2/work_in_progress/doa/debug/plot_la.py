import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import calandigital as calan

def plot_la(_fpga):
    global fpga,data, freq
    fpga = _fpga
    data = []
    axes = []
    freq = np.arange(2048)#np.linspace(0,600,2048,endpoint=0)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(-2**15, 2**15)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
        axes.append(ax)
    axes[0].set_title('l1')
    axes[1].set_title('l2')
    axes[2].set_title('mu1')
    axes[3].set_title('mu2')
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()


def init():
    for i in range(4):
        data[i].set_data([],[])
    return data


def animate(i):
    r11_brams = ['r11_0','r11_1','r11_2','r11_3']
    r12_brams = ['r12_0','r12_1','r12_2','r12_3']
    r22_brams = ['r22_0','r22_1','r22_2','r22_3']

    r11 = calan.read_interleave_data(fpga, r11_brams, 9, 16, dtype='>u2')
    r22 = calan.read_interleave_data(fpga, r22_brams, 9, 16, dtype='>u2')
    r12 = calan.read_interleave_data(fpga, r12_brams, 9, 16, dtype='>i2')
    r21 = r12

    lamb1 = (r11+r22+np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    lamb2 = (r11+r22-np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    mu1 = 2*np.arctan(-(r11-lamb1)/r12)
    mu2 = 2*np.arctan(-(r11-lamb2)/r12)
    
    ind = np.isnan(mu1)
    mu1[ind] = 0
    ind = np.isnan(mu2)
    mu2[ind] = 0 

    data[0].set_data(freq, lamb1.real)
    data[1].set_data(freq, lamb2.real)
    data[2].set_data(freq, mu1)
    data[3].set_data(freq, mu2)
    return data
