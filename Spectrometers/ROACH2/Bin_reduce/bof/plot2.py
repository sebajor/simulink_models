import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc

def plot_spect(_fpga,_bw):
    global data, fpga, freq0, freq1, bw
    bw = _bw
    freq0 = np.linspace(0, bw, 4096, endpoint =False)
    freq1 = np.linspace(0, bw, 128, endpoint=False)
    fpga = _fpga
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    data1, = ax1.plot([],[], lw=2)
    data2, = ax2.plot([],[], lw=2)
        
    data = [data1, data2]
    ax1.set_title('ADC0 spectrum')
    ax1.set_xlabel('MHz')
    ax1.set_ylabel('[dB]')
    ax2.set_title('reduce spectrum')
    ax2.set_xlabel('cycles')
    ax2.set_ylabel('[dB]')

    ax1.set_xlim(0, bw)
    ax1.set_ylim(20, 120)
    ax2.set_xlim(0, bw)
    ax2.set_ylim(20, 120)
    
    ax1.grid()
    ax2.grid()
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show() 


def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    return data

def get_data():
    d0_0 = np.array(struct.unpack('>512Q', fpga.read('dout0_0', 512*8)))
    d0_1 = np.array(struct.unpack('>512Q', fpga.read('dout0_1', 512*8)))
    d0_2 = np.array(struct.unpack('>512Q', fpga.read('dout0_2', 512*8)))
    d0_3 = np.array(struct.unpack('>512Q', fpga.read('dout0_3', 512*8)))
    d0_4 = np.array(struct.unpack('>512Q', fpga.read('dout0_4', 512*8)))
    d0_5 = np.array(struct.unpack('>512Q', fpga.read('dout0_5', 512*8)))
    d0_6 = np.array(struct.unpack('>512Q', fpga.read('dout0_6', 512*8)))
    d0_7 = np.array(struct.unpack('>512Q', fpga.read('dout0_7', 512*8)))
    
    d0 = np.vstack([d0_0,d0_1,d0_2,d0_3,d0_4,d0_5,d0_6,d0_7])
    d0 = np.transpose(d0).flatten()
    d0 = 10*np.log10(d0+1)
    
    red = np.array(struct.unpack('>128Q', fpga.read('small_spec', 128*8)))
    d1 = 10*np.log10(red+1)
    return [d0, d1]




def animate(i):
    aux = get_data()
    data[0].set_data(freq0,aux[0])
    data[1].set_data(freq1, aux[1])
   # print(str(aux[1][6068])+'dB')
    return data

