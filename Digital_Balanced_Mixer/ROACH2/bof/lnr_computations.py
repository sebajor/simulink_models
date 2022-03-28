import numpy as np
import matplotlib.pyplot as plt
import h5py, os
from hyperparams import *


def lnr_computation(hot_rf, cold_rf, hot_lo, cold_lo):
    lnr = 1.*(hot_rf-cold_rf)/(hot_lo-cold_lo)
    return lnr

def Tsys_computation(T_cold, T_hot, cold_pow, hot_pow):
    """
    """
    y_factor= 1.*np.sum(hot_pow)/np.sum(cold_pow)
    Te = (T_hot-y_factor*T_cold)/(y_factor-1)
    return Te

def lnr_franco(lo, rf, rf_nolo):
    lnr = 1.*(lo-rf_nolo)/np.abs(rf-rf_nolo)
    return lnr
    

# I found the formulas here: http://rfic.eecs.berkeley.edu/142/pdf/NoiseFigLect.pdf
# https://www.testworld.com/wp-content/uploads/noise-figure-measurement-accuracy-the-y-factor-method.pdf


folder_name = 'complete_hot_cold'#_filt630_att10'

noise_enr_db = 15  #goes from 14-16 dB

#ENR = 10log10((T_on-T_off)/T0)
T0 = 290
T_hot = 10**(noise_enr_db/10.)*T0+T0
T_cold = T0


freq = np.linspace(0, bw, channels, endpoint=False)

dirs = os.listdir(folder_name)
for fil in dirs:
    if(fil.endswith('.hdf5')):
        f = h5py.File(folder_name+'/'+fil, 'r')

        #ideal
        cold_ideal_rf = np.array(f['cold_ideal_rf'])
        hot_ideal_rf  = np.array(f['hot_ideal_rf'])
        cold_ideal_lo = np.array(f['cold_ideal_lo'])
        hot_ideal_lo  = np.array(f['hot_ideal_lo'])
        
        y_ideal_rf= 1.*np.sum(hot_ideal_rf)/np.sum(cold_ideal_rf)
        y_ideal_lo= 1.*np.sum(hot_ideal_lo)/np.sum(cold_ideal_lo)
        Te_ideal_rf = (T_hot-y_ideal_rf*T_cold)/(y_ideal_rf-1)
        Te_ideal_lo = (T_hot-y_ideal_lo*T_cold)/(y_ideal_lo-1)
        
        ##calibrated 
        cold_cal_rf = np.array(f['cold_cal_rf'])
        hot_cal_rf  = np.array(f['hot_cal_rf'])
        cold_cal_lo = np.array(f['cold_cal_lo'])
        hot_cal_lo  = np.array(f['hot_cal_lo'])
        
        y_cal_rf=   1.*np.sum(hot_cal_rf)/np.sum(cold_cal_rf)
        y_cal_lo=   1.*np.sum(hot_cal_lo)/np.sum(cold_cal_lo)
        Te_cal_rf   = (T_hot-y_cal_rf*T_cold)/(y_cal_rf-1)
        Te_cal_lo   = (T_hot-y_cal_lo*T_cold)/(y_cal_lo-1)

        #analog
        cold_ana_rf = np.array(f['zero_cold_pow0'])
        hot_ana_rf  = np.array(f['zero_hot_pow0'])
        cold_ana_lo = np.array(f['invert_cold_pow0'])
        hot_ana_lo  = np.array(f['invert_hot_pow0'])

        y_ana_rf=   1.*np.sum(hot_ana_rf)/np.sum(cold_ana_rf)
        y_ana_lo=   1.*np.sum(hot_cal_lo)/np.sum(cold_ana_lo)
        Te_ana_rf   = (T_hot-y_ana_rf*T_cold)/(y_ana_rf-1)
        Te_ana_lo   = (T_hot-y_ana_lo*T_cold)/(y_ana_lo-1)


        
        ##no LO noise ideal
        nolo_cold_ideal_rf = np.array(f['nolo_cold_ideal_rf'])
        nolo_hot_ideal_rf  = np.array(f['nolo_hot_ideal_rf'])
        nolo_cold_ideal_lo = np.array(f['nolo_cold_ideal_lo'])
        nolo_hot_ideal_lo  = np.array(f['nolo_hot_ideal_lo'])
        
        y_nolo_ideal_rf= 1.*np.sum(nolo_hot_ideal_rf)/np.sum(nolo_cold_ideal_rf)
        y_nolo_ideal_lo= 1.*np.sum(nolo_hot_ideal_lo)/np.sum(nolo_cold_ideal_lo)
        Te_nolo_ideal_rf = (T_hot-y_nolo_ideal_rf*T_cold)/(y_nolo_ideal_rf-1)
        Te_nolo_ideal_lo = (T_hot-y_nolo_ideal_lo*T_cold)/(y_nolo_ideal_lo-1)
            
        ##no LO noise cal
        nolo_cold_cal_rf = np.array(f['nolo_cold_cal_rf'])
        nolo_hot_cal_rf  = np.array(f['nolo_hot_cal_rf'])
        nolo_cold_cal_lo = np.array(f['nolo_cold_cal_lo'])
        nolo_hot_cal_lo  = np.array(f['nolo_hot_cal_lo'])
        
        y_nolo_cal_rf=   1.*np.sum(nolo_hot_cal_rf)/np.sum(nolo_cold_cal_rf)
        y_nolo_cal_lo=   1.*np.sum(nolo_hot_cal_lo)/np.sum(nolo_cold_cal_lo)
        Te_nolo_cal_rf   = (T_hot-y_nolo_cal_rf*T_cold)/(y_nolo_cal_rf-1)
        Te_nolo_cal_lo   = (T_hot-y_nolo_cal_lo*T_cold)/(y_nolo_cal_lo-1)

        #no noise analog
        
        nolo_cold_ana_rf = np.array(f['nolo_zero_cold_pow0'])
        nolo_hot_ana_rf  = np.array(f['nolo_zero_hot_pow0'])
        nolo_cold_ana_lo = np.array(f['nolo_invert_cold_pow0'])
        nolo_hot_ana_lo  = np.array(f['nolo_invert_hot_pow0'])

        y_nolo_ana_rf=   1.*np.sum(nolo_hot_ana_rf)/np.sum(nolo_cold_ana_rf)
        y_nolo_ana_lo=   1.*np.sum(nolo_hot_cal_lo)/np.sum(nolo_cold_ana_lo)
        Te_nolo_ana_rf   = (T_hot-y_nolo_ana_rf*T_cold)/(y_nolo_ana_rf-1)
        Te_nolo_ana_lo   = (T_hot-y_nolo_ana_lo*T_cold)/(y_nolo_ana_lo-1)


        print('LO: '+str(fil.split('.hdf5')[0]))
        print('Te rf:')
        print('ideal: %.2f \t cal: %.2f \t analog: %.2f' %(Te_ideal_rf, Te_cal_rf, Te_ana_rf))
        print('nolo ideal: %.2f \t nolo cal: %.2f \t analog: %.2f\n' %(Te_nolo_ideal_rf, Te_nolo_cal_rf, Te_nolo_ana_rf))

        print('Te Lo')
        print('ideal: %.2f \t cal: %.2f \t analog: %.2f' %(Te_ideal_lo, Te_cal_lo, Te_ana_lo))
        print('nolo ideal: %.2f \t nolo cal: %.2f \t analog: %.2f \n' %(Te_nolo_ideal_lo, Te_nolo_cal_lo, Te_nolo_ana_lo))



        lnr_ideal = lnr_computation(hot_ideal_rf, cold_ideal_rf, 
                                    hot_ideal_lo, cold_ideal_lo)

        lnr_cal = lnr_computation(hot_cal_rf, cold_cal_rf, 
                                    hot_cal_lo, cold_cal_lo)
        
        lnr_ana = lnr_computation(hot_ana_rf, cold_ana_rf, 
                                    hot_ana_lo, cold_ana_lo)
        
        fig = plt.figure()
        plt.plot(freq, 10*np.log10(lnr_cal), label='cal')
        plt.plot(freq, 10*np.log10(lnr_ideal), label='ideal')
        plt.legend()
        plt.ylabel('lnr japos [dB]'); plt.xlabel('MHz')
        name = fil.strip('.hdf5').strip('lo_') 
        plt.title('lo :'+name)

        fig = plt.figure()
        ax1 = fig.add_subplot(121); ax2 = fig.add_subplot(122)
        
        lnr_cal_hot = lnr_franco(hot_cal_lo,hot_cal_rf, nolo_hot_cal_rf)
        lnr_cal_cold = lnr_franco(cold_cal_lo, cold_cal_rf, nolo_cold_cal_rf)
        lnr_ana_cold = lnr_franco(cold_ana_lo, cold_ana_rf, nolo_cold_ana_rf)
        
        lnr_ideal_hot = lnr_franco(hot_ideal_lo,hot_ideal_rf, nolo_hot_ideal_rf)
        lnr_ideal_cold = lnr_franco(cold_ideal_lo,cold_ideal_rf, nolo_cold_ideal_rf)
        lnr_ana_hot = lnr_franco(hot_ana_lo, hot_ana_rf, nolo_hot_ana_rf)


        ax1.plot(freq[lnr_cal_hot>0], 10*np.log10(lnr_cal_hot[lnr_cal_hot>0]), label='cal')
        ax1.plot(freq[lnr_ideal_hot>0], 10*np.log10(lnr_ideal_hot[lnr_ideal_hot>0]), label='ideal')
        ax1.plot(freq[lnr_ana_hot>0], 10*np.log10(lnr_ana_hot[lnr_ana_hot>0]), label='ana')
        ax1.set_ylabel('lnr hot'); ax1.set_xlabel('MHz')
        ax1.grid()
        

        ax2.plot(freq[lnr_cal_cold>0], 10*np.log10(lnr_cal_cold[lnr_cal_cold>0]), label='cal')
        ax2.plot(freq[lnr_ideal_cold>0], 10*np.log10(lnr_ideal_cold[lnr_ideal_cold>0]), label='ideal')
        ax2.plot(freq[lnr_ana_cold>0], 10*np.log10(lnr_ana_cold[lnr_ana_cold>0]), label='ana')
        ax2.set_ylabel('lnr cold'); ax2.set_xlabel('MHz')
        ax2.legend()
        ax2.grid()

        plt.show()
       

