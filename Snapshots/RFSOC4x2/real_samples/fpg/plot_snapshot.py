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
parser.add_argument("-ns", "--nsamples", dest="nsamples", type=int, default=256,
    help="Number of samples of snapshot to plot.")

def plot_snapshot():
    args = parser.parse_args()
    fpga = casperfpga.CasperFpga(args.ip)
    time.sleep(0.1)
    fpga.upload_to_ram_and_program(args.fpgfile)
    time.sleep(0.1)
    
    fig, axes = create_figure(fpga.snapshots.keys(), args.nsamples, args.dtype)

    def animate(i):
        for snap, line in zip(fpga.snapshots, axes):
            raw, raw_time = snap.read_raw(man_trig=True, man_valid=True)
            snap_data = np.frombuffer(raw['data'], dtype=args.dtype)
            #snap_data = snap_data.reshape((-1,8))[:,::-1].flatten()
            #snap_data = fpga.snapshot_get(snap, man_trig=True, man_valid=True)
            line.set_data(range(args.nsamples), snap_data[:args.nsamples])
        return axes
    ani = FuncAnimation(fig, animate, blit=True)
    plt.show()

    
def create_figure(snapshots, samples, dtype):
    names = ['ADC D', 'ADC C', 'ADC B', 'ADC A']
    axmap = {1 : (1,1), 2 : (1,2), 4 : (2,2), 16 : (4,4)}
    fig, axes = plt.subplots(*axmap[len(snapshots)], squeeze=False)
    fig.set_tight_layout(True)

    lines = []
    for snap,ax,name in zip(snapshots, axes.flatten(), names):
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

