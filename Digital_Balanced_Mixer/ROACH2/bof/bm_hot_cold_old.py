import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time, h5py, os
from utils import *
from hyperparams import *
from calandigital.instruments.rigol_dp832 import rigol_dp832
from calandigital.instruments import generator
from calandigital.instruments.rs_hmp4040 import rs_hmp4040
from bm_full_meas import *
from functs import *


##before running this script you must have calibrated and sychronized the adcs!
##also the rigol channels are connected this way
##      1: noise source (for the RF branch)
##      2: rf amplifier
##      3: if amplifier
##
##rs power supply channels 
##      1: noise source (for the LO) 
##      2: LO noise amps 
##      3: Claudio amp (12V)


if __name__ == '__main__':

    #create the saving folder if it doesnt exist
    save_path = 'hot_cold_data'
    if(not os.path.exists(save_path)):
        os.makedirs(save_path)

    img_path = 'hot_cold_data/images'
    if(not os.path.exists(img_path)):
        os.makedirs(img_path)


    roach = calan.initialize_roach(roach_ip)
    time.sleep(1)
    roach.write_int('cnt_rst', 1)
    roach.write_int('syn_acc_len', syn_acc_len)
    roach.write_int('cal_acc_len', cal_acc_len)
    roach.write_int('cnt_rst',0)
    time.sleep(1)

    freq = np.linspace(0, bw, channels, endpoint=False)

    #connect to the rigol
    rigol = rigol_dp832(rigol_ip)
    
    #connect to the rs power supply
    rs_supply = rs_hmp4040(rs_ip, rs_port)
    ##check that is connected

    #connect to the psg
    psg_source = generator.create_generator(psg_info)
    ##initialize system

    lo_freqs = np.linspace(test_lo_freq[0], test_lo_freq[1], test_lo_freq[2])
    print(lo_freqs)

    lo_power = np.linspace(test_lo_power[0], test_lo_power[1], test_lo_power[2])
    print(lo_power)

    #initialize the constants
    print('Initializing constants to 1')
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
    load_constants(roach, const, cal1_info)

    print('Starting measurement !')
    turn_on_sequence(rigol,rs_supply, psg_source, sleep_time=3)

    for lo_freq in lo_freqs:
        freq_path = save_path+'/'+format(lo_freq, '.2f')
        if(not os.path.exists(freq_path)):
            os.makedirs(freq_path)
        print('LO freq %.2f' %lo_freq)
        psg_source.set_freq_ghz(lo_freq)
        for lo_pow in lo_power:
            print('LO power: %.4f \n' %lo_pow)
            psg_source.set_power_dbm(lo_pow)
            start = time.time()
            ####################################################################
            print('Turning on LO noise')
            turn_on_LO_noise(rs_supply, sleep_time=3)
            time.sleep(5)
            [cold_ideal_rf, cold_ideal_lo,cold_cal_rf, 
            cold_cal_lo, cold_pow0, cold_pow1, cold_cross,
            hot_ideal_rf, hot_ideal_lo, hot_cal_rf,
            hot_cal_lo, hot_pow0, hot_pow1, hot_cross,
            ab_ratios] = complete_measure(roach, rigol, pow0_info, pow1_info, cross_info,
                                          cal0_info, cal1_info, synth_info, 
                                          channels, cal_iters, n_frames,rf_off=rf_off )
            
            print('Turning off the LO Noise')    
            turn_off_LO_noise(rs_supply, sleep_time=3)
            time.sleep(5)
            #####################################################################
            [nolo_cold_ideal_rf, nolo_cold_ideal_lo, nolo_cold_cal_rf, 
            nolo_cold_cal_lo, nolo_cold_pow0, nolo_cold_pow1, nolo_cold_cross,
            nolo_hot_ideal_rf, nolo_hot_ideal_lo, nolo_hot_cal_rf,
            nolo_hot_cal_lo, nolo_hot_pow0, nolo_hot_pow1, nolo_hot_cross,
            nolo_ab_ratios
            ] = complete_measure(roach, rigol, pow0_info, pow1_info, cross_info,
                                                        cal0_info, cal1_info, synth_info, 
                                                        channels, cal_iters, n_frames,rf_off=rf_off, ratios=ab_ratios)
            ####################################################################
            f = h5py.File(freq_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'w') 
            dset0 = f.create_dataset('cold_ideal_rf', data=cold_ideal_rf)
            dset1 = f.create_dataset('cold_ideal_lo', data=cold_ideal_lo)
            dset2 = f.create_dataset('cold_cal_rf', data=cold_cal_rf)
            dset3 = f.create_dataset('cold_cal_lo', data=cold_cal_lo)
            dset4 = f.create_dataset('cold_pow0', data=cold_pow0)
            dset5 = f.create_dataset('cold_pow1', data=cold_pow1)
            dset6 = f.create_dataset('cold_cross', data=cold_cross, dtype=complex)

            dset7 = f.create_dataset('hot_ideal_rf', data=hot_ideal_rf)
            dset8 = f.create_dataset('hot_ideal_lo', data=hot_ideal_lo)
            dset9 = f.create_dataset('hot_cal_rf', data=hot_cal_rf)
            dsetA = f.create_dataset('hot_cal_lo', data=hot_cal_lo)
            dsetB = f.create_dataset('hot_pow0', data=hot_pow0)
            dsetC = f.create_dataset('hot_pow1', data=hot_pow1)
            dsetD = f.create_dataset('hot_cross', data=hot_cross, dtype=complex)
            dsetE = f.create_dataset('ab_ratios', data=ab_ratios, dtype=complex)


            dset0 = f.create_dataset('nolo_cold_ideal_rf', data=nolo_cold_ideal_rf)
            dset1 = f.create_dataset('nolo_cold_ideal_lo', data=nolo_cold_ideal_lo)
            dset2 = f.create_dataset('nolo_cold_cal_rf', data=nolo_cold_cal_rf)
            dset3 = f.create_dataset('nolo_cold_cal_lo', data=nolo_cold_cal_lo)
            dset4 = f.create_dataset('nolo_cold_pow0', data=nolo_cold_pow0)
            dset5 = f.create_dataset('nolo_cold_pow1', data=nolo_cold_pow1)
            dset6 = f.create_dataset('nolo_cold_cross', data=nolo_cold_cross, dtype=complex)

            dset7 = f.create_dataset('nolo_hot_ideal_rf', data=nolo_hot_ideal_rf)
            dset8 = f.create_dataset('nolo_hot_ideal_lo', data=nolo_hot_ideal_lo)
            dset9 = f.create_dataset('nolo_hot_cal_rf', data=nolo_hot_cal_rf)
            dsetA = f.create_dataset('nolo_hot_cal_lo', data=nolo_hot_cal_lo)
            dsetB = f.create_dataset('nolo_hot_pow0', data=nolo_hot_pow0)
            dsetC = f.create_dataset('nolo_hot_pow1', data=nolo_hot_pow1)
            dsetD = f.create_dataset('nolo_hot_cross', data=nolo_hot_cross, dtype=complex)
            dsetE = f.create_dataset('nolo_ab_ratios', data=ab_ratios, dtype=complex)
            
            f.close()
            end = time.time()-start
            print('The iteration took %.4f' %end)
    
    turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=3)
    os.system('play -nq -t alsa synth 1 sine 440')
    print('Now connect the 0 deg combiner')
    raw_input('Press enter when you are ready')

    turn_on_sequence(rigol,rs_supply, psg_source, sleep_time=3)
    
    for lo_freq in lo_freqs:
        psg_source.set_freq_ghz(lo_freq)
        freq_path = save_path+'/'+format(lo_freq, '.2f')
        for lo_pow in lo_power: 
            f = h5py.File(freq_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'a') 
            print('LO power: %.4f \n' %lo_pow)
            psg_source.set_power_dbm(lo_pow)

            start = time.time()
            ####################################################################
            print('Turning on LO noise')
            turn_on_LO_noise(rs_supply, sleep_time=2)
            time.sleep(2)
            [zero_cold_single0,zero_cold_pow0, 
             zero_hot_single0,zero_hot_pow0 ] = analog_measure(roach, rigol, pow0_info, 
                                                         pow1_info, cal0_info, cal1_info, 
                                                         synth_info, channels)
            #####################################################################
            print('Turning off LO noise')
            turn_off_LO_noise(rs_supply, sleep_time=2)
            time.sleep(2)
            [nolo_zero_cold_single0,
             nolo_zero_cold_pow0, 
             nolo_zero_hot_single0,
             nolo_zero_hot_pow0 ] = analog_measure(roach, rigol, pow0_info, 
                                                         pow1_info, cal0_info, cal1_info, 
                                                         synth_info, channels)
            ####################################################################
            dset0= f.create_dataset('zero_cold_single0', data=zero_cold_single0)
            dset1= f.create_dataset('zero_cold_pow0', data=zero_cold_pow0)
            dset2= f.create_dataset('zero_hot_single0', data=zero_hot_single0)
            dset3= f.create_dataset('zero_hot_pow0', data=zero_hot_pow0)

            dset4= f.create_dataset('nolo_zero_cold_single0', data=nolo_zero_cold_single0)
            dset5= f.create_dataset('nolo_zero_cold_pow0', data=nolo_zero_cold_pow0)
            dset6= f.create_dataset('nolo_zero_hot_single0', data=nolo_zero_hot_single0)
            dset7= f.create_dataset('nolo_zero_hot_pow0', data=nolo_zero_hot_pow0)
            f.close()
            end = time.time()-start
            print('The iteration took %.4f' %end)


    turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=3)
    os.system('play -nq -t alsa synth 1 sine 440')
    print('Now connect the 180 deg combiner')
    raw_input('Press enter when you are ready')

    turn_on_sequence(rigol,rs_supply, psg_source, sleep_time=3)

    for lo_freq in lo_freqs:
        psg_source.set_freq_ghz(lo_freq)
        freq_path = save_path+'/'+format(lo_freq, '.2f')
    
        for lo_pow in lo_power:
            f = h5py.File(save_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'a') 
            print('LO power: %.4f \n' %lo_pow)
            psg_source.set_power_dbm(lo_pow)

            start = time.time()
            ####################################################################
            print('Turning on LO noise')
            turn_on_LO_noise(rs_supply, sleep_time=3)
            time.sleep(2)
            [invert_cold_single0,invert_cold_pow0,
             invert_hot_single0, invert_hot_pow0 ] = analog_measure(roach, rigol, pow0_info, 
                                                         pow1_info, cal0_info, cal1_info, 
                                                         synth_info, channels)
            #####################################################################
            print('Turning off LO noise')
            turn_off_LO_noise(rs_supply, sleep_time=3)
            time.sleep(2)
            [nolo_invert_cold_single0, 
             nolo_invert_cold_pow0, 
             nolo_invert_hot_single0,
             nolo_invert_hot_pow0 ] = analog_measure(roach, rigol, pow0_info, 
                                                         pow1_info, cal0_info, cal1_info, 
                                                         synth_info, channels)
            #####################################################################
            dset0= f.create_dataset('invert_cold_single0', data=invert_cold_single0)
            dset1= f.create_dataset('invert_cold_pow0', data=invert_cold_pow0)
            dset2= f.create_dataset('invert_hot_single0', data=invert_hot_single0)
            dset3= f.create_dataset('invert_hot_pow0', data=invert_hot_pow0)
        
            dset4= f.create_dataset('nolo_invert_cold_single0', data=nolo_invert_cold_single0)
            dset5= f.create_dataset('nolo_invert_cold_pow0', data=nolo_invert_cold_pow0)
            dset6= f.create_dataset('nolo_invert_hot_single0', data=nolo_invert_hot_single0)
            dset7= f.create_dataset('nolo_invert_hot_pow0', data=nolo_invert_hot_pow0)
            f.close()
            end = time.time()-start
            print('The iteration took %.4f' %end)


    turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=3)
    os.system('play -nq -t alsa synth 1 sine 440')
    print('Connect the 2 IF inputs for the next iteration')

    freq = np.linspace(0,1080, 2048, endpoint=0)
    print('Making some plots')
    for lo_freq in lo_freqs:
        freq_path = save_path+'/'+format(lo_freq, '.2f')
        for lo_pow in lo_power:
            name = (freq_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5')
            [Te_cal_rf, Te_nolo_cal_rf, 
             Te_ideal_rf, Te_nolo_ideal_rf, 
             Te_ana_rf, Te_nolo_ana_rf,
             Te_cal_rf_vec, Te_nolo_cal_rf_vec, 
             Te_ideal_rf_vec, Te_nolo_ideal_rf_vec,
             Te_ana_rf_vec, Te_nolo_ana_rf_vec] = sys_temp(name,lo_freq)#'complete_hot_cold/lo_14.00.hdf5', 13.7)
            plt.plot(freq, Te_cal_rf_vec, label='calibrate')
            plt.plot(freq,Te_ana_rf_vec, label='analog')
            plt.plot(freq, Te_ideal_rf_vec, label='ideal')
            plt.grid()
            plt.ylabel('K')
            plt.ylim(0, 10000)
            plt.legend()
            fig_name = 'lo_'+format(lo_freq,'.2f')+'ghz_'+format(lo_pow,'.2f')+'_dbm'
            plt.title('LO '+format(lo_freq,'.2f')+'GHz: '+format(lo_pow,'.2f')+'dBm')
            plt.savefig(img_path+'/'+fig_name+'.svg')
            plt.close()
