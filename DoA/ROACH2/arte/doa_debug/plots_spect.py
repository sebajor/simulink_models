import numpy as np
import struct
import calandigital as calan
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plots(_fpga, freq=(0, 600), ylim=(-80, 5)):
    global fpga, lines, pow_brams, autocor_bram, frequencies
    frequencies = np.linspace(freq[0], freq[1], 2048, endpoint=0)
    pow_brams = [['dout_0a_0', 'dout_0a_1', 'dout_0a_2', 'dout_0a_3'],
                 ['dout_0c_0', 'dout_0c_1', 'dout_0c_2', 'dout_0c_3']]
    autocor_bram = [['x11_0', 'x11_1'], ['x22_0', 'x22_1']]
    fpga = _fpga
    fig = plt.figure()
    axes = []
    lines = []
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.grid()
        ax.set_xlabel('MHz')
        ax.set_ylabel('dB')
        ax.set_ylim(ylim)
        ax.set_xlim(freq)
        axes.append(ax)
        line, = ax.plot([],[], lw=2)
        lines.append(line)
    axes[0].set_title('ADC0 power')
    axes[1].set_title('R11')
    axes[2].set_title('ADC1 power')
    axes[3].set_title('R22')
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(4):
        lines[i].set_data([],[])
    return lines

def animate(_):
    awidth = 9
    dwidth = 64
    for i in range(2):
        spect_data = calan.read_interleave_data(fpga, pow_brams[i], awidth,dwidth,
                dtype='>i8')
        #maybe I have to scale it!
        lines[2*i].set_data(frequencies, 10*np.log10(spect_data+1))
    #check!
    dat0, dat1 = calan.read_deinterleave_data(fpga, bram=autocor_bram[i][0], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    dat2, dat3 = calan.read_deinterleave_data(fpga, autocor_bram[i][1], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    
    corr1 = np.vstack([dat0,dat1,dat2,dat3]).T
    lines[1].set_data(frequencies, 10*np.log10(corr1.flatten()+1))
    dat0, dat1 = calan.read_deinterleave_data(fpga, autocor_bram[1][0], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    dat2, dat3 = calan.read_deinterleave_data(fpga, autocor_bram[1][1], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    corr1 = np.vstack([dat0,dat1,dat2,dat3]).T
    lines[3].set_data(frequencies, 10*np.log10(corr1.flatten()+1))
    return lines
    
    
