import corr, time, struct
import numpy as np
import matplotlib.pyplot as plt
from frb_acc_trigger import plot_frb
import calandigital as calan
import acc_trigger

roach_ip = '192.168.0.40'
boffile = 'trigger_logic.bof.gz'#.fpg'
gain = 2**12
thresh = 5#2.5 ##frb_thresh = avg+var*thresh*var

thresh0 = 5*0.5
thresh1 = 5*0.2

acc_len = 1024  ##just for view

thetas = [61, 64, 66, 67]   #ufix_32_12

adc_bits = 8
bw = 600.
fcenter = 1500
nchnls = 2048
count_reg = "cnt_rst"
#acc_regs = ["acc_len0", "acc_len1", "acc_len2", "acc_len3"]
#bram_list = ["ACC0", "ACC1", "ACC2", "ACC3"]
theta_list = ['theta0', 'theta1']


k= 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]

DMs = [100, 300]
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

roach = corr.katcp_wrapper.FpgaClient(roach_ip)
#roach.upload_program_bof(roach_ip, boffile, 3000, timeout=10)
time.sleep(2)
accs = compute_accs()
print(DMs)
print(accs)
for i in range(len(accs)):
    roach.write_int('acc_number',i+1)
    time.sleep(0.5)
    roach.write_int('acc_dedisp', accs[i])


roach.write_int('acc_number',3)
roach.write_int('acc_dedisp', accs[1])


roach.write_int('acc_number', 0)

#for theta_reg, theta in zip(theta_list, thetas):
#    roach.write_int(theta_reg, int(10**(theta/10.)))    ##fail mio, me falto un cast para
                                                        ##arreglar el pto que viene

thresh0_fix = calan.float2fixed(np.array(thresh0), 32, 12, signed=0)
thresh1_fix = calan.float2fixed(np.array(thresh1), 32, 12, signed=0)
roach.write_int('theta0', thresh0_fix)
roach.write_int('theta1', thresh1_fix)

roach.write_int('cnt_rst',1)    ##0:cnt_rst, 1:rst_detection


roach.write_int('gain', gain)
roach.write_int('acc_len',acc_len)
roach.write_int('cnt_rst',0)

plot_frb(roach, thresh)
acc_trigger.plot_frb(roach, thresh)
