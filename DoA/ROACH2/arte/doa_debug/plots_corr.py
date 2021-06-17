import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_correlation(_fpga, freq=(0,600),  ylim=(-80, 5)):
    global fpga, corr_brams, lines, frequencies
    frequencies = np.linspace(freq[0], freq[1], 2048, endpoint=0)
    corr_brams = ['x12_0', 'x12_1']
    fpga = _fpga
    fig = plt.figure()
    axes = []
    lines = []
    ax = fig.add_subplot(1,1,1)
    ax.grid()
    ax.set_xlabel('MHz')
    ax.set_ylabel('dB')
    ax.set_ylim(ylim)
    ax.set_xlim(freq)
    axes.append(ax)
    line, = ax.plot([],[], lw=2)
    lines.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    lines[0].set_data([],[])
    return lines

def animate(_):
    awidth = 9
    dwidth = 32
    dfactor = 2
    dat0, dat1 = calan.read_deinterleave_data(fpga, corr_brams[0], dfactor=2,
                awidth=9, dwidth=64, dtype='>i4')
    dat2, dat3 = calan.read_deinterleave_data(fpga, corr_brams[1], dfactor=2,
                awidth=9, dwidth=64, dtype='>i4')
    corr1 = np.vstack([dat0,dat1,dat2,dat3]).T
    lines[0].set_data(frequencies, corr1.flatten())
    return lines
