import numpy as np
import calandigital as calan



def plot_eigval(_fpga):
    global data, fpga
    fpga = _fpga
    fig = plt.figure()
    data = []
    for i in range(2):
        ax = fig.add_subplot(1,2,i)
        ax.set_title("eigenvalue:"+str(i+1))
        ax.grid()
        ax.set_xlim(0, 2048)
        ax.set_ylim(-1,1)
        line, = ax.plot([],[], lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()


def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data


def animate(i):
    l1_0, l2_0 = calan.read_deinterleave_data(fpga, 'l0', 2, 9, 32, '>i2')
    l1_1, l2_1 = calan.read_deinterleave_data(fpga, 'l1', 2, 9, 32, '>i2')
    l1_2, l2_2 = calan.read_deinterleave_data(fpga, 'l2', 2, 9, 32, '>i2')
    l1_3, l2_3 = calan.read_deinterleave_data(fpga, 'l3', 2, 9, 32, '>i2')
    l1 = np.vstack([l1_0,l1_1,l1_2,l1_3]).reshape((-1,), order='F')
    l2 = np.vstack([l2_0,l2_1,l2_2,l2_3]).reshape((-1,), order='F')
    data[0].set_data(range(len(l1)), l1)
    data[1].set_data(range(len(l1)), l2)
    return data
