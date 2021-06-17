import numpy as np
import calandigital as calan


def plot_correlation(_fpga, freq=(0,600),  ylim=(-80, 5)):
    global fpga, corr_brams, lines, frequencies
    frequencies = np.linspace(freq[0], freq[1], 2048, endpoint=0)
    corr_brams = [['x12_0', 'x12_1'], ['y12_0', 'y12_1']]
    fpga = _fpga
    fig = plt.figure()
    axes = []
    lines = []
    for i in range(2):
        ax = fig.add_subplot(1,2,i)
        ax.grid()
        ax.set_xlabel('MHz')
        ax.set_ylabel('dB')
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        axes.append(ax)
        line, = ax.plot([],[], lw=2)
        lines.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(2):
        lines[i].set_data([],[])
    return lines

def animate(_):
    awidth = 9
    dwidth = 32
    dfactor = 2
    for i in range(2):
        dat0, dat1 = calan.read_deinterleave_data(fpga, corr_brams[i][0], dfactor=2,
                awidth=9, dwidth=32, dtype='>4i')
        dat2, dat3 = calan.read_deinterleave_data(fpga, corr_brams[i][1], dfactor=2,
                awidth=9, dwidth=32, dtype='>4i')
        corr1 = np.hstack([dat0,dat1,dat2,dat3])
        lines[i].set_data(frequencies, 10*np.log10(corr1))
    return lines
