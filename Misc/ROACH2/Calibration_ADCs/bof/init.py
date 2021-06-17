import calandigital as calan
import numpy as np
import corr, time, struct
from scipy.fftpack import fft

def time_phase(adc0, adc1, freq, fs=1200):
    dft_len = len(adc0)
    k = round(1.*freq/fs*dft_len)  
    #print(k)
    twid_factors = np.exp(-1j*2*np.pi*np.arange(dft_len)*k/dft_len)
    dft0 = np.mean(adc0*twid_factors)
    dft1 = np.mean(adc1*twid_factors)
    correlation = dft0*np.conj(dft1)
    phase = np.rad2deg(np.angle(correlation))
    return phase


def dft_phase(adc0, adc1, freq, fs=1200):
    dft_len = len(adc0)
    k = round(1.*freq/fs*dft_len)  
    #print(k)
    spec0 = fft(adc0)
    spec1 = fft(adc1)
    correlation = spec0*np.conj(spec1)
    phase = np.rad2deg(np.angle(correlation[int(k)]))
    return phase


roach_ip = '192.168.0.40'
boffile = 'test_cal_v1.bof.gz'
freq = 20
fs = 1080*2
iters = 64


roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)

snaps = ['adcsnap0', 'adcsnap1']

roach.write_int('snap_trig',0)


for i in range(iters):
    roach.snapshot_arm(snaps[0],man_trig=1,man_valid=1)
    roach.snapshot_arm(snaps[1],man_trig=1,man_valid=1)
    roach.write_int('snap_trig',1)
    time.sleep(0.1)
    roach.write_int('snap_trig',0)
    adc0 = struct.unpack('>8192b', roach.read('adc0', 8192))
    adc1 = struct.unpack('>8192b', roach.read('adc1', 8192))
    #adc0 = struct.unpack('>8192b', roach.read(snaps[0]+'_bram', 8192))
    #adc1 = struct.unpack('>8192b', roach.read(snaps[1]+'_bram', 8192))
    #adc0,adc1 = calan.read_snapshots(roach,snaps)
    ang1 = time_phase(adc0,adc1,freq, fs)
    ang2 = dft_phase(adc0, adc1,freq, fs)
    print("time: %.4f \t dft: %.4f"%(ang1, ang2))
    #print("time: %.4f"%(ang1))
