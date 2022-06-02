import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import ipdb
import matplotlib.patches as mpatches

def plot_dedisp_pow(_roach, DMs, _dedisp_brams, _thresh_brams):
    global data, roach, dedisp_brams, thresh_brams
    roach = _roach
    dedisp_brams = _dedisp_brams
    thresh_brams = _thresh_brams
    data = []
    y_lim = (50, 62.5)#(0, 50)
    fig = plt.figure()
    for i in range(4):
        ax = fig.add_subplot(2,2,i+1)
        ax.set_ylim(y_lim)
        ax.set_xlim(0, 2**10)
        ax.grid()
        ax.set_title('DM:'+str(DMs[i]))
        dat, = ax.plot([],[], lw=2)
        thresh, = ax.plot([],[],lw=2)
        data.append(dat); data.append(thresh)
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()

def init():
    for i in range(2*len(dedisp_brams)):
        data[i].set_data([],[])
    return data

def animate(i):
    """ I think the point are the same in the design, check!

    """
    for i in range(len(dedisp_brams)):
        dedisp_pow = calan.read_data(roach, dedisp_brams[i], 10,32,'>u4')
        thresh = calan.read_data(roach, thresh_brams[i], 10,32,'>u4')
        dedisp_pow = 10*np.log10(dedisp_pow+1)
        thresh = 10*np.log10(thresh+1)
        #dedisp_pow = dedisp_pow/2.**13
        #thresh = thresh/2.**13
        data[2*i].set_data(np.arange(2**10), dedisp_pow)
        data[2*i+1].set_data(np.arange(2**10), thresh)
    return data




