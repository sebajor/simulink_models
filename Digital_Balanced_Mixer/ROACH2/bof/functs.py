import numpy as np
import matplotlib.pyplot as plt
import h5py


def generate_lnr_plots(filename, lo_freq, saturate=None, absolute=None, discard=None,acc=4):
    """
    Generate LNR plots
    filename:   Name of the file that store the data
    lo_freq:    Used LO frequency
    saturate:   1 if you want to saturate lnr below zero
    absolute:   1 if you want to calculate the absolute value over the LNR 
    discard:    1 if you want to discard the points where the LNR <0
    acc:        how many neighbour points use to smooth the LNR curve
    """
    freq = np.linspace(0, 1080, 2048, endpoint=False)
    f = h5py.File(filename, 'r')
    rf = np.array(f['rf_ideal'])
    lo = np.array(f['lo_ideal'])
    nolo_rf = np.array(f['nolo_rf_ideal'])
    fig = plt.figure()
    plt.plot(freq, 10*np.log10(rf), label='RF')
    plt.plot(freq, 10*np.log10(lo), label='LO')
    plt.plot(freq, 10*np.log10(nolo_rf), label='RF no noise')
    plt.xlabel('MHz')
    plt.ylabel('Power dB')
    plt.ylim(40, 85)
    plt.title('Ideal constants, LO: %.2f GHz' %lo_freq)
    plt.grid()
    plt.legend(loc=1)
    plt.savefig('ideal'+str(int(lo_freq))+'.png', dpi=fig.dpi)
    plt.close()

    lnr_ideal = lnr_computation(rf, lo, nolo_rf, saturate=saturate, absolute=absolute)

    rf = np.array(f['rf_ana'])
    lo = np.array(f['lo_ana'])
    nolo_rf = np.array(f['nolo_rf_ana'])
    fig = plt.figure()
    plt.plot(freq, 10*np.log10(rf), label='RF')
    plt.plot(freq, 10*np.log10(lo), label='LO')
    plt.plot(freq, 10*np.log10(nolo_rf), label='RF no noise')
    plt.xlabel('MHz')
    plt.ylabel('Power dB')
    plt.ylim(40, 85)
    plt.title('Analog, LO: %.2f GHz' %lo_freq)
    plt.grid()
    plt.legend(loc=1)
    plt.savefig('cal'+str(int(lo_freq))+'.png', dpi=fig.dpi)

    lnr_ana = lnr_computation(rf, lo, nolo_rf, saturate=saturate, absolute=absolute)

    rf = np.array(f['rf_cal'])
    lo = np.array(f['lo_cal'])
    nolo_rf = np.array(f['nolo_rf_cal'])
    fig = plt.figure()
    plt.plot(freq, 10*np.log10(rf), label='RF')
    plt.plot(freq, 10*np.log10(lo), label='LO')
    plt.plot(freq, 10*np.log10(nolo_rf), label='RF no noise')
    plt.xlabel('MHz')
    plt.ylabel('Power dB')
    plt.ylim(40, 85)
    plt.title('calibrated constants, LO: %.2f GHz' %lo_freq)
    plt.grid()
    plt.legend(loc=1)
    plt.savefig('ana_'+str(int(lo_freq))+'.png', dpi=fig.dpi)
    plt.close()
    
    lnr_cal = lnr_computation(rf, lo, nolo_rf, saturate=saturate, absolute=absolute)
    
    fig = plt.figure()
    if(discard is not None):
        plt.plot(freq[lnr_cal>0], 10*np.log10(lnr_cal[lnr_cal>0]), label='calibrated')
        plt.plot(freq[lnr_ideal>0], 10*np.log10(lnr_ideal[lnr_ideal>0]), label='ideal')
        plt.plot(freq[lnr_ana>0], 10*np.log10(lnr_ana[lnr_ana>0]), label='analog')
    else:
        plt.plot(freq, 10*np.log10(lnr_cal), label='calibrated')
        plt.plot(freq, 10*np.log10(lnr_ideal), label='ideal')
        plt.plot(freq, 10*np.log10(lnr_ana), label='analog')
    
    plt.xlabel('MHz')
    plt.ylabel('dB')
    plt.ylim(10, 62)
    plt.title('LO noise rejection, LO: %.2f GHz' %(lo_freq))
    plt.grid()
    plt.legend(loc=1)
    plt.savefig('lnr_'+str(int(lo_freq))+'.png', dpi=fig.dpi)
    plt.close()

    f.close()

    fig = plt.figure()
    if(discard is not None):
        mask = (lnr_cal>0) & (lnr_ana>0)
        val = 10*(np.log10(lnr_cal[mask])-np.log10(lnr_ana[mask]))
        ind = len(val)//acc
        val_acc = np.mean(val[:int(ind*acc)].reshape([-1, acc]), axis=1)
        #freq_jump = len(freq)//len(val_acc)
        freq = np.linspace(0, 1080, len(val_acc), endpoint=False)
        plt.plot(freq, val_acc)
        plt.grid()
        plt.ylabel('dB')
        plt.xlabel('MHz')
        plt.title('Calibrated LNR - Analog LNR')
        plt.savefig('diff_lnr'+str(int(lo_freq))+'.png', dpi=fig.dpi)
        plt.close()
    else:
        plt.plot(freq, 10*(np.log10(lnr_cal)-np.log10(lnr_ana)))
        plt.grid()
        plt.ylabel('dB')
        plt.xlabel('MHz')
        plt.title('Calibrated LNR - Analog LNR')
        plt.savefig('diff_lnr'+str(int(lo_freq))+'.png', dpi=fig.dpi)
        plt.close()
    #plt.show()

def lnr_computation(rf, lo, nolo_rf, saturate=None, absolute=None):
    """
    Compute the LNR
    RF:         measure that adds coherently the two branches to enhace the RF signal.
    LO:         measure that adds in counter phase the two branches to enhance the LO noise.
    nolo_RF:    turn off the LO noise and add coherently the two branches.
    saturate:   1 if you want to saturate lnr below zero
    absolute:   1 if you want to calculate the absolute value over the LNR 
    """
    freq = np.linspace(0,1080, 2048, endpoint=False)
    lnr = 1.*(lo-nolo_rf)/(rf-nolo_rf)
    if(absolute is not None):
        lnr = 1.*(lo-nolo_rf)/np.abs(rf-nolo_rf)
    if(saturate is not None):
        lnr[lnr<0] = saturate
    return lnr


def sys_temp(filename, lo_freq):
    """
    Create the plots for the Hot-Cold test
    filename:   name of the file where the data is stored.
    lo_freq:    LO frequency
    """
    freq = np.linspace(0,1080, 2048, endpoint=False)
    noise_enr_db = 15  #goes from 14-16 dB
    #ENR = 10log10((T_on-T_off)/T0)
    T0 = 290
    T_hot = 10**(noise_enr_db/10.)*T0+T0
    T_cold = T0
    f = h5py.File(filename, 'r')

    #ideal
    cold_ideal_rf = np.array(f['cold_ideal_rf'])
    hot_ideal_rf  = np.array(f['hot_ideal_rf'])
    y_ideal_rf= 1.*np.sum(hot_ideal_rf)/np.sum(cold_ideal_rf)
    y_ideal_rf_vec = hot_ideal_rf/cold_ideal_rf
    Te_ideal_rf = (T_hot-y_ideal_rf*T_cold)/(y_ideal_rf-1)
    Te_ideal_rf_vec = (T_hot-y_ideal_rf_vec*T_cold)/(y_ideal_rf_vec-1)

    nolo_cold_ideal_rf = np.array(f['nolo_cold_ideal_rf'])
    nolo_hot_ideal_rf  = np.array(f['nolo_hot_ideal_rf'])
    y_nolo_ideal_rf= 1.*np.sum(nolo_hot_ideal_rf)/np.sum(nolo_cold_ideal_rf)
    y_nolo_ideal_rf_vec = nolo_hot_ideal_rf/nolo_cold_ideal_rf
    Te_nolo_ideal_rf = (T_hot-y_nolo_ideal_rf*T_cold)/(y_nolo_ideal_rf-1)
    Te_nolo_ideal_rf_vec = (T_hot-y_nolo_ideal_rf_vec*T_cold)/(y_nolo_ideal_rf_vec-1)


    #cal
    cold_cal_rf = np.array(f['cold_cal_rf'])
    hot_cal_rf  = np.array(f['hot_cal_rf'])
    y_cal_rf=   1.*np.sum(hot_cal_rf)/np.sum(cold_cal_rf)
    y_cal_rf_vec = hot_cal_rf/cold_cal_rf
    Te_cal_rf   = (T_hot-y_cal_rf*T_cold)/(y_cal_rf-1)
    Te_cal_rf_vec   = (T_hot-y_cal_rf_vec*T_cold)/(y_cal_rf_vec-1)

    nolo_cold_cal_rf = np.array(f['nolo_cold_cal_rf'])
    nolo_hot_cal_rf  = np.array(f['nolo_hot_cal_rf'])
    y_nolo_cal_rf=   1.*np.sum(nolo_hot_cal_rf)/np.sum(nolo_cold_cal_rf)
    y_nolo_cal_rf_vec = nolo_hot_cal_rf/nolo_cold_cal_rf
    Te_nolo_cal_rf   = (T_hot-y_nolo_cal_rf*T_cold)/(y_nolo_cal_rf-1)
    Te_nolo_cal_rf_vec = (T_hot-y_nolo_cal_rf_vec*T_cold)/(y_nolo_cal_rf_vec-1)


    #analog
    cold_ana_rf = np.array(f['zero_cold_pow0'])
    hot_ana_rf  = np.array(f['zero_hot_pow0'])
    y_ana_rf=   1.*np.sum(hot_ana_rf)/np.sum(cold_ana_rf)
    y_ana_rf_vec = hot_ana_rf/cold_ana_rf
    Te_ana_rf   = (T_hot-y_ana_rf*T_cold)/(y_ana_rf-1)
    Te_ana_rf_vec   = (T_hot-y_ana_rf_vec*T_cold)/(y_ana_rf_vec-1)

    nolo_cold_ana_rf = np.array(f['nolo_zero_cold_pow0'])
    nolo_hot_ana_rf  = np.array(f['nolo_zero_hot_pow0'])
    y_nolo_ana_rf=   1.*np.sum(nolo_hot_ana_rf)/np.sum(nolo_cold_ana_rf)
    y_nolo_ana_rf_vec = nolo_hot_ana_rf/nolo_cold_ana_rf
    Te_nolo_ana_rf   = (T_hot-y_nolo_ana_rf*T_cold)/(y_nolo_ana_rf-1)
    Te_nolo_ana_rf_vec   = (T_hot-y_nolo_ana_rf_vec*T_cold)/(y_nolo_ana_rf_vec-1)

    f.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.plot(freq, 10*np.log10(cold_cal_rf),  label='cold cal')
    ax1.plot(freq, 10*np.log10(hot_cal_rf),  label='hot cal')
    
    ax1.plot(freq, 10*np.log10(cold_ideal_rf), label='cold ideal')
    ax1.plot(freq, 10*np.log10(hot_ideal_rf),  label='hot ideal')

    ax1.plot(freq, 10*np.log10(cold_ana_rf), label='cold analog')
    ax1.plot(freq, 10*np.log10(hot_ana_rf),  label='hot analog')

    ax1.grid()
    ax1.set_ylabel('dB')
    ax1.set_ylim(40, 75)
    ax1.set_xlabel('MHz')
    ax1.set_title('Hot-cold with LO noise')
    ax1.legend()


    ax2.plot(freq, 10*np.log10(nolo_cold_cal_rf), label='cold cal')
    ax2.plot(freq, 10*np.log10(nolo_hot_cal_rf),  label='hot cal')
    
    ax2.plot(freq, 10*np.log10(nolo_cold_ideal_rf), label='cold ideal')
    ax2.plot(freq, 10*np.log10(nolo_hot_ideal_rf), label='hot ideal')

    ax2.plot(freq, 10*np.log10(nolo_cold_ana_rf), label='cold analog')
    ax2.plot(freq, 10*np.log10(nolo_hot_ana_rf), label='hot analog')

    ax2.grid()
    ax2.set_ylabel('dB')
    ax2.set_ylim(40, 75)
    ax2.set_xlabel('MHz')
    ax2.set_title('Hot-cold without LO noise')
    ax2.legend()

    plt.savefig('hot_cold_'+str(int(lo_freq))+'.png', dpi=fig.dpi)
    #plt.show()
    plt.close()


    return [Te_cal_rf, Te_nolo_cal_rf, Te_ideal_rf, Te_nolo_ideal_rf, Te_ana_rf, Te_nolo_ana_rf, 
            Te_cal_rf_vec, Te_nolo_cal_rf_vec, Te_ideal_rf_vec, Te_nolo_ideal_rf_vec, Te_ana_rf_vec, Te_nolo_ana_rf_vec]



