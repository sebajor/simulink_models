import numpy as np
import matplotlib.patches as mpatches
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

def plot_rank(_fpga, _acc, _freq=[0, 600]):
    global fpga, data, freq, dBFS, acc
    dBFS = 8*6.02+10*np.log10(2048)
    acc = _acc
    fpga =_fpga
    y_lim = (-90, 0)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    names = ['corr', 'pow', 'sw rank', 'hw rank']
    bl_patch = mpatches.Patch(color='blue', label='hw')
    or_patch = mpatches.Patch(color='orange', label='sw')
    fig.legend(handles=[bl_patch, or_patch],loc='upper left')
    ax = fig.add_subplot(111)
    ax.set_xlim(freq[0], freq[-1])
    ax.set_ylim(-0.5, 3)
    ax.grid()
    hw, = ax.plot([],[],lw=2, zorder=0)
    sw, = ax.plot([],[],lw=2, zorder=10)
    data.append(hw)
    data.append(sw)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(2):
        data[i].set_data([],[])
    return data

def animate(i):
    corr_bram = ['corr0', 'corr1', 'corr2', 'corr3'] #64
    spec_bram = ['mul0', 'mul1', 'mul2', 'mul3']
    dtypes = ['>u4', '>u4', '>u4']
    bitsize = [32, 32,32]
    corr_vals = calan.read_interleave_data(roach, corr_bram, 9, 32, '>u4')
    spec = calan.read_interleave_data(roach, spec_bram, 9, 32, '>u4')
    sw = (corr_vals)/spec+1 ##+1to avoid not def
    hw = calan.read_data(roach, 'rfi', 11, 16, '>h')/2.**13
    hw = hw.reshape(-1,4)[:,::-1].flatten()
    data[1].set_data(freq, sw)
    data[0].set_data(freq, hw)
    return data

if __name__ == '__main__':
    args = parser.parse_args()
    roach = corr.katcp_wrapper.FpgaClient(args.ip)
    #roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=0)
    plot_rank(roach, args.acc)
