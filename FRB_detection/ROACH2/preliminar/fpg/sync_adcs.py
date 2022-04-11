import calandigital as calan
from calandigital.instruments import generator
import matplotlib.pyplot as plt
import numpy as np
import sys, time
sys.path.append('codes/')
import utils
import control
from scipy.fftpack import fft
import scipy.stats

roach_ip = '192.168.1.18'
boffile = 'arte.fpg'

snap_names = ['adcsnap0', 'adcsnap1', 'adcsnap2', 'adcsnap3']

##agilent connection information
agilent_info = {    'type'      :   'visa',
                    'connection':   'TCPIP::192.168.1.34::INSTR',
                    'def_freq'  :   1200,
                    'def_power' :   -6
        }

bw = [1200, 1800]    #mhz
dft_channels = 2048
test_points = 32#128

######
def find_period(corr_data):
    """Search the peaks of a correlation data looking for the change
    in the curvature of the peaks (ie second derivative) Then we look
    for the maximum value in those index.
    https://stackoverflow.com/questions/59265603/how-to-find-period-of-signal-autocorrelation-vs-fast-fourier-transform-vs-power
    """
    inflection = np.diff(np.sign(np.diff(corr_data)))
    peak = (inflection <0).nonzero()[0]+1
    delay = peak[corr_data[peak].argmax()]
    return delay



def cross_corr_dly(adc0, adc1):
    """ Return the delay that maximize the correlation of the
    time domain adc0 and adc1.
    outputs:
            corr0: output of correlate(adc0, adc1)
            corr1: output of correalte(adc1, adc0)
            [delay0, delay1] where delay0 is comes from correlate(adc0, adc1)
            and delay1 comes from correlate(adc1, adc0)
    """
    N = len(adc0)
    adc0_data = adc0-np.mean(adc0)
    adc1_data = adc1-np.mean(adc1)
    corr0 = np.correlate(adc0_data, adc1_data, mode='full')
    corr0 = corr0[-N:]
    corr1 = np.correlate(adc1_data, adc0_data, mode='full')
    corr1 = corr1[-N:]
    delay0 = find_period(corr0)
    delay1 = find_period(corr1)
    return corr0, corr1, delay0, delay1


def compute_adc_delay(freqs, angles, bandwidth):
    """
    Compute the adc delay between two unsynchronized adcs. It is done by 
    computing the slope of the phase difference with respect the frequency, 
    and then it translates this value into an integer delay in number of 
    samples.
    :param freqs: frequency array in which the sideband ratios where computed.
    :param ratios: complex ratios array of the adcs. The complex ratios is the 
        complex division of an spectral channel from adc0 with adc1.
    :param bandwidth: spectrometer bandwidth.
    :return: adc delay in number of samples.
    """
    linregress_results = scipy.stats.linregress(freqs, np.unwrap(angles))
    angle_slope = linregress_results.slope
    delay = int(round(angle_slope * 2*bandwidth / (2*np.pi))) # delay = dphi/df * Fs / 2pi
    print "Computed delay: " + str(delay)
    return delay
   



roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
time.sleep(1)
roach_control = control.roach_control(roach)

freq = np.linspace(bw[0], bw[1], dft_channels, endpoint=False)
#subsample freq
sub_sample = dft_channels//test_points
freq = freq[2::sub_sample]

agilent_source = generator.create_generator(agilent_info)
time.sleep(0.5)

agilent_source.set_freq_mhz(freq[10])
agilent_source.turn_output_on()
"""
adcs = np.zeros([4, 2048, len(freq)])
for j in range(len(freq)):
    k = freq[j]/1200*2048%2048
    k2 = (freq[j]-bw[0])/1200*2048
    print('freq: %.3f \t k:%i \t k2:%i '%(freq[j],k, k2))
    for i in range(2):
        agilent_source.set_freq_mhz(freq[j])
        adcs[:,:,j] = roach_control.get_sync_snapshots(snap_names)
        phase12 = utils.relative_phase(adcs[0,:,j], adcs[1,:,j], freq=freq[j])
        print('phase: %.4f' %np.rad2deg(phase12))
        #corr0,corr1,delay0,delay1 = cross_corr_dly(adcs[0,:,j], adcs[1,:,j])
        #print('delay0: %.2f \t delay1: %.2f'%(delay0,delay1))
    print('\n')
"""
def sync_iter(gen_source,curr_delay, freqs, bandwidth, snap_names):
    phases01 = np.zeros(len(freqs))
    phases02 = np.zeros(len(freqs))
    #phases03 = np.zeros(len(freqs))
    gen_source.turn_output_on()
    for i in range(len(freqs)):
        gen_source.set_freq_mhz(freqs[i])
        adc0,adc1,adc2,adc3 =roach_control.get_sync_snapshots(snap_names)
        phases01[i] = utils.relative_phase(adc0,adc1,freq=freqs[i])
        phases02[i] = utils.relative_phase(adc0,adc2,freq=freqs[i])
        #phases03[i] = utils.relative_phase(adc0,adc3,freq=freqs[i])
    gen_source.turn_output_off()

    delay1 = compute_adc_delay(freqs, phases01, bandwidth)
    delay2 = compute_adc_delay(freqs, phases02, bandwidth)
    #delay3 = compute_adc_delay(freqs, phases03, bandwidth)
    
    dels = np.array([delay1,delay2])#,delay3])
    adc0_delay = 0
    adc1_delay = 0
    adc2_delay = 0
    #adc3_delay = 0
    if((dels>0).any()):
        most_neg = np.max(dels)#np.min(dels)
        adc0_delay = most_neg+curr_delay[0]
    else:
        ##if every one is positive we could set the other ones
        adc1_delay = curr_delay[1]-delay1
        adc2_delay = curr_delay[2]-delay2
        #adc3_delay = delay3+curr_delay[3]
    return [adc0_delay, adc1_delay, adc2_delay] #adc3_delay]


adc0_delay = 0
adc1_delay = 0
adc2_delay = 0
#adc3_delay = 0

bandwidth = (bw[1]-bw[0])

curr_delay = [0,0,0,0]
iter0 = sync_iter(agilent_source,curr_delay, freq, bandwidth, snap_names)
print("latencies : %i %i %i" %(iter0[0],iter0[1],iter0[2]))

for i in range(3):
    roach_control.set_adc_latencies(i, iter0[i])

time.sleep(0.5)
curr_delay = iter0
iter1 = sync_iter(agilent_source,curr_delay, freq, bandwidth, snap_names)
print("latencies : %i %i %i" %(iter1[0],iter1[1],iter1[2]))
for i in range(3):
    roach_control.set_adc_latencies(i, iter1[i])


time.sleep(0.5)
curr_delay = iter1
iter2 = sync_iter(agilent_source,curr_delay, freq, bandwidth, snap_names)
print("latencies : %i %i %i" %(iter2[0],iter2[1],iter2[2]))
#for i in range(4):
#    roach_control.set_adc_latencies(i, iter2[i])


agilent_source.close_connection()
