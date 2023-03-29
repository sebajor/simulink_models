import numpy as np
import matplotlib.pyplot as plt
import utils, corr, argparse
from matplotlib.animation import FuncAnimation




parser = argparse.ArgumentParser(
    description="Plot spectra from an spectrometer model in ROACH.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH1 only).")
parser.add_argument("-f", "--file", dest="filename")
parser.add_argument("-fr", "--freq", dest="freq", type=float)



if __name__ == '__main__':
    args = parser.parse_args()
    roach = corr.katcp_wrapper.FpgaClient(args.ip)
    if(args.upload):
        roach.upload_program_bof(args.boffile)
        time.sleep(0.1)
    freq = np.linspace(1200,1800, 2048, endpoint=False)
    channel = np.argmin(np.abs(freq-args.freq))
    print("Saving data from frequency %.3f with channel number %i" %(args.freq, channel))

    data_beam = utils.get_beam(roach)
    data_quant_beam = utils.get_quantize_beam(roach)
    plt.ion()
    fig, axes = plt.subplots(1,2, sharex=True)
    try:
        while(1):
            beam0 = utils.get_beam(roach)
            beam1 = utils.get_quantize_beam(roach)
            data_beam = np.vstack((data_beam, beam0))
            data_quant_beam = np.vstack((data_quant_beam, beam1))
            
            axes[0].cla()
            axes[1].cla()
            axes[0].plot(10*np.log10(data_beam[:,channel]))
            axes[1].plot(10*np.log10(data_quant_beam[:, channel]))
            fig.canvas.draw()
    except KeyboardInterrupt:
        np.savez(args.filename, 
                 beam = data_beam,
                 beam_quant= data_quant_beam)


            
     
    
      



