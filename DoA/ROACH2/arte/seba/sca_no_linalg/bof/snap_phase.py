import corr, struct, time
import calandigital as calan
import matplotlib.pyplot as plt
import numpy as np

#no se xq pero el snapshot no esta pescando las senales de control
def snap_phase(fpga, freq, fs, snaps=['adcsnap0', 'adcsnap1'],):
    """freq tiene que ser cr a banda base ie luego del aliasing
    """
    #prepare the snapshots for trigger the acquisition
    for snap in snaps:
        fpga.write_int(snap+'_ctrl',0)
        fpga.write_int(snap+'_ctrl',1)
    fpga.write_int('snap_trig',1)
    time.sleep(0.1)
    fpga.write_int('snap_trig',0)
    adc0 = struct.unpack('>8192b', fpga.read(snaps[0]+'_bram', 8192))
    adc1 = struct.unpack('>8192b', fpga.read(snaps[1]+'_bram', 8192))
    #calculate the dft for the frequency bin
    dft_len = len(adc0)
    k = round(1.*freq/fs*dft_len)  
    #print(k)
    twid_factors = np.exp(-1j*2*np.pi*np.arange(dft_len)*k/dft_len)
    dft0 = np.mean(adc0*twid_factors)
    dft1 = np.mean(adc1*twid_factors)
    correlation = dft0*np.conj(dft1)
    phase = np.rad2deg(np.angle(correlation))
    return phase


