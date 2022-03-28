import calandigital as calan
import numpy as np
import argparse, time, corr
import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")
parser.add_argument("-a", "--acc_len", dest="acc_len",
    help="Accumulation length")
parser.add_argument("-g", "--gain", dest="gain", type=float,
    help="Gain for the bit reduction")

def plot_reduced_spect(_fpga, _acc_len, _freq=[0,600]):
    global fpga, data, freq, acc_len
    fpga = _fpga
    acc_len = _acc_len
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=False)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.set_ylim(0,100)
    ax.set_xlim(_freq[0], _freq[1])
    data, = ax.plot([],[],lw=2)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    data.set_data([],[])
    return data,

def animate(i):
    dBFS = 6.02*8 + 1.76 + 10*np.log10(2048)
    spect = calan.read_deinterleave_data(roach=fpga, bram='reduced',dfactor=4,
            awidth=9,dwidth=32,dtype='>I')
    spect = calan.scale_and_dBFS_specdata(np.array(spect), acc_len, dBFS)
    data.set_data(freq, spect)
    return data,


if __name__ == '__main__':
    args = parser.parse_args()
    print(args.ip)
    print(args.upload)
    print(args.boffile)
    #roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=args.upload)
    roach = corr.katcp_wrapper.FpgaClient(args.ip)
    time.sleep(1)
    #print('set the gain: %.4f'%args.gain)
    #gain = calan.float2fixed(args.gain, 32,15)
    #roach.write_int('gain', gain)
    plot_reduced_spect(roach, args.acc_len)

