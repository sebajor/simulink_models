import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import calandigital as calan

parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")



def plot_antennas(_fpga, _freq=[1200, 1800]):
    global fpga, data, freq
    fpga = _fpga;
    y_lim = (0, 100)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        ax.set_title("antenna "+str(i))
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()


def init():
    for i in range(4):
        data[i].set_data([],[])
    return data

def animate(i):
    spec1_0, spec1_1 = calan.read_deinterleave_data(fpga, 'spec1_0', 2, 9, 64, '>u4')
    spec1_2, spec1_3 = calan.read_deinterleave_data(fpga, 'spec1_1', 2, 9, 64, '>u4')
    spec1 = np.vstack([spec1_0,spec1_1,spec1_2,spec1_3]).reshape((-1,), order='F')

    spec2_0, spec2_1 = calan.read_deinterleave_data(fpga, 'spec2_0', 2, 9, 64, '>u4')
    spec2_2, spec2_3 = calan.read_deinterleave_data(fpga, 'spec2_1', 2, 9, 64, '>u4')
    spec2 = np.vstack([spec2_0,spec2_1,spec2_2,spec2_3]).reshape((-1,), order='F')

    spec3_0, spec3_1 = calan.read_deinterleave_data(fpga, 'spec3_0', 2, 9, 64, '>u4')
    spec3_2, spec3_3 = calan.read_deinterleave_data(fpga, 'spec3_1', 2, 9, 64, '>u4')
    spec3 = np.vstack([spec3_0,spec3_1,spec3_2,spec3_3]).reshape((-1,), order='F')

    spec4_0, spec4_1 = calan.read_deinterleave_data(fpga, 'spec4_0', 2, 9, 64, '>u4')
    spec4_2, spec4_3 = calan.read_deinterleave_data(fpga, 'spec4_1', 2, 9, 64, '>u4')
    spec4 = np.vstack([spec4_0,spec4_1,spec4_2,spec4_3]).reshape((-1,), order='F')


    data[0].set_data(freq, 10*np.log10(spec1+1))
    data[1].set_data(freq, 10*np.log10(spec2+1))
    data[2].set_data(freq, 10*np.log10(spec3+1))
    data[3].set_data(freq, 10*np.log10(spec4+1))
    return data


if __name__ == '__main__':
    args = parser.parse_args()
    roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=args.upload)
    plot_antennas(roach)
