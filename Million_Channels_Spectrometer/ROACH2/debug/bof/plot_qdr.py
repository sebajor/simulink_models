import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct, corr
import calandigital as calan
import ipdb


parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")

def get_matrix(fpga):
    fftchan = 256
    ct = 128
    addr = 8-3+7 #log2(fftchan)-3+log2(ct)
    qdr_brams = ['dat0', 'dat1', 'dat2', 'dat3']
    mat = []
    #ipdb.set_trace()
    for i in range(4):
        dat = calan.read_data(fpga, qdr_brams[i], addr+1, 64, '>u8').reshape([-1,2])
        dat0 = dat[:,0]
        dat0 = dat0.reshape([-1,ct])
        dat1 = dat[:,1]
        dat1 = dat1.reshape([-1,ct])
        mat.append(dat0)
        mat.append(dat1)
    mat = np.hstack(mat)
    mat = mat.reshape([fftchan, ct])
    return mat




def plot_qdr(_fpga,  _freq=[0, 1080]):
    global fpga, data, freq1, freq2
    fpga = _fpga
    data = []
    y_lim = (0, 100)
    freq1 = np.linspace(_freq[0], _freq[1], 256, endpoint=False)
    freq2 = np.linspace(_freq[0], _freq[1], 256*128, endpoint=False)
    fig = plt.figure()
    axes = []
    for i in range(2):
        ax = fig.add_subplot(1,2,i+1)
        axes.append(ax)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq1[0], freq1[-1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
    axes[0].set_title('Normal')
    axes[1].set_title('Extended')
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

    spect = calan.read_interleave_data(fpga, spect_brams, 5, 64, '>u8')
    mat = get_matrix(fpga)
    data[0].set_data(freq1, 10*np.log10(spect+1))
    data[1].set_data(freq2, 10*np.log10(mat.flatten()+1))
    return data
    """
    fft_size = 256
    stream = 256/8
    transpose = 128
    #mat = np.zeros([transpose, fft_size], dtype=complex)
    mat = []
    #ipdb.set_trace()
    for i in range(4):
        dat = calan.read_data(roach, qdr_brams[i], 14, 16, '>i2').reshape([-1,4])
        dat0 = dat[:,0]+1j*dat[:,1]
        dat0 = dat0.reshape([-1,transpose])
        dat1 = dat[:,0]+1j*dat[:,1]
        dat1 = dat1.reshape([-1,transpose])
        mat.append(dat0)
        mat.append(dat1)
    data[0].set_data(freq, 10*np.log10(spect))
    mat = np.hstack(mat)
    mat = mat.reshape([fft_size, transpose])
    #data[1].set_data(freq, 20*np.log10(np.sum(np.abs(mat), axis=1)))
    data[1].set_data(freq, 20*np.log10(np.abs(mat[:,20])+1))
    return data
    """


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

        

        
        




