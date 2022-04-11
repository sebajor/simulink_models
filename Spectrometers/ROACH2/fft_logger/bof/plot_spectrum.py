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
    y_lim = (40, 140)
    data = []
    axes = []
    freq = np.linspace(0, 1080, 2048, endpoint=0)
    fig = plt.figure()
    for i in range(2):
        ax = fig.add_subplot(1,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        ax.set_title("ADC "+str(i))
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(2):
        data[i].set_data([],[])
    return data

def animate(i):
    adc0_bram = ['dout0_0', 'dout0_1', 'dout0_2', 'dout0_3',
                 'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7']
    adc1_bram = ['dout1_0', 'dout1_1', 'dout1_2', 'dout1_3',
                 'dout1_4', 'dout1_5', 'dout1_6', 'dout1_7']
    
    roach.write_int('cnt_rst', 2)
    roach.write_int('cnt_rst', 0)
    #time.sleep(0.1)
    re, im = read_brams(roach, adc0_bram,12,32,'>i')
    data0 = re+1j*im
    data0 = data0.reshape([-1,2048])
    re, im = read_brams(roach, adc1_bram,12,32,'>i')
    data1 = re+1j*im
    data1 = data0.reshape([-1,2048])
    
    data0 = np.mean(np.abs(data0), axis=0)
    data1 = np.mean(np.abs(data1), axis=0)

    data[0].set_data(freq, 10*np.log10(data0+1))
    data[1].set_data(freq, 10*np.log10(data1+1))
    return data

if __name__ == '__main__':
    args = parser.parse_args()
    roach = calan.initialize_roach(args.ip)
    plot_spectrum(roach)
