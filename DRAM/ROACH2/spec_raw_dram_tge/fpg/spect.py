import numpy as np
import matplotlib.pyplot as plt
import struct, calandigital
import matplotlib.animation as animation

def plot_spect(_fpga):
    global fpga, data, freq
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    


    bw_i=0; bw_e=1080
    freq = np.linspace(bw_i,bw_e, 4096, endpoint=False)

    ax1.set_xlim(bw_i, bw_e)
    y_min=20; y_max=140
    ax1.set_ylim(y_min, y_max)
    ax1.grid()
    ax2.set_xlim(bw_i, bw_e)
    y_min=20; y_max=140
    ax2.set_ylim(y_min, y_max)
    ax2.grid()

    line1, = ax1.plot([],[])
    line2, = ax2.plot([],[])
    data = [line1, line2]
    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=50,blit=True)
    plt.show()

def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data

def animate(i):
    data0 = calandigital.read_interleave_data(fpga, ['dout0_0', 'dout0_1', 'dout0_2',
                                    'dout0_3', 'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7'],
                                    awidth=9, dwidth=64, dtype='>512Q')

    data1 = calandigital.read_interleave_data(fpga, ['dout1_0', 'dout1_1', 'dout1_2',
                                    'dout1_3', 'dout1_4', 'dout1_5', 'dout1_6', 'dout1_7'],
                                    awidth=9, dwidth=64, dtype='>512Q')

    
    data[0].set_data(freq, 10*np.log10(data0+1.))
    data[1].set_data(freq, 10*np.log10(data1+1.))
    return data
    

