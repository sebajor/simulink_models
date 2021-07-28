import calandigital as calan
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ipdb

def plot_specs(_fpga, _acc):
    global fpga, data, freq, acc
    acc = _acc
    fpga = _fpga
    y_lim = (-80, 0)
    data = []
    axes = []
    #freq = np.linspace(_freq[0], _freq[1], 2048, endpoint=0)
    freq = np.arange(2048)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(freq[0], freq[-1])
        ax.grid()
        line, = ax.plot([],[],lw=2)
        data.append(line)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()


def init():
    for i in range(4):
        data[i].set_data([],[])
    return data

def animate(i):
    dBFS = 6.02*8+10*np.log10(2048)
    ch0_brams = ['dout_0a_0', 'dout_0a_1', 'dout_0a_2', 'dout_0a_3']
    ch1_brams = ['dout_0c_0', 'dout_0c_1', 'dout_0c_2', 'dout_0c_3']
    ch2_brams = ['dout_1a_0', 'dout_1a_1', 'dout_1a_2', 'dout_1a_3']
    ch3_brams = ['dout_1c_0', 'dout_1c_1', 'dout_1c_2', 'dout_1c_3']
    brams = [ch0_brams, ch1_brams, ch2_brams, ch3_brams]
    for i in range(len(brams)):
        dat = calan.read_interleave_data(roach, brams[i], 9, 64, '>u8')
        mag = calan.scale_and_dBFS_specdata(dat, acc, dBFS)
        data[i].set_data(freq, mag)
    return data



def flag_channels(roach, flags, n_chan=2048, n_streams=4):
    """ n_chan: fft channels
        n_streams = parallel streams (out of the fft)
    """
    chan_flag = np.zeros(n_chan)
    chan_flag[flags] = 1
    chan_flag = chan_flag.reshape([-1, n_streams])
    #need to append zeros until 8 bits to use packbits
    aux = np.zeros([n_chan/n_streams, 8-n_streams])
    chan_flags = np.hstack([chan_flag, aux])
    vals = np.packbits(chan_flags[:,::-1].astype(np.uint8))
    ind = np.where(vals!=0)[0]
    #ipdb.set_trace()
    roach.write_int('flag_en',1)
    for i in range(len(ind)):
        roach.write_int('flag_num',ind[i])
        roach.write_int('flag_config', vals[ind[i]])
    roach.write_int('flag_en',0)


if __name__ == '__main__':
    roach_ip = '192.168.0.40'
    boffile = 'flagged_spectrometer.bof.gz'
    acc = 1024
    #channels to be flagged
    flags = np.arange(71).tolist()
    #flags = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    flags = flags+[1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 
            1025, 1026, 1027, 1028, 1029, 1030]
    ###
    roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
    roach.write_int('cnt_rst',1)
    print('writing flags..')
    flag_channels(roach, flags)
    print('finish!')
    roach.write_int('acc_len', acc)
    roach.write_int('cnt_rst',0)
    plot_specs(roach, acc)

