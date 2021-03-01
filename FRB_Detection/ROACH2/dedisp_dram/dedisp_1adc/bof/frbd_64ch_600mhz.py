import calandigital as cd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import dram_class, time

# communication parameters
#roach_ip = '192.168.1.12'
roach_ip = '192.168.1.14'
boffile  = 'frbd_64ch_600mhz_2.fpg'
#boffile  = None

# model parameters
#sock_addr = ('192.168.2.2', 1234)
sock_addr = ('10.0.0.29', 1234)
gain = 2**18
adc_bits  = 8
bandwidth = 600.0 # MHz
fcenter   = 1500 # MHz
nchnls    = 64
count_reg = "cnt_rst"
acc_regs = ["acc_len0", "acc_len1", "acc_len2", "acc_len3", 
    "acc_len4", "acc_len5", "acc_len6", "acc_len7", 
    "acc_len8", "acc_len9", "acc_len10"]
det_regs = ["frb_detect0", "frb_detect1", "frb_detect2", 
    "frb_detect3", "frb_detect4", "frb_detect5", "frb_detect6",
    "frb_detect7", "frb_detect8", "frb_detect9", 
    "frb_detect10"]
bram_list = ["ACC0", "ACC1", "ACC2", "ACC3", "ACC4", "ACC5", 
    "ACC6", "ACC7", "ACC9", "ACC9", "ACC10"]
bram_addr_width = 10 # bits
bram_word_width = 32 # bits
bram_data_type  = '>u4'

# experiment parameters
k     = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
DMs   = range(0, 550, 50)
DMs[0] = 20
#ylim  = (55,75)
##thi valeues are measured....test only!!!
ylims = [(60,65), (60,65), (65,70), (67,72), (68,73), (68,73), 
        (70,75), (70, 75), (70,75), (70,75), (70, 75)]

#thetas = [63+2, 63+2, 66+2, 67+2, 69+2,70+2, 70.8+2,
#         71.4+2, 72.4+2, 72.4+2, 72.8+2, 73+2]

thetas = [63+8, 63+8, 66+8, 67+8, 69+8,70+8, 70.8+8,
         71.4+8, 72.4+8, 72.4+8, 72.8+8, 73+8]



# derivative parameters
flow    = fcenter - bandwidth/2 # MHz
fhigh   = fcenter + bandwidth/2 # MHz
iffreqs = np.linspace(0, bandwidth, nchnls, endpoint=False)
rffreqs = iffreqs + flow
Ts      = 1/(2*bandwidth) # us
tspec   = Ts*nchnls # us

def main():
    # initialize roach
    roach = cd.initialize_roach(roach_ip, boffile=boffile, upload=1)

    # create figures
    fig, lines = create_figure()
        
    # initial setting of registers
    print("Setting accumulation registers.")
    accs = compute_accs()
    for acc, acc_reg in zip(accs, acc_regs):
        roach.write_int(acc_reg, acc)
    roach.write_int('acc_len',1) #the debuging one
    roach.write_int('gain', gain)
    
    print('writing theta (for testing only)!')
    for i in range(11):
        roach.write_int('theta'+str(i), 10**(thetas[i]/10.))
    


    print("Initializing DRAM")
    dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr, n_pkt=20)
    time.sleep(0.5)
    dram_ring.init_ring()
    roach.write_int('control', 5)
    time.sleep(3)
    print("Resseting counter registers.")
    roach.write_int(count_reg, 1)
    roach.write_int(count_reg, 0)
    print("done.")

    # animation definition
    def animate(_):
        for line, bram in zip(lines, bram_list):
            # get spectral data
            frbdata = cd.read_data(roach, bram, 
                bram_addr_width, bram_word_width,   
                bram_data_type)
            frbdata = 10*np.log10(frbdata+1)
            line.set_data(range(len(frbdata)),frbdata)
        return lines

    ani = FuncAnimation(fig, animate, blit=True)
    plt.show()
    resp = raw_input('Read dram?(y/n)')
    if(resp=='y'):
        print("reading dram data")
        roach.write_int('control', 0)
        dram_ring.reading_dram()
    dram_ring.close_socket()



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
        ax.set_xlim(0, 2**bram_addr_width)
        if i in [0,3,6,9]:
            ax.set_ylabel('Power [dB]')
        ax.set_title("DM: " + str(dm))
        print(i)
        ax.set_ylim(ylims[i])
        ax.grid()
        line, = ax.plot([], [], animated=True)
        ax.plot([0,2**bram_addr_width], [thetas[i], thetas[i]])
        lines.append(line)

    return fig, lines

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
    accs[0] = accs[1]
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

if __name__ == '__main__':
    main()
