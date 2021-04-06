import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
from math import trunc

def plot_spect(_fpga,_bw):
    global data, fpga, freq0, freq1, bw
    bw = _bw
    freq0 = np.linspace(bw[0], bw[1], 2048, endpoint =False)
    freq1 = np.linspace(bw[0], bw[1], 64, endpoint=False)
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

    ax1.set_xlim(bw[0], bw[1])
    ax1.set_ylim(20, 120)
    ax2.set_xlim(bw[0], bw[1])
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
    d0_0 = np.array(struct.unpack('>512Q', fpga.read('spec1_0', 512*8)))
    d0_1 = np.array(struct.unpack('>512Q', fpga.read('spec1_1', 512*8)))
    d0_2 = np.array(struct.unpack('>512Q', fpga.read('spec1_2', 512*8)))
    d0_3 = np.array(struct.unpack('>512Q', fpga.read('spec1_3', 512*8)))
    
    d0 = np.vstack([d0_0,d0_1,d0_2,d0_3])
    d0 = np.transpose(d0).flatten()
    d0 = 10*np.log10(d0+1)
    
    red = np.array(struct.unpack('>64Q', fpga.read('small_spec1', 64*8)))
    d1 = 10*np.log10(red+1)
    return [d0, d1]




def animate(i):
    aux = get_data()
    data[0].set_data(freq0,aux[0])
    data[1].set_data(freq1, aux[1])
   # print(str(aux[1][6068])+'dB')
    return data

