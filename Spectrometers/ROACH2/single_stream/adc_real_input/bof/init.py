import calandigital as calan
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot_specs(_fpga, _freq=[0, 150]):
    global fpga, data, freq
    fpga = _fpga
    y_lim = (0, 200)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    for i in range(2):
        ax = fig.add_subplot(1,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(_freq[0], _freq[1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(2):
        data[i].set_data([],[])
    return data

def animate(i):
    ##for real input
    chan0 = calan.read_data(roach, 'dout_0a_0',11,64, '>u8')
    chan1 = calan.read_data(roach, 'dout_0a_1',11,64, '>u8')
    ##check, this is for complex input, we have real only data
    spec0 = chan0[:1024]
    spec1 = chan1[:1024]
    """
    spec0 = np.zeros(2048)
    spec1 = np.zeros(2048)
    for i in range(1024):
        spec0[2*i] = chan0[i]
        spec0[2*i+1] = chan0[2047-i]
        spec1[2*i] = chan1[i]
        spec1[2*i+1] = chan1[2047-i]
    """
    data[0].set_data(freq[:1024], 10*np.log10(spec0+1))
    data[1].set_data(freq[:1024], 10*np.log10(spec1+1))
    return data

if __name__ == '__main__':
    roach_ip = '192.168.0.40'
    boffile = 'complex_dft.bof.gz'
    roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
    roach.write_int('cnt_rst',1)
    roach.write_int('acc_len', 1024)
    roach.write_int('shift', 2047)
    roach.write_int('cnt_rst',0)
    plot_specs(roach)



