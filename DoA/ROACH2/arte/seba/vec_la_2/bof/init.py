import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
import time, struct, snap_phase
import uesprit
from plot_corrs import plot_corrs
from plot_la import plot_la


roachIP = '192.168.0.40'
boffile = 'vec_linalg2.bof.gz'

signal_freq = 400
fs = 1200

doa_gain = 2**6#2**7
doa_gain1 = 2**9    #ufix32_9


#brams
spec0_brams = ['dout_0a_0','dout_0a_1','dout_0a_2','dout_0a_3']
spec1_brams = ['dout_0c_0','dout_0c_1','dout_0c_2','dout_0c_3']
r11_brams = ['r11_0','r11_1','r11_2','r11_3']
r12_brams = ['r12_0','r12_1','r12_2','r12_3']
r22_brams = ['r22_0','r22_1','r22_2','r22_3']
phase_brams = ['phase0','phase1','phase2','phase3']

roach = calan.initialize_roach(roachIP , boffile=boffile, upload=1)
roach.write_int('cnt_rst',3)
roach.write_int('acc_len',8)
roach.write_int('doa_acc',10)
roach.write_int('doa_gain', doa_gain)
roach.write_int('doa_gain1',doa_gain1)
roach.write_int('cnt_rst',0)


time.sleep(0.5)
roach.write_int('doa_en',1)
"""
fig = plt.figure()
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)

frec = np.linspace(0,600, 2048,endpoint=0)
spec0 = calan.read_interleave_data(roach, spec0_brams, 9, 64, dtype='>u8')
spec1 = calan.read_interleave_data(roach, spec1_brams, 9, 64, dtype='>u8')
r11 = calan.read_interleave_data(roach, r11_brams, 9, 16, dtype='>u4')
r22 = calan.read_interleave_data(roach, r22_brams, 9, 16, dtype='>u4')
r12 = calan.read_interleave_data(roach, r12_brams, 9, 16, dtype='>i4')

ax1.plot(frec[5:],spec0[5:]); ax1.grid();
ax2.plot(frec[5:],r11[5:]); ax2.grid();
ax3.plot(frec[5:],spec1[5:]); ax3.grid();
ax4.plot(frec[5:],r22[5:]); ax4.grid();
ax5.plot(frec[5:],r12[5:]); ax5.grid();
plt.show()
"""

plot_la(roach)

plot_corrs(roach)



iters = 5
angs = np.zeros(iters)
print("Classical phase")
for i in range(iters):
    angs[i] = snap_phase.snap_phase(roach, signal_freq, fs)
ang = np.mean(angs)
print("phase between adcs: %.4f" %ang)


v1_mu1 = np.zeros(iters)
v1_mu2 = np.zeros(iters)
print("Version 1:")
for i in range(iters):
    u1_mu1, u1_mu2, u1_l1,u1_l2 = uesprit.uesprit_v1(roach)
    v1_mu1[i] = u1_mu1; v1_mu2[i] = u1_mu2    
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u1_mu1), np.rad2deg(u1_mu2)))    #check!!


samples = 4
v3_mu1 = np.zeros(iters)
v3_mu2 = np.zeros(iters)
print("Version 3:")
for i in range(iters):
    u3_mu1, u3_mu2,u3_l1,u3_l2= uesprit.uesprit_v3(roach, signal_freq, samples=samples, fs=fs)
    v3_mu1[i] = u3_mu1; v3_mu2[i] = u3_mu2
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u3_mu1), np.rad2deg(u3_mu2)))    #check!!
