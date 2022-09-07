import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time, h5py, os
from utils import *
from hyperparams import *
from calandigital.instruments.rigol_dp832 import rigol_dp832
from calandigital.instruments import generator
from calandigital.instruments.rs_hmp4040 import rs_hmp4040
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


def roach_meas(roach, ab_ratio, pow0_info, pow1_info, cross_info,
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


def differential_measurement(roach, rigol, pow0_info, pow1_info, cross_info, cal0_info,
        cal1_info, synth_info, channels, cal_iters, n_frames, rf_off=0, ratios=None, sleep_time=0.5):
    """ roach       :   roach handler
        rigol       :   caladigital.instr rigol object (The channel 1 is connected to the RF noise source)
        adc0_info   :   dictionary with bram info
        adc1_info   :   dictionary with bram info
        channels    :   fft channels
        cal_iters   :   number of iteration for calibration
        n_frames    :   number of fft frames that you get per cal iteration
        rf_off      :   calibrate with the rf off
    """
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
    time.sleep(sleep_time)
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

if __name__ == '__main__':
    save_path = 'hot_cold'
    if(not os.path.exists(save_path)):
        os.makedirs(save_path)

    img_path = 'hot_cold/images'
    if(not os.path.exists(img_path)):
        os.makedirs(img_path)

     

