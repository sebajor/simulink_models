import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import matplotlib.patches as mpatches
import calandigital as calan
#animation of the first dedispersor, the fpga trigger value, reads the 
#avg and the variance and calculate the rigth avg+alpha*std
#is intended to calibrate the theta values.


def test_theta(_roach, _std_coef, y_lim=(0,40)):
    global data, roach, std_coef
    roach = _roach; std_coef = _std_coef
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(y_lim)
    ax.set_xlim(0, 2**10)
    ax.grid()
    bl_patch = mpatches.Patch(color='blue', label='dedisp')
    or_patch = mpatches.Patch(color='orange', label='sw avg+$ \\alpha \\cdot$std')
    gr_patch = mpatches.Patch(color='green', label='hw avg+$ \\beta \\cdot$var')
    fig.legend(handles=[bl_patch, or_patch, gr_patch],loc='upper left')
    line, = ax.plot([],[], lw=2)
    hw_trig, = ax.plot([],[], lw=2)
    sw_trig, = ax.plot([],[], lw=2)
    data = [line, hw_trig, sw_trig]  
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.show()


def init():
    for i in range(3):
        data[i].set_data([],[])
    return data


def animate(i):
    dat = calan.read_data(roach, 'ACC0', 10, 32, '>u4')
    avg = calan.read_data(roach, 'avg0', 10, 32, '>u4')
    var = calan.read_data(roach, 'var0',  10, 64, '>u8')
    hw_thresh = calan.read_data(roach, 'thresh0',  10, 32, '>u4')
    
    #put the binary point in the right place
    avg = avg/2.**13
    var = var/2.**26
    dat = dat/2.**13
    hw_thresh = hw_thresh/2.**13

    std = np.sqrt(var)
    sw_thresh = avg+std_coef*std

    data[0].set_data(np.arange(2**10), dat)
    data[1].set_data(np.arange(2**10), hw_thresh)
    data[2].set_data(np.arange(2**10), sw_thresh)

    return data

