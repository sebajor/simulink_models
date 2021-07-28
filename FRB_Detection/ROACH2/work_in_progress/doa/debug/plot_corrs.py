import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import calandigital as calan


def plot_corrs(_fpga):
    global fpga,data, freq
    fpga = _fpga
    data = []
    axes = []
    freq = np.arange(2048)#np.linspace(0,600,2048,endpoint=0)
    fig = plt.figure()
    for i in range(5):
        ax = fig.add_subplot(3,2,i+1)
        ax.set_ylim(0, 2**16-1)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
        axes.append(ax)
    axes[-1].set_ylim(-2**15, 2**15)
    axes[0].set_title('pow0')
    axes[1].set_title('r11')
    axes[2].set_title('pow1')
    axes[3].set_title('r22')
    axes[4].set_title('r12')
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(5):
        data[i].set_data([],[])
    return data

def animate(i):
    spec0_brams = ['dout_0a_0','dout_0a_1','dout_0a_2','dout_0a_3']
    spec1_brams = ['dout_0c_0','dout_0c_1','dout_0c_2','dout_0c_3']
    r11_brams = ['r11_0','r11_1','r11_2','r11_3']
    r12_brams = ['r12_0','r12_1','r12_2','r12_3']
    r22_brams = ['r22_0','r22_1','r22_2','r22_3']

    spec0 = calan.read_interleave_data(fpga, spec0_brams, 9, 64, dtype='>u8')
    spec1 = calan.read_interleave_data(fpga, spec1_brams, 9, 64, dtype='>u8')
    r11 = calan.read_interleave_data(fpga, r11_brams, 9, 16, dtype='>u2')
    r22 = calan.read_interleave_data(fpga, r22_brams, 9, 16, dtype='>u2')
    r12 = calan.read_interleave_data(fpga, r12_brams, 9, 16, dtype='>i2')
    data[0].set_data(freq,spec0)
    data[1].set_data(freq,r11)
    data[2].set_data(freq,spec1)
    data[3].set_data(freq,r22)
    data[4].set_data(freq,r12)
    return data
