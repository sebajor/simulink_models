import numpy as np
import calandigital as calan 
import matploltib.pyplot as plt
from matplotlib.animation import FuncAnimation
import corr, time

global acc, adc_bits, spec_channels, dBFS, roach_ip
acc = 1024
adc_bits = 8
spec_channels = 2048
dBFS = 6.02 adc_bits + 10*log10(spec_channels)
roach_ip = '10.17.89.91'
boffile = 'corr4in_2048ch_600mhz.bof.gz'


def plot_correlation(_fpga, _freq=[1200, 1800]):
    global fpga, data, freq
    fpga = _fpga
    y_lim = (40,140)
    data = []
    axes = []
    freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    fig = plt.figure()
    names = ['phase01', 'phase12', 'phase13']
    for i in range(3):
        ax = fig.add_subplot(2,3,i+1)
        ax.set_ylim(-180,180)
        ax.set_xlim(freq[0], freq[-1])
        ax.set_title(names[i])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
    names = ['ADC0', 'ADC1', 'ADC2', 'ADC3']
    for i in range(4):
        ax = fig.add_subplot(2,4,5+i)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = FuncAnimation(fig, animate, interval=50, blit=True)
    plt.show()


    def get_phase():
        corr01_re_bram = ['dout_0a0c_re0','dout_0a0c_re1', 'dout_0a0c_re2', 'dout_0a0c_re3']
        corr01_im_bram = ['dout_0a0c_im0','dout_0a0c_im1', 'dout_0a0c_im2', 'dout_0a0c_im3']
        
        corr02_re_bram = ['dout_0a1a_re0','dout_0a1a_re1', 'dout_0a1a_re2', 'dout_0a1a_re3']
        corr02_im_bram = ['dout_0a1a_im0','dout_0a1a_im1', 'dout_0a1a_im2', 'dout_0a1a_im3']

        corr03_re_bram = ['dout_0a1c_re0','dout_0a1c_re1', 'dout_0a1c_re2', 'dout_0a1c_re3']
        corr03_im_bram = ['dout_0a1c_im0','dout_0a1c_im1', 'dout_0a1c_im2', 'dout_0a1c_im3']

        bram_re = [corr01_re_bram, corr02_re_bram, corr03_re_bram]
        bram_im = [corr01_im_bram, corr02_im_bram, corr03_im_bram]
        
        phase = np.zeros([3, 2048])
        for i in range(3):
            corr_re = calan.read_interleave_data(fpga, bram_re[i], 9, 64, '>q')
            corr_im = calan.read_interleave_data(fpga, bram_im[i], 9, 64, '>q')
            phase[i,:] = np.arctan2(corr_im, corr_re)
        return phase

    def get_power():
        pow0 = ['dout_0a2_0', 'dout_0a2_1', 'dout_0a2_2', 'dout_0a2_3']
        pow1 = ['dout_0c2_0', 'dout_0c2_1', 'dout_0c2_2', 'dout_0c2_3']
        pow2 = ['dout_1a2_0', 'dout_1a2_1', 'dout_1a2_2', 'dout_1a2_3']
        pow3 = ['dout_1c2_0', 'dout_1c2_1', 'dout_1c2_2', 'dout_1c2_3']
        pows = [pow0,pow1,pow2,pow3]
        power_data = np.zeros((4,2048))
        for i in range(4):
            data = calan.read_interleave_data(fpga, pows[i], 9, 64, '>Q')
            power_data[i,:] = calan.scale_and_dBFS_specdata(data, acc, dBFS)
        return power_data
            
    def animate(i):
        corrs = get_phase()
        for i in range(3):
            data[i].set_data(freq, corrs[i])
        pows = get_power()
        for j in range(4):
            data[3+i].set_data(freq, pows[i])
        return data

if __name__ == '__main__':
    roach = corr.katcp_wrapper.FpgaClient(roach_ip)
    time.sleep(0.5)
    roach.upload_program_bof(boffile, 3000)
    time.sleep(0.5)
    plot_correlation(roach)


