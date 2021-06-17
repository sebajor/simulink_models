import calandigital as calan
import numpy as np
import matplotlib.pyplot as plt
import time, struct, snap_phase
from u_esprit import uesprit_v1, uesprit_v2, uesprit_v3
import plots_spect

##this model is to check that the system could get the relative phase
##when the input signal is cw


roachip = '192.168.0.40'
boffile = 'doa_debug.bof.gz'

gain = 2**12

signal_freq = 400
fs = 1200

roach = calan.initialize_roach(roachip , boffile=boffile, upload=1)
roach.write_int('cnt_rst',1)
roach.write_int('gain', gain)
roach.write_int('acc_len',8)
roach.write_int('cnt_rst',0)

#check plots to modify the gain if its needed
plots_spect.plots(roach,ylim=(-5,100))   

#get the phase between adcs usign snapshots
iters = 10
angs = np.zeros(iters)
print("Classical phase")
for i in range(iters):
    angs[i] = snap_phase.snap_phase(roach, signal_freq, fs)

ang = np.mean(angs)
print("phase between adcs: %.4f" %ang)

#version 1
# take the spectrums and correlations, and add them in sw then la
v1_mu1 = np.zeros(iters)
v1_mu2 = np.zeros(iters)
print("Version 1:")
for i in range(iters):
    u1_mu1, u1_mu2, l1,l2 = uesprit_v1(roach)
    v1_mu1[i] = u1_mu1; v1_mu2[i] = u1_mu2    
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u1_mu1/2.), np.rad2deg(u1_mu2)))    #check!!

#version 2
##takes the integrated spects, corrs from hw and then la
v2_mu1 = np.zeros(iters)
v2_mu2 = np.zeros(iters)
print("Version 2:")
for i in range(iters):
    u2_mu1, u2_mu2, l1,l2= uesprit_v2(roach)
    v2_mu1[i] = u2_mu1; v2_mu2[i] = u2_mu2    
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u2_mu1/2.), np.rad2deg(u2_mu2)))    #check!!



#version 1
# take the spectrums and correlations, collect just one channel and make a la 
samples = 32
v3_mu1 = np.zeros(iters)
v3_mu2 = np.zeros(iters)
print("Version 3:")
for i in range(iters):
    u3_mu1, u3_mu2,l1,l2= uesprit_v3(roach, signal_freq, samples=samples, fs=fs)
    v3_mu1[i] = u3_mu1; v3_mu2[i] = u3_mu2    
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u3_mu1/2.), np.rad2deg(u3_mu2)))    #check!!
    
