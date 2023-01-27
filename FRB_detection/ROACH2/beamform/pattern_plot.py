import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, rc

colors = ['purple', 'm']
markers = ['x', '^']

f = np.load('roach/pattern_data_horizontal_roach.npz', allow_pickle=True)
data1 = 10*np.log10(f['channel'])
theta = f['theta']

f = np.load('roach/pattern_data_vertical_roach.npz', allow_pickle=True)
data2 = 10*np.log10(f['channel'])


rad1 = data1 - np.max([data1, data2])
plt.figure(figsize = (10, 10))
ax = plt.subplot(111, polar = True)
ax.plot(theta, rad1, color = colors[0],lw = 3, ls = '-', label='horizontal')


theta = f['theta']
rad2 = data2 - np.max([data1, data2])
ax.plot(theta, rad2, color = colors[1], lw = 3, ls = '-', label='vertical')


ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(np.arange(0, 360, 30) * np.pi / 180)
plt.yticks(np.array([-30, -20, -10, -3, 0]))
ax.grid(True)
ax.set_rlabel_position(245)
plt.legend(loc = (0.85, -0.1))
plt.title('$f = $ 1575 MHz')
plt.show()



plt.figure(figsize = (10, 10))
ax2 = plt.subplot(111)
x = np.linspace(-180, 180, rad1.shape[0])
dat1 = np.roll(rad1,180)
dat2 = np.roll(rad2,180)
ax2.plot(x, dat1, color = colors[0],lw = 3, ls = '-', label='horizontal')
ax2.plot(x, dat2, color = colors[1], lw = 3, ls = '-', label='vertical')
plt.yticks(np.array([-30, -20, -10, -3, 0]))
ax2.grid(True)
plt.legend(loc = (0.85, -0.1))
plt.title('$f = $ 1575 MHz')
ax2.set_ylabel('Normalized Gain dB')
ax2.set_xlabel('Angle (deg)')

hpbw0 = np.argmin(np.abs(dat1[:180]+3))
hpbw1 = 180+np.argmin(np.abs(dat1[180:]+3))

ax2.axvline(x[hpbw0], ls='--', color=colors[0])
ax2.axvline(x[hpbw1], ls='--', color=colors[0])


hpbw0 = np.argmin(np.abs(dat2[:180]+3))
hpbw1 = 180+np.argmin(np.abs(dat2[180:]+3))

ax2.axvline(x[hpbw0], ls='--', color=colors[1])
ax2.axvline(x[hpbw1], ls='--', color=colors[1])





plt.show()
