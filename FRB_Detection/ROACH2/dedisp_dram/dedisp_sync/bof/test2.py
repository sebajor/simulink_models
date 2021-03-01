import calandigital as cd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, ipdb
import corr 

# communication parameters
roach_ip ='192.168.0.40'
boffile  = 'sync_frb.fpg'

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
bram_list = np.array(["ACC0", "ACC1", "ACC2", "ACC3", "ACC4", "ACC5",
    "ACC6", "ACC7", "ACC9", "ACC9", "ACC10"])
bram_addr_width = 10 # bits
bram_word_width = 32 # bits
bram_data_type  = '>u4'

# experiment parameters
k     = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
DMs   = range(0, 550, 50)
DMs[0] = 20
ylim  = (65,75)#(30,80)
theta = 70
#ploting time, it depdends of what DM are you looking at
refresh = np.array([0.5565, 1.3912, 2.7823, 4.1736, 5.5648, 6.9560, 8.3471,
           9.7383, 11.1295, 12.5208, 13.9119])

# derivative parameters
flow    = fcenter - bandwidth/2 # MHz
fhigh   = fcenter + bandwidth/2 # MHz
iffreqs = np.linspace(0, bandwidth, nchnls, endpoint=False)
rffreqs = iffreqs + flow
Ts      = 1/(2*bandwidth) # us
tspec   = Ts*nchnls # us




class ploting():
    def __init__(self, roach):
        self.roach = roach
        fig = plt.figure()
        self.axes = []
        for i in range(len(DMs)):
            axes.append(fig.add_subplot(4,3,i+1))
        fig.set_tight_layout(1)
        #set axes parameters
        self.lines = []
        for i,ax,dm in zip(range(len(DMs)), self.axes, DMs):
            if i in [0,3,6,9]:
                ax.set_ylabel('Power [dB]')
            ax.grid()
            line, = ax.plot([],[])  ##animated=True ?
            ax.axhline(theta, color='r')
            self.lines.append(line)
        self.y_data = np.zeros([len(DMs),2, 2**bram_addr_width])
        self.x_data = np.zeros([len(DMs),2, 2**bram_addr_width])



    def get_data(self):
        ind = self.roach.read('bram_done',4)
        print(ind)
        mask = np.unpackbits(np.frombuffer(ind, dtype='uint8'))[::-1] ##check!
        mask = mask[:len(DMs)]
        index = mask[::-1].nonzero()[0]
        print(mask)

        for i in range(len(index)):
            frbdata = cd.read_data(self.roach, bram_list[index[i]], bram_addr_width,
                                    bram_word_width, bram_data_type)
            frbdata = 10*np.log10(frbdata+1)
            self.y_data[index[i],0,:] = y_data[index[i],1,:]
            self.y_data[index[i],1,:] = frbdata
            self.x_data[index[i],0,:] = x_data[index[i],1,:]
            read_time = time.time()-1609813880 ##delete that number!
            self.x_data[index[i],1,:] = np.linspace(read_time-refresh[index[i]],
                                        read_time, 2**bram_addr_width)
            datx = self.x_data[index[i],:,:].flatten()
            daty = self.y_data[index[i],:,:].flatten()
            self.lines[index[i]].set_data(datx,daty)
            self.axes[index[i]].relim()
            self.axes[index[i]].autoscale_view(1,1,1)
        self.roach.write('rst_brams', ind)
        self.roach.write_int('rst_brams',0)
    
    def animate(i):
        
        

plt.ion()
plt.show()

    


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




###here start
roach = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(2)
print("Setting accumulation registers.")
accs = compute_accs()
for acc, acc_reg in zip(accs, acc_regs):
    roach.write_int(acc_reg, acc)
roach.write_int('acc_len',1) #the debuging one
roach.write_int('gain',gain)
print("Resseting counter registers.")
roach.write_int(count_reg, 1)
roach.write_int(count_reg, 0)
print("done.")












