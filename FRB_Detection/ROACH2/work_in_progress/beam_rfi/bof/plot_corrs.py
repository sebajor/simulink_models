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

def plot_corrs(_fpga, _acc, _freq=[1200, 1800]):
    global fpga, data, freq, dBFS, acc
    dBFS = 8*6.02+10*np.log10(2048)
    acc = _acc
    fpga =_fpga
    y_lim = (-85, 0)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    names = ['corr', 'adc0', 'adc1', 'mul']
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        ax.set_title(names[i])
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(4):
        data[i].set_data([],[])
    return data

def animate(i):
    corr_bram = ['corr0', 'corr1', 'corr2', 'corr3'] #64
    spec1_bram = ['dout_0c_0', 'dout_0c_1','dout_0c_2','dout_0c_3'] #32
    spec2_bram = ['dout_1a_0', 'dout_1a_1','dout_1a_2','dout_1a_3'] #32
    mul_bram = ['mul0', 'mul1', 'mul2', 'mul3']
    brams = [corr_bram, spec1_bram, spec2_bram, mul_bram]
    dtypes = ['>u4', '>u4', '>u4', '>u4']
    bitsize = [32, 32,32,32]
    for i in range(4):
        spec = calan.read_interleave_data(roach, brams[i], 9, bitsize[i], dtypes[i])
        pow_spec = calan.scale_and_dBFS_specdata(spec, acc, dBFS)
        data[i].set_data(freq, pow_spec)
    return data

if __name__ == '__main__':
    args = parser.parse_args()
    roach = corr.katcp_wrapper.FpgaClient(args.ip)
    #roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=0)
    plot_corrs(roach, args.acc)
