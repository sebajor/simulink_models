import calandigital as calan
import numpy as np
import scipy.stats
import time, argparse, pyvisa, corr
import matplotlib.pyplot as plt


###
### Author: Sebastian Jorquera
###

parser = argparse.ArgumentParser(
    description="Synchronize 2 ADC5G ADCs in ROACH2.")
parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--bof", dest="boffile",
    help="Boffile to load into the FPGA.")
parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")
parser.add_argument("-g", "--genname", dest="generator_name", default=None,
    help="Generator name as a VISA string. Simulated if not given.\
    See https://pyvisa.readthedocs.io/en/latest/introduction/names.html")
parser.add_argument("-gp", "--genpow", dest="genpow", type=float,
    help="Power (dBm) to set at the generator to perform the calibration.")
parser.add_argument("-bw", "--bandwidth", dest="bandwidth", type=float, default=600,
    help="Bandwidth of the spectra to plot in MHz.")
parser.add_argument("-n","--points", dest="test_points", type=int, default=32,
        help='Number of points')
parser.add_argument("-z","--nyquist_zone", dest="nyq", type=int, default=3,
        help="Nyquist zone")
parser.add_argument("-s", "--snapnames", dest="snap_names", nargs="*", 
        help="snapnames")


def compute_adc_delay(freqs, angles, bandwidth):
    """
    Compute the adc delay between two unsynchronized adcs. It is done by
    computing the slope of the phase difference with respect the frequency,
    and then it translates this value into an integer delay in number of
    samples.
    :param freqs: frequency array in which the sideband ratios where computed.
    :param angles: angles of the correlation of two adcs in radians
    :param bandwidth: spectrometer bandwidth.
    :return: adc delay in number of samples.
    """
    linregress_results = scipy.stats.linregress(freqs, np.unwrap(angles))
    angle_slope = linregress_results.slope
    delay = int(round(angle_slope * 2*bandwidth / (2*np.pi))) # delay = dphi/df * Fs / 2pi
    print "Computed delay: " + str(delay)
    return delay

def get_sync_snapshots(roach, snap_names, addr_width=11):
    """
    Arm a bunch of snapshots to capture data in a synchronized fashion
    """
    roach.write_int('snap_trig',0)
    for snap in snap_names:
        roach.write_int(snap+'_ctrl',0)
        roach.write_int(snap+'_ctrl',1)
    time.sleep(0.1)
    roach.write_int('snap_trig',1)
    time.sleep(0.1)
    roach.write_int('snap_trig',0)
    adc_data = np.zeros([len(snap_names), 2**addr_width])
    for i in range(len(snap_names)):
        adc_data[i,:] = calan.read_data(roach, snap_names[i]+'_bram',
                addr_width, 8, '>i1')
    return adc_data


def relative_phase(data0, data1, freq, fs=1200, dft_len=2048):
    """
    Get the relative phase between two snapshots using a dft 
    """
    k = round(freq/fs*dft_len%dft_len)
    twidd_factor = np.exp(-1j*2*np.pi*np.arange(dft_len)*k/dft_len)
    dft0 = np.mean(data0*twidd_factor)
    dft1 = np.mean(data1*twidd_factor)
    correlation = dft0*np.conj(dft1)
    phase = np.angle(correlation)
    return phase




def sync_iter(roach, gen_source,curr_delay, freqs, bandwidth, snap_names, 
        spectra_data, phases_data, fig):
    phases01 = np.zeros(len(freqs))
    phases02 = np.zeros(len(freqs))
    phases03 = np.zeros(len(freqs))
    gen_source.write('outp on')
    freq_plot = np.linspace(0, bandwidth, 1024, endpoint=0)
    for i in range(len(freqs)):
        gen_source.write('freq '+str(freqs[i])+' mhz')
        adcs = get_sync_snapshots(roach, snap_names)
        ###plot spectrums
        for j in range(4):
            spectra = np.fft.fft(adcs[j])
            spectra = 20*np.log10(np.abs(spectra[:1024]))
            spectra_data[j].set_data(freq_plot, spectra)
        phases01[i] = relative_phase(adcs[0],adcs[1],freq=freqs[i])
        phases02[i] = relative_phase(adcs[0],adcs[2],freq=freqs[i])
        phases03[i] = relative_phase(adcs[0],adcs[3],freq=freqs[i])
        #plot phases
        phases_data[1].set_data(freqs, np.rad2deg(phases01))
        phases_data[2].set_data(freqs, np.rad2deg(phases02))
        phases_data[3].set_data(freqs, np.rad2deg(phases03))
        #update plots
        fig.canvas.draw()
        fig.canvas.flush_events()
    gen_source.write('outp off')

    delay1 = compute_adc_delay(freqs, phases01, bandwidth)
    delay2 = compute_adc_delay(freqs, phases02, bandwidth)
    delay3 = compute_adc_delay(freqs, phases03, bandwidth)
    dels = np.array([delay1,delay2,delay3])
    adc0_delay =0; adc1_delay =0; adc2_delay=0; adc3_delay=0;

    print("delay1:%i \t delay2:%i \t delay3:%i"%(delay1, delay2,delay3))

    if((dels>0).any()):
        most_neg = np.max(dels)
        adc0_delay = most_neg+curr_delay[0]
    else:
        #if every one is negative we could set the other one
        adc0_delay = curr_delay[0]
        adc1_delay = curr_delay[1]-delay1
        adc2_delay = curr_delay[2]-delay2
        adc3_delay = curr_delay[3]-delay3
    return [adc0_delay, adc1_delay, adc2_delay, adc3_delay]


def main():
    args = parser.parse_args()
    # initialize roach
    if(args.upload):
        roach = calan.initialize_roach(args.ip, boffile=args.boffile, upload=args.upload)
    else:
        roach = corr.katcp_wrapper.FpgaClient(args.ip, 7147, timeout=10.)
    time.sleep(1)
    print(roach.is_connected())

    test_freqs = np.linspace((args.nyq-1)*args.bandwidth, args.nyq*args.bandwidth, 2048, endpoint=False)
    test_freqs = test_freqs[1::2048//args.test_points]

    if(args.generator_name is None):
        raise Exception("Generator info is missing :(")
    else:
        rm = pyvisa.ResourceManager('@py')
    generator = rm.open_resource(args.generator_name)
    generator.write("power "+str(args.genpow)+" dBm")

    ##reset the delays
    roach.write_int('adc0_delay',0)
    roach.write_int('adc1_delay',0)
    roach.write_int('adc2_delay',0)
    roach.write_int('adc3_delay',0)
    
    fig, spectra_data, phases_data = create_figure(args.bandwidth)
    
    print("Start Synchronizing ADCs...")
    prev_delays = np.zeros(4)
    while(1):
        new_delays = sync_iter(roach, generator,prev_delays, test_freqs, 
                args.bandwidth, args.snap_names, spectra_data, phases_data,
                fig)
        print("new delays:")
        print("adc0: %i \t adc1: %i \t adc2: %i \t adc3: %i" %(new_delays[0], new_delays[1], new_delays[2], new_delays[3]))
        roach.write_int('adc0_delay', new_delays[0])
        roach.write_int('adc1_delay', new_delays[1])
        print(roach.read_int('adc1_delay'))
        roach.write_int('adc2_delay', new_delays[2])
        roach.write_int('adc3_delay', new_delays[3])
        time.sleep(0.5)
        if(np.sum(prev_delays-np.array(new_delays))==0):
            print("Synchronization done :)")
            break
        prev_delays = new_delays


def create_figure(bw):
    fig, axes = plt.subplots(2,4, squeeze=False)
    fig.set_tight_layout(True)
    fig.show()
    fig.canvas.draw()
    ###plots for the spectrum at each ADCs
    spectra_data = []
    for i in range(4):
        axes[0,i].set_xlim(0,bw)
        axes[0,i].set_ylim(0, 100)
        axes[0,i].set_xlabel('Frequency MHz')
        axes[0,i].set_ylabel('dB')
        axes[0,i].grid()
        data, = axes[0,i].plot([],[])
        spectra_data.append(data)
    ###plots for the relatives phases
    phases_data = []
    for i in range(4):
        axes[1,i].set_xlim(0,bw)
        axes[1,i].set_ylim(-200,200)
        axes[1,i].set_xlabel('Frequency MHz')
        axes[1,i].set_ylabel('phases')
        axes[1,i].grid()
        data, = axes[1,i].plot([],[])
        phases_data.append(data)
    return fig, spectra_data, phases_data
    

if __name__ == '__main__':
    main()
