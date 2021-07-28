import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct, corr
import calandigital as calan


parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")

def plot_qdr(_fpga,  _freq=[0, 1080]):
    global fpga, data, freq
    fpga = _fpga
    data = []
    y_lim = (0, 100)
    freq = np.linspace(_freq[0], _freq[1], 1024, endpoint=False)
    fig = plt.figure()
    for i in range(2):
        ax = fig.add_subplot(1,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
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
    spect_brams = ['dout0_0', 'dout0_1', 'dout0_2', 'dout0_3',
               'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7']
    qdr_brams = ['dat0', 'dat1', 'dat2', 'dat3']

    spect = calan.read_interleave_data(fpga, spect_brams, 7, 64, '>u8')
    mat = np.zeros([128, 1024], dtype=complex)
    for i in range(4):
        dat = calan.read_data(roach, qdr_brams[i], 16, 16, '>i2').reshape([-1,4])
        dat0 = dat[:,0]+1j*dat[:,1]
        dat0 = dat0.reshape([-1,128])
        dat1 = dat[:,0]+1j*dat[:,1]
        dat1 = dat1.reshape([-1,128])
        mat[:, 128*2*i:128*2*i+128] = dat0
        mat[:, 128*2*i+128:128*2*(i+1)] = dat1
    data[0].set_data(freq, 10*np.log10(spect))
    mat = mat.reshape([1024, 128])
    #data[1].set_data(freq, 20*np.log10(np.sum(np.abs(mat), axis=1)))
    data[1].set_data(freq, 20*np.log10(np.abs(mat[:,10])+1))
    return data

if __name__ == '__main__':
    args = parser.parse_args()
    roach = corr.katcp_wrapper.FpgaClient(args.ip)
    #roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=0)
    plot_qdr(roach)


"""
    data = calan.read_data(roach, qdr_brams[0], 14, 16, '>i2').reshape([-1,4])
    dat0 = data[:,0]+1j*data[:,1]
    dat1 = data[:,0]+1j*data[:,1]
    data = calan.read_data(roach, qdr_brams[1], 14, 16, '>i2').reshape([-1,4])
    dat2 = data[:,0]+1j*data[:,1]
    dat3 = data[:,0]+1j*data[:,1]
    data = calan.read_data(roach, qdr_brams[2], 14, 16, '>i2').reshape([-1,4])
    dat4 = data[:,0]+1j*data[:,1]
    dat5 = data[:,0]+1j*data[:,1]
    data = calan.read_data(roach, qdr_brams[3], 14, 16, '>i2').reshape([-1,4])
    dat6 = data[:,0]+1j*data[:,1]
    dat7 = data[:,0]+1j*data[:,1]
"""

        

        
        




