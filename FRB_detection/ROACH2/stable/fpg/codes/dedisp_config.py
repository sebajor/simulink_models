import calandigital as calan
import time
import numpy as np


def disp_time(dm, flow, fhigh):
    """
    Compute dispersed FRB duration.
    :param dm: Dispersion measure in [pc*cm^-3]
    :param flow: Lower frequency of FRB in [MHz]
    :param fhigh: Higher frequency of FRB in [MHz]
    """
    # DM formula (1e-3 to change from ms to s)
    k = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
    td = k*dm*(flow**-2 - fhigh**-2)*1e-3
    return td


def compute_accs(fcenter, bw, nchnls, DMs):
    k= 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
    
    flow    = fcenter - bw/2 # MHz
    fhigh   = fcenter + bw/2 # MHz
    iffreqs = np.linspace(0, bw, nchnls/32, endpoint=False)
    rffreqs = iffreqs + flow
    Ts      = 1/(2*bw) # us
    tspec   = Ts*nchnls # us

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




def dedisp_config(roach, DMs, theta_values,offset, fcenter=1500, bw=600., nchnls=2048):
    """set the accumulation for each dedispersor and sets the theta value which is
        related with the detection threshold.

        threshold = avg+ theta*var ---> we would like to select theta in a way that
            theta*var ~ 5*std, it depends on the DM. You have to check the rigth values
            using for that the first dedispersor which allows you to directly take
            the avg and var.
    """ 
    accs = compute_accs(fcenter, bw, nchnls, DMs)
    print("accs:")
    print(accs)
    for i in range(len(accs)):
        roach.write_int('acc_number', i+1)
        time.sleep(0.5)
        roach.write_int('acc_dedisp', accs[i])
        roach.write_int('theta', theta_values[i])
        roach.write_int('thresh_offset', offset[i])
    roach.write_int('acc_number',0) #this value address nothing




