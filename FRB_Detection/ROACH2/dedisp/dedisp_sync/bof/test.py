import calandigital as calan
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, ipdb, sys
import corr


roach_ip = '192.168.1.14'
boffile = 'dedisp_sync.fpg'

gain = 2**18
adc_bits = 8
bandwidth = 600.
fcenter = 1500
nchnls= 64
count_reg = "cnt_rst"

bram_list = np.array(["ACC0", "ACC1", "ACC2", "ACC3", "ACC4", "ACC5", 
    "ACC6", "ACC7", "ACC9", "ACC9", "ACC10"])

bram_addr_width = np.array([10,10,9,8,8,8,7,7,7,7,7])   #bits
bram_word_width = 32
bram_data_type = '>u4'

# experiment parameters
k     = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
DMs   = range(0, 550, 50)
DMs[0] = 20

#test values
ylims = [(57,62), (60,65), (65,70), (67,72), (68,73), (68,73), 
        (70,75), (70, 75), (70,75), (70,75), (70, 75)]

thetas = [63+2, 63+2, 66+2, 67+2, 69+2,70+2, 70.8+2,
         71.4+2, 72.4+2, 72.4+2, 72.8+2, 73+2]

# derivative parameters
flow    = fcenter - bandwidth/2 # MHz
fhigh   = fcenter + bandwidth/2 # MHz
iffreqs = np.linspace(0, bandwidth, nchnls, endpoint=False)
rffreqs = iffreqs + flow
Ts      = 1/(2*bandwidth) # us
tspec   = Ts*nchnls # us


##ploting time
refresh = np.array([0.5565, 1.3912, 1.39116544, 1.04338,1.39119,
        1.73899, 1.0433, 1.2172, 1.39119, 1.5650, 1.73898])

def create_figure():
    # create figure and axes
    #fig, axes = plt.subplots(4, 3, sharey=True, sharex=True)
    fig = plt.figure()
    axes = []
    for i in range(len(DMs)):
        axes.append(fig.add_subplot(4,3,i+1))
    fig.set_tight_layout(True)

    # set axes parameters
    lines = []
    for i,ax,dm in zip(range(len(DMs)),axes,DMs):
        #ax.set_xlim(0, 2**bram_addr_width)
        if i in [0,3,6,9]:
            ax.set_ylabel('Power [dB]')
        #ax.set_title("DM: " + str(dm))
        ax.set_ylim(ylims[i])
        ax.grid()
        #line, = ax.plot([], [], animated=True)
        line, = ax.plot([],[])
        ax.axhline(thetas[i], color='r')
        #ax.plot([0,2**bram_addr_width], [theta, theta])
        lines.append(line)
        
    return fig, np.array(lines), np.array(axes)

def compute_accs():
    """
    Compute the necessary accumulation for each DM for
    proper dedispersion.
    """
    # use higher frequency because it requires the lowest
    # accumulation
    binsize = iffreqs[1]
    fbin_low  = rffreqs[-2] + binsize/2
    fbin_high = rffreqs[-1] + binsize/2
    accs = []
    for dm in DMs:
        disptime = disp_time(dm, fbin_low, fbin_high)
        acc = disptime*1e6 / tspec
        accs.append(int(round(acc)))
    
    # adjust DM 0 to the next acc
    #accs[0] = accs[1]
    print("Computed accumulations: " + str(accs))
    return accs

def disp_time(dm, flow, fhigh):
    """
    Compute dispersed FRB duration.
    :param dm: Dispersion measure in [pc*cm^-3]
    :param flow: Lower frequency of FRB in [MHz]
    :param fhigh: Higher frequency of FRB in [MHz]
    """
    # DM formula (1e-3 to change from ms to s)
    td = k*dm*(flow**-2 - fhigh**-2)*1e-3
    return td


roach = corr.katcp_wrapper.FpgaClient(roach_ip)
#roach.upload_program_bof(boffile, 3000)
time.sleep(1)
print("Setting accumulation registers")
accs = compute_accs()
print("Set theta values (for testing only!)")
for i in range(len(accs)):
    roach.write_int('frb_addr', i)
    roach.write_int('acc_len_frb', accs[i])
    roach.write_int('theta_frb', thetas[i])

roach.write_int('acc_len',1)
roach.write_int('gain', gain)
print("Reset counters")
roach.write_int(count_reg,1)
roach.write_int(count_reg,0)
print("done")


global lines, x_data, y_data, axes, fig
fig, lines, axes = create_figure()
x_data = []
y_data = []
for i in range(11):
    x_data.append(np.zeros([2,2**bram_addr_width[i]]))
    y_data.append(np.zeros([2,2**bram_addr_width[i]]))

def get_data(roach):
    #ipdb.set_trace()
    ind_bin = roach.read('bram_done',4)
    mask = np.unpackbits(np.frombuffer(ind_bin, dtype='uint8'))[::-1]
    mask = mask[:len(DMs)]
    index = mask.nonzero()[0]
    for i in range(len(index)):
        ind = index[i]
        frbdata = calan.read_data(roach, bram_list[ind], bram_addr_width[ind],
                                bram_word_width, bram_data_type)
        frbdata = 10*np.log10(frbdata+1)
        y_data[ind][0,:] = y_data[index[i]][1,:]
        y_data[ind][1,:] = frbdata
        x_data[ind][0,:] = x_data[ind][1,:]
        read_time = time.time()-1609813880  #to normalize a little
        x_data[ind][1,:] = np.linspace(read_time-refresh[ind], read_time,
                                            2**bram_addr_width[ind])
        datx = x_data[ind].flatten()
        daty = y_data[ind].flatten()
        lines[index[i]].set_data(datx,daty)
        axes[index[i]].relim()
        axes[index[i]].autoscale_view(1,1,1)
    roach.write('rst_brams', ind_bin)
    roach.write_int('rst_brams',0)
    fig.canvas.draw()
    fig.canvas.flush_events()


plt.ion()
plt.show()
while(1):
    try:
        get_data(roach)
    except:
        sys.exit()
