import matplotlib.pyplot as plt
import numpy as np
import calandigital as calan
import argparse, time
import matplotlib.animation as animation


parser = argparse.ArgumentParser(
    description="intialize roach")

parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")

def read_brams(roach, bram_list,awidth,dwidth,dtype):
    re_list = []
    im_list = []
    for bram in bram_list:
        real, img = calan.read_deinterleave_data(roach, bram, dfactor=2,
                awidth=awidth, dwidth=dwidth, dtype=dtype)
        re_list.append(real)
        im_list.append(img)
    re_data = np.vstack(re_list).reshape((-1,), order='F')
    im_data = np.vstack(im_list).reshape((-1,), order='F')
    return re_data, im_data

def plot_spectrum(roach_):
    global roach, data, freq
    roach = roach_
    y_lim = (0, 100)
    data = []
    axes = []
    freq = np.linspace(0, 600, 2048, endpoint=0)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.set_title('ADC'+str(i))
        ax.grid()
        line, = ax.plot([],[])
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(4):
        data[i].set_data([],[])
    return data

def animate(i):
    adc_bram0 = ['dout_0a_0', 'dout_0a_1', 'dout_0a_2', 'dout_0a_3']
    adc_bram1 = ['dout_0c_0', 'dout_0c_1', 'dout_0c_2', 'dout_0c_3']
    adc_bram2 = ['dout_1a_0', 'dout_1a_1', 'dout_1a_2', 'dout_1a_3']
    adc_bram3 = ['dout_1c_0', 'dout_1c_1', 'dout_1c_2', 'dout_1c_3']
    bram_names = [adc_bram0, adc_bram1, adc_bram2, adc_bram3]
    
    roach.write_int('cnt_rst', 2)
    roach.write_int('cnt_rst', 0)
    for i in range(4):
        re, im = read_brams(roach, bram_names[i],14,16,'>h')
        dat = re+1j*im
        dat = dat.reshape([-1, 2048])
        dat = np.mean(np.abs(dat), axis=0)
        data[i].set_data(freq, 20*np.log10(dat+1))
    return data


if __name__ == '__main__':
    args = parser.parse_args()
    roach = calan.initialize_roach(args.ip)
    plot_spectrum(roach)
