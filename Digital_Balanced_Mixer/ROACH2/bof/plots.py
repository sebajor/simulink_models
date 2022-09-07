import numpy as np
import sys
from functs import *
import os


#13.5GHz
[Te_cal_rf, Te_nolo_cal_rf, 
 Te_ideal_rf, Te_nolo_ideal_rf, 
 Te_ana_rf, Te_nolo_ana_rf,
 Te_cal_rf_vec, Te_nolo_cal_rf_vec, 
 Te_ideal_rf_vec, Te_nolo_ideal_rf_vec,
 Te_ana_rf_vec, Te_nolo_ana_rf_vec] = sys_temp('13.30/lo_14.50.hdf5',13.7)#'complete_hot_cold/lo_14.00.hdf5', 13.7)

#temperature plots
freq = np.linspace(0, 1080, 2048, endpoint=0)
plt.plot(freq,Te_cal_rf_vec, label='calibrated')
plt.plot(freq,Te_ana_rf_vec, label='analog')
plt.plot(freq, Te_ideal_rf_vec, label='ideal')
plt.grid()
plt.ylabel('K')
plt.ylim(0, 10000)
plt.legend()
plt.title('LO 13.7GHz')
plt.show()
#plt.savefig('t_sys_13.svg')
plt.close()


"""
[Te_cal_rf, Te_nolo_cal_rf, 
 Te_ideal_rf, Te_nolo_ideal_rf, 
 Te_ana_rf, Te_nolo_ana_rf,
 Te_cal_rf_vec, Te_nolo_cal_rf_vec, 
 Te_ideal_rf_vec, Te_nolo_ideal_rf_vec,
 Te_ana_rf_vec, Te_nolo_ana_rf_vec] = sys_temp('15_3GHz/filt800_att10/hot_cold/lo_15.00.hdf5', 15.3)

#temperature plots
freq = np.linspace(0, 1080, 2048, endpoint=0)
plt.plot(freq,Te_cal_rf_vec, label='calibrated')
plt.plot(freq,Te_ana_rf_vec, label='analog')
plt.grid()
plt.ylabel('K')
plt.ylim(0, 8000)
plt.legend()
plt.title('LO 15.3GHz')
plt.savefig('t_sys_15.svg')
plt.close()
"""
