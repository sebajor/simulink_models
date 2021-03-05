import numpy as np
import matplotlib.pyplot as plt
import struct, calandigital
import matplotlib.animation as animation

def plot_spect(_fpga):
    global fpga,data,freq
    fpga = _fpga
    fig = plt.figure()
    ax1=fig.add_subplot(221); ax2=fig.add_subplot(222);
    ax3=fig.add_subplot(223); ax4=fig.add_subplot(224);
    
    bw_i=0; bw_e=600
    ax1.set_xlim(bw_i,bw_e);ax2.set_xlim(bw_i,bw_e);
    ax3.set_xlim(bw_i,bw_e);ax4.set_xlim(bw_i,bw_e);
    freq = np.linspace(bw_i, bw_e, 2048, endpoint=False)

    #check parameters!
    y_min =20; y_max = 140
    ax1.set_ylim(y_min,y_max);ax2.set_ylim(y_min,y_max);
    ax3.set_ylim(y_min,y_max);ax4.set_ylim(y_min,y_max);
    
    ax1.grid();ax2.grid();ax3.grid();ax4.grid()

    line1, = ax1.plot([],[])
    line2, = ax2.plot([],[])
    line3, = ax3.plot([],[])
    line4, = ax4.plot([],[])

    data = [line1,line2,line3,line4]
    ani = animation.FuncAnimation(fig, animate,init_func=init, interval=50, blit=True)
    plt.show()

def init():
    data[0].set_data([],[]);data[1].set_data([],[]);
    data[2].set_data([],[]);data[3].set_data([],[]);
    return data

def animate(i):
    spec0 = calandigital.read_interleave_data(fpga,
           ['dout_0a_0','dout_0a_1','dout_0a_2','dout_0a_3'],
           awidth=9, dwidth=64, dtype='>512Q')
    spec1 = calandigital.read_interleave_data(fpga,
           ['dout_0c_0','dout_0c_1','dout_0c_2','dout_0c_3'],
           awidth=9, dwidth=64, dtype='>512Q')
    spec2 = calandigital.read_interleave_data(fpga,
           ['dout_1a_0','dout_1a_1','dout_1a_2','dout_1a_3'],
           awidth=9, dwidth=64, dtype='>512Q')
    spec3 = calandigital.read_interleave_data(fpga,
           ['dout_1c_0','dout_1c_1','dout_1c_2','dout_1c_3'],
           awidth=9, dwidth=64, dtype='>512Q')

    data[0].set_data(freq,10*np.log10(spec0+1)); data[1].set_data(freq,10*np.log10(spec1+1))
    data[2].set_data(freq,10*np.log10(spec2+1)); data[3].set_data(freq,10*np.log10(spec3+1))

    return data
    









