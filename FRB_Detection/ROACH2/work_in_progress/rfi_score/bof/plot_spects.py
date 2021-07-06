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
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")
parser.add_argument("-a", "--acc", dest="acc", help="accumulation value")

def plot_spects(_fpga, _acc, _freq=[0, 600]):
    global fpga, data, freq, dBFS, acc
    dBFS = 8*6.02+10*np.log10(2048)
    acc = _acc
    fpga =_fpga
    y_lim = (-80, 0)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        ax.set_title("adc "+str(i))
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(4):
        data[i].set_data([],[])
    return data

def animate(i):
    spec0_bram = ['dout_0a_0', 'dout_0a_1','dout_0a_2','dout_0a_3'] #64
    spec1_bram = ['dout_0c_0', 'dout_0c_1','dout_0c_2','dout_0c_3'] #32
    spec2_bram = ['dout_1a_0', 'dout_1a_1','dout_1a_2','dout_1a_3'] #32
    spec3_bram = ['dout_1c_0', 'dout_1c_1','dout_1c_2','dout_1c_3'] #64
    brams = [spec0_bram, spec1_bram, spec2_bram, spec3_bram]
    dtypes = ['>u8', '>u4', '>u4', '>u8']
    bitsize = [64, 32,32,64]
    for i in range(4):
        spec = calan.read_interleave_data(roach, brams[i], 9, bitsize[i], dtypes[i])
        pow_spec = calan.scale_and_dBFS_specdata(spec, acc, dBFS)
        data[i].set_data(freq, pow_spec)
    return data

if __name__ == '__main__':
    args = parser.parse_args()
    #roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=0)
    roach = corr.katcp_wrapper.FpgaClient('192.168.0.40')
    plot_spects(roach, args.acc)
