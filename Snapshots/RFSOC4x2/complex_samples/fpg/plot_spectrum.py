import numpy as np
import matplotlib.pyplot as plt
import argparse, time
import casperfpga 
from matplotlib.animation import FuncAnimation
import ipdb

parser = argparse.ArgumentParser(
    description="Plot snapshots from snapshot blocks in ROACH model.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-f", "--fpg", dest="fpgfile",
    help="fpgfile to load into the FPGA.")
parser.add_argument("-dt", "--dtype", dest="dtype", default=">i2",
    help="Data type of snapshot data. Must be Numpy compatible.")
parser.add_argument("-bw", "--bw", dest="bandwidth", default=1966.08,
    help="Bandwidth of the system.")

def plot_spectrum():
    args = parser.parse_args()
    fpga = casperfpga.CasperFpga(args.ip)
    time.sleep(0.1)
    fpga.upload_to_ram_and_program(args.fpgfile)
    time.sleep(0.1)
    fig, axes = create_figure(fpga.snapshots.keys(), args.nsamples, args.dtype)
    freq = np.linspace()
    
    def get_sync_snapshots(fpga, nsamples, dtype, bram_addr=2**11):
        fpga.write_int('snap_trig',0)
        ##arm all the snapshots
        for snap in fpga.snapshots.keys():
            fpga.write_int(snap+'_ctrl',0)
            fpga.write_int(snap+'_ctrl',1)
        fpga.write_int('snap_trig',1)
        time.sleep(0.1)
        fpga.write_int('snap_trig',0)
        time.sleep(0.1)
        #get the data
        freq = np.linsapce(0,args.bw, args.nsamples, endpoint=True)
        snapnames = fpga.snapshots.keys()
        adc_data = np.zeros((len(snapnames)//2, nsamples), dtype=complex)
        for i in range(len(snapnames)//2):
            raw = fpga.read(snapnames[2*i]+'_bram', bram_addr*16)
            data_imag = np.frombuffer(raw, dtype)
            raw = fpga.read(snapnames[2*i+1]+'_bram', bram_addr*16)
            data_real = np.frombuffer(raw, dtype)
            adc_data[i,:] = data_real[:nsamples]+1j*data_imag[:nsamples]
        return adc_data

    def animate(i):
        adc_data = get_sync_snapshots(fpga, args.nsamples, args.dtype)
        spect = np.fft.fft(adc_data, axis=1)
        ##reorder the channels (by default the first half are positive freq and the last
        ##half are the negative freqs
        spect = np.hstack((spect[:,spect.shape[1]//2:], spect[:, :spect.shape[1]//2])
        for line,i in zip(axes,range(adc_data.shape[0])):
            line.set_data(freq, spect[i,:])
        return axes
    ani = FuncAnimation(fig, animate, blit=True)
    plt.show()
    



def create_figure(snapshots, samples, dtype):
    names = ['ADC D', 'ADC C', 'ADC B', 'ADC A']
    axmap = {1 : (1,1), 2 : (1,2), 4 : (2,2), 16 : (4,4)}
    fig, axes = plt.subplots(*axmap[len(names)], squeeze=False)
    fig.set_tight_layout(True)

    lines = []
    for ax,name in zip(axes.flatten(), names):
        ax.set_xlim(samples)
        ax.set_ylim(np.iinfo(dtype).min-10, np.iinfo(dtype).max+10)
        ax.set_xlabel('Samples')
        ax.set_ylabel('Amplitude')
        ax.set_title(name)
        ax.grid()
        line, = ax.plot([],[], animated=True)
        lines.append(line)
    return fig, lines


if __name__ == '__main__':
    plot_snapshot()

