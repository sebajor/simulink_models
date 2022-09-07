import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time, h5py, os
from utils import *
from hyperparams import *
from calandigital.instruments.rigol_dp832 import rigol_dp832
from calandigital.instruments import generator
from calandigital.instruments.rs_hmp4040 import rs_hmp4040


##this code tries several LO power to make different hot cold test, this is
##in order to found the optimal operation point

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


def complete_hot_cold(roach, ab_ratios, pow0_info, pow1_info, cross_info,
        cal0_info, cal1_info, synth_info, channels, sleep_time=0.5):
    """ 
        Makes a mesure synthesizing 4 types of data, obtain the LO and RF parts
        of the signals with calibrated and ideal constants
        roach   :   roach handler
        ab_ratio:   calibration constants
    """
    print('Singled ended data0')
    pow0 = calan.read_interleave_data(roach, pow0_info['brams'], pow0_info['addrwidth'],
            pow0_info['bitwidth'], pow0_info['dtype'])
    
    print('Singled ended data1')
    pow1 = calan.read_interleave_data(roach, pow1_info['brams'], pow1_info['addrwidth'],
            pow1_info['bitwidth'], pow1_info['dtype'])
    
    print('Cross data')
    cross_re = calan.read_interleave_data(roach, cross_info['bram_re'], cross_info['addrwidth'],
            cross_info['bitwidth'], cross_info['dtype'])
    cross_im = calan.read_interleave_data(roach, cross_info['bram_im'], cross_info['addrwidth'],
            cross_info['bitwidth'], cross_info['dtype'])
    cross = cross_re+1j*cross_im
    
    #just in case
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal1_info)

    print('Ideal constants for RF signal (1)')
    const = np.ones(channels, dtype=complex)
    time.sleep(sleep_time)
    ideal_rf = get_synth(roach, const, cal0_info, synth_info)
    
    print('Ideal constants for LO signal (-1)')
    const = -1*np.ones(channels, dtype=complex)
    time.sleep(sleep_time)
    ideal_lo = get_synth(roach, const, cal0_info, synth_info)
    
    print('Cal constants for RF signal')
    const = ab_ratios
    time.sleep(sleep_time)
    cal_rf = get_synth(roach, const, cal0_info, synth_info)

    print('Cal constants for LO signal')
    const = -ab_ratios
    time.sleep(sleep_time)
    cal_lo = get_synth(roach, const, cal0_info, synth_info)

    #return ideal_rf, ideal_lo, cal_rf, cal_lo, single0, single1, fft0, fft1
    return ideal_rf, ideal_lo, cal_rf, cal_lo, pow0, pow1, cross


def complete_measure(roach, rigol, pow0_info, pow1_info, cross_info, cal0_info,
        cal1_info, synth_info, channels, cal_iters, n_frames, rf_off=0, ratios=None):
    """ roach       :   roach handler
        rigol       :   caladigital.instr rigol object (The channel 1 is connected to the RF noise source)
        adc0_info   :   dictionary with bram info
        adc1_info   :   dictionary with bram info
        channels    :   fft channels
        cal_iters   :   number of iteration for calibration
        n_frames    :   number of fft frames that you get per cal iteration
        rf_off      :   calibrate with the rf off
    """
    
    #to have a starting point
    #print('Initializing constants to 1')
    #const = np.ones(channels, dtype=complex)
    #load_constants(roach, const, cal0_info)
     
    rigol.turn_output_off(1)
    if(rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn off!')
    if(rf_off!=0):
        rigol.turn_output_off(2)
        if(rigol.get_status(2)):
            raise Exception('Channel 2 doesnt turn off!')
    if(ratios is None):
        print('Computing constants')
        ab_ratios,ab,aa,bb = compute_calibration(roach, pow0_info, pow1_info, cross_info)
    else:
        ab_ratios = ratios
    
    print('Cold Measuremet')
    rigol.turn_output_on(2)
    if(not rigol.get_status(2)):
        raise Exception('Channel 2 doesnt turn on!')

    [cold_ideal_rf, cold_ideal_lo, cold_cal_rf, 
     cold_cal_lo, cold_pow0, cold_pow1, cold_cross
     ] = complete_hot_cold(roach, ab_ratios, pow0_info, pow1_info, cross_info,
                            cal0_info, cal1_info, synth_info, channels)

    print('Hot Measurment')
    rigol.turn_output_on(1)
    if(not rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn on!')
    time.sleep(1.5)
    [hot_ideal_rf, hot_ideal_lo, hot_cal_rf, 
     hot_cal_lo, hot_pow0, hot_pow1, hot_cross
     ] = complete_hot_cold(roach, ab_ratios, pow0_info, pow1_info, cross_info,
                            cal0_info, cal1_info, synth_info, channels)

    return [cold_ideal_rf, cold_ideal_lo, cold_cal_rf, cold_cal_lo, cold_pow0, cold_pow1, cold_cross,
            hot_ideal_rf, hot_ideal_lo, hot_cal_rf, hot_cal_lo, hot_pow0, hot_pow1, hot_cross,
            ab_ratios]

def analog_measure(roach, rigol, pow0_info, pow1_info, cal0_info, cal1_info,
            synth_info, channels, sleep_time=0.5):
    rigol.turn_output_off(1)
    if(rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn off!')
    print('Cold Measuremet')
    rigol.turn_output_on(2)
    if(not rigol.get_status(2)):
        raise Exception('Channel 2 doesnt turn on!')
    time.sleep(3)
    
    print('Singled ended data0')
    const = np.zeros(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal1_info)
    time.sleep(sleep_time)
    cold_single0 = calan.read_interleave_data(roach, synth_info['brams'],
            synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])

    print('Power 0')
    cold_pow0 = calan.read_interleave_data(roach, pow0_info['brams'], pow0_info['addrwidth'],
            pow0_info['bitwidth'], pow0_info['dtype'])
    
    print('Hot Measurment')
    rigol.turn_output_on(1)
    if(not rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn on!')
    time.sleep(3)
    time.sleep(sleep_time)
    print('Singled ended data0')
    const = np.zeros(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal1_info)
    time.sleep(sleep_time)
    hot_single0 = calan.read_interleave_data(roach, synth_info['brams'],
            synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])

    print('Power 0')
    hot_pow0 = calan.read_interleave_data(roach, pow0_info['brams'], pow0_info['addrwidth'],
            pow0_info['bitwidth'], pow0_info['dtype'])
    return [cold_single0, cold_pow0, hot_single0, hot_pow0]


if __name__ == '__main__':
    #create the saving folder if it doesnt exist
    save_path = 'complete_hot_cold'
    if(not os.path.exists(save_path)):
        os.makedirs(save_path)

    img_path = 'complete_hot_cold/images'
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

    lo_power = np.linspace(test_lo_power[0], test_lo_power[1], test_lo_power[2])
    print(lo_power)

    #initialize the constants
    print('Initializing constants to 1')
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
    load_constants(roach, const, cal1_info)

    print('Starting measurement !')

    turn_on_sequence(rigol,rs_supply, psg_source, sleep_time=3)
    #digital measures
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
        f = h5py.File(save_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'w') 
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
    for lo_pow in lo_power:
        f = h5py.File(save_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'a') 
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
   

    print('Making some plots :P')
    for lo_pow in lo_power:
        f = h5py.File(save_path+'/lo_'+format(lo_pow, '.2f')+'.hdf5', 'r') 
        #rf signals
        cold_ideal_rf = np.array(f['cold_ideal_rf'])
        hot_ideal_rf = np.array(f['hot_ideal_rf'])
        cold_cal_rf = np.array(f['cold_cal_rf'])
        hot_cal_rf = np.array(f['hot_cal_rf'])
        zero_cold_single0 = np.array(f['zero_cold_pow0'])
        zero_hot_single0 = np.array(f['zero_hot_pow0'])
        #lo signals
        cold_ideal_lo = np.array(f['cold_ideal_lo'])
        hot_ideal_lo = np.array(f['hot_ideal_lo'])
        cold_cal_lo = np.array(f['cold_cal_lo'])
        hot_cal_lo = np.array(f['hot_cal_lo'])
        invert_cold_single0 = np.array(f['invert_cold_pow0'])
        invert_hot_single0 = np.array(f['invert_hot_pow0'])


        ##plots
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.set_ylim(35,80);    ax2.set_ylim(35,80)
        ax1.plot(freq, 10*np.log10(cold_ideal_rf), label='cold ideal')
        ax1.plot(freq, 10*np.log10(hot_ideal_rf), label='hot ideal')
        ax1.plot(freq, 10*np.log10(cold_cal_rf), label='cold cal')
        ax1.plot(freq, 10*np.log10(hot_cal_rf), label='hot cal')
        ax1.plot(freq, 10*np.log10(zero_cold_single0), label='cold analog')
        ax1.plot(freq, 10*np.log10(zero_hot_single0), label='hot analog')

        ax1.grid(); ax1.set_xlabel('MHz');  ax1.set_ylabel('dB')
        ax1.set_title('RF signal, LO:'+format(lo_pow, '.2f')+'dBm')
        handles, labels = ax1.get_legend_handles_labels()
        #ax1.legend()

        ax2.plot(freq, 10*np.log10(cold_ideal_lo), label='cold ideal')
        ax2.plot(freq, 10*np.log10(hot_ideal_lo), label='hot ideal')
        ax2.plot(freq, 10*np.log10(cold_cal_lo), label='cold cal')
        ax2.plot(freq, 10*np.log10(hot_cal_lo), label='hot cal')
        ax2.plot(freq, 10*np.log10(invert_cold_single0), label='cold analog')
        ax2.plot(freq, 10*np.log10(invert_hot_single0), label='hot analog')
        
        ax2.grid(); ax2.set_xlabel('MHz');  ax2.set_ylabel('dB')
        ax2.set_title('LO noise signal, LO:'+format(lo_pow, '.2f')+'dBm')
        ax2.legend(loc='lower right')

        #fig.legend(handles, labels, loc='lower right')
        plt.tight_layout()
        plt.savefig(img_path+'/lo'+format(lo_pow, '.2f')+'.png')
        plt.close()
        ##lnr plots
