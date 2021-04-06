import corr, time, dram_class
import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
from plot2 import plot_spect
from frb_acc import plot_frb


roach_ip ='192.168.0.40'
boffile = 'dedisp.fpg'
gain = 2**18

adc_bits = 8
bw = 600.
fcenter = 1500
nchnls = 2048
count_reg = "cnt_rst"
acc_regs = ["acc_len0", "acc_len1", "acc_len2", "acc_len3"]
bram_list = ["ACC0", "ACC1", "ACC2", "ACC3"]
theta_list = ['theta0', 'theta1', 'theta2', 'theta3']


bram_addr_width = 10
bram_word_width = 32
bram_data_type = '>u4'


##ring buffer parameters
sock_addr = ('10.0.0.29', 1234)



k     = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]

DMs = [100, 200, 300, 400]
flow    = fcenter - bw/2 # MHz
fhigh   = fcenter + bw/2 # MHz
iffreqs = np.linspace(0, bw, nchnls/32, endpoint=False)
rffreqs = iffreqs + flow
Ts      = 1/(2*bw) # us
tspec   = Ts*nchnls # us


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
    
def compute_accs():
    binsize = iffreqs[1]
    fbin_low = rffreqs[-2]+binsize/2
    fbin_high = rffreqs[-1]+binsize/2
    accs = []
    for dm in DMs:
        disptime = disp_time(dm, fbin_low, fbin_high)
        acc = 1.*disptime*1e6/tspec
        accs.append(int(round(acc)))
    print('Computed accumulations: '+ str(accs))
    return accs

#roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=0)
roach = corr.katcp_wrapper.FpgaClient('192.168.0.40')
#roach.upload_program_bof(boffile, 3000, timeout=60)
time.sleep(1)

accs = compute_accs()
print(DMs)
print(accs)
for acc, acc_reg in zip(accs, acc_regs):
    roach.write_int(acc_reg, acc)

thetas = [61, 64, 66, 67]
for theta_reg, theta in zip(theta_list, thetas):
    roach.write_int(theta_reg, int(10**(theta/10.)))    ##fail mio, me falto un cast para
                                                        ##arreglar el pto que viene
                                                        ##desde el accumulador 


roach.write_int('cnt_rst',1)

print("Initializing DRAM")
dram_ring = dram_class.dram_ring(roach, sock_addr=sock_addr, n_pkt=20)
time.sleep(0.5)
dram_ring.init_ring()
roach.write_int('control1', 5)


roach.write_int('gain_adc', 2**18)
roach.write_int('gain', gain)
roach.write_int('acc_len',1)
roach.write_int('cnt_rst',0)



plot_spect(roach, [1200, 1800])
plot_frb(roach, thetas)

dump = raw_input('dump the data collected?(y/n)')
if(dump=='y'):
    print("reading dram data")
    roach.write_int('control1', 0)
    dram_ring.reading_dram()

dram_ring.close_socket()
