import numpy as np
import calandigital as calan
import matplotlib.pyplot as plt
import time, struct, snap_phase
import uesprit

roachIP = '192.168.0.40'
boffile = 'sca_no_linalg.bof.gz'

signal_freq = 400
fs = 1200

#brams
spec0_brams = ['dout_0a_0','dout_0a_1','dout_0a_2','dout_0a_3']
spec1_brams = ['dout_0c_0','dout_0c_1','dout_0c_2','dout_0c_3']
r11_brams = ['r11_0','r11_1','r11_2','r11_3']
r12_brams = ['r12_0','r12_1','r12_2','r12_3']
r22_brams = ['r22_0','r22_1','r22_2','r22_3']



roach = calan.initialize_roach(roachIP , boffile=boffile, upload=1)
roach.write_int('cnt_rst',1)
roach.write_int('acc_len',8)
roach.write_int('doa_acc',10)
roach.write_int('doa_gain',2**8)
roach.write_int('cnt_rst',0)


time.sleep(0.5)
roach.write_int('doa_en',3)
roach.write_int('doa_en',1)

fig = plt.figure()
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)

frec = np.linspace(0,600, 2048,endpoint=0)
spec0 = calan.read_interleave_data(roach, spec0_brams, 9, 64, dtype='>u8')
spec1 = calan.read_interleave_data(roach, spec1_brams, 9, 64, dtype='>u8')
r11 = calan.read_interleave_data(roach, r11_brams, 9, 32, dtype='>u4')
r22 = calan.read_interleave_data(roach, r22_brams, 9, 32, dtype='>u4')
r12 = calan.read_interleave_data(roach, r12_brams, 9, 32, dtype='>i4')

ax1.plot(frec[5:],spec0[5:]); ax1.grid();
ax2.plot(frec[5:],r11[5:]); ax2.grid();
ax3.plot(frec[5:],spec1[5:]); ax3.grid();
ax4.plot(frec[5:],r22[5:]); ax4.grid();
ax5.plot(frec[5:],r12[5:]); ax5.grid();
plt.show()

iters = 30
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

#version 2
##takes the integrated spects, corrs from hw and then la
v2_mu1 = np.zeros(iters)
v2_mu2 = np.zeros(iters)
print("Version 2:")
for i in range(iters):
    u2_mu1, u2_mu2, u2_l1,u2_l2= uesprit.uesprit_v2(roach)
    v2_mu1[i] = u2_mu1; v2_mu2[i] = u2_mu2
    print("mu1: %.4f \t mu2: %.4f"%(np.rad2deg(u2_mu1), np.rad2deg(u2_mu2)))    #check!!
