import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time



def read_brams(roach, bram_list,awidth,dwidth,dtype):
    re_list = []
    im_list = []
    for bram in bram_list:
        real, img = calan.read_deinterleave_data(roach, bram, dfactor=2,
                awidth=awidth, dwidth=dwidth, dtype=dtype)
        re_list.append(real)
        im_list.append(img)
    re_data = np.vstack(re_list).reshape((-1,), order='F')
    im_data = np.vstack(im_list).reshape((-1,), order='F')
    return re_data, im_data


def compute_calibration(roach, pow0_info, pow1_info,cross_info, channels=2048):
    """ xx_info: dictionary with the fields
            brams,bitwidth,addrwidth,dtype
        n_frames: number of fft frames that you read in one iter
    """

    print('Singled ended data0')
    aa = calan.read_interleave_data(roach, pow0_info['brams'], pow0_info['addrwidth'],
            pow0_info['bitwidth'], pow0_info['dtype'])
    print('Singled ended data1')
    bb = calan.read_interleave_data(roach, pow1_info['brams'], pow1_info['addrwidth'],
            pow1_info['bitwidth'], pow1_info['dtype'])
    print('Cross data')
    ab_re = calan.read_interleave_data(roach, cross_info['bram_re'], cross_info['addrwidth'],
            cross_info['bitwidth'], cross_info['dtype'])
    ab_im = calan.read_interleave_data(roach, cross_info['bram_im'], cross_info['addrwidth'],
            cross_info['bitwidth'], cross_info['dtype'])
    ab = ab_re+1j*ab_im
    ab_ratio = -ab/bb #ab*/bb* = a/b
    return ab_ratio, ab, aa, bb
    

def get_raw_spect(roach, pow0_info, pow1_info,channels=2048):
    roach.write_int('cnt_rst', 2)
    roach.write_int('cnt_rst', 0)
    time.sleep(0.5)
    re0, im0 = read_brams(roach, pow0_info['brams'], pow0_info['addrwidth'],
            pow0_info['bitwidth'], pow0_info['dtype'])
    data0 = re0+1j*im0
    data0 = data0.reshape([-1,channels])
    re1, im1 = read_brams(roach, pow1_info['brams'], pow1_info['addrwidth'],
            pow1_info['bitwidth'], pow1_info['dtype'])
    data1 = re1+1j*im1
    data1 = data1.reshape([-1,channels])
    return data0,data1



def get_phase(roach,adc0_info, adc1_info,channels=2048):
    data0, data1 = get_raw_spect(roach, adc0_info, adc1_info,
            channels=channels)
    corr_data = data0*np.conj(data1)
    angle = np.mean(np.angle(corr_data.T), axis=1)
    return angle


def load_constants(roach, constants, cal_info):
    """cal_info: dict with fields
        bram_re:list of the real part
        bram_im:list of the img part
        bitwidth
        bit_pt
    """
    const_real = calan.float2fixed(constants.real,
            cal_info['bitwidth'], cal_info['bit_pt'])
    const_imag = calan.float2fixed(constants.imag,
            cal_info['bitwidth'], cal_info['bit_pt'])
    calan.write_interleaved_data(roach, cal_info['bram_re'], const_real)
    calan.write_interleaved_data(roach, cal_info['bram_im'], const_imag)


def get_synth(roach, constants, cal_info, synth_info, sleep_time=5):
    """ cal_info: dict with fields
            bram_re:list of the real part
            bram_im:list of the img part
            bitwidth
            bit_pt
        synth_info: dict with the fields
            brams,bitwidth,addrwidth,dtype
    """
    load_constants(roach, constants, cal_info)
    time.sleep(sleep_time)
    synth_data = calan.read_interleave_data(roach, synth_info['brams'],
            synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])
    return synth_data



def synth_meas(roach, ab_ratios, cal0_info, synth_info, channels):
    """ 
        Makes a mesure synthesizing 4 types of data, obtain the LO and RF parts
        of the signals with calibrated and ideal constants
        roach   :   roach handler
        ab_ratio:   calibration constants
    """
    print('Ideal constants for RF signal (1)')
    const = np.ones(channels, dtype=complex)
    ideal_rf = get_synth(roach, const, cal0_info, synth_info)
    
    print('Ideal constants for LO signal (-1)')
    const = -1*np.ones(channels, dtype=complex)
    ideal_lo = get_synth(roach, const, cal0_info, synth_info)
    
    print('Cal constants for RF signal')
    const = ab_ratios
    cal_rf = get_synth(roach, const, cal0_info, synth_info)

    print('Cal constants for LO signal')
    const = -ab_ratios
    cal_lo = get_synth(roach, const, cal0_info, synth_info)

    return ideal_rf, ideal_lo, cal_rf, cal_lo

def hot_cold_measure(roach, rigol, adc0_info, adc1_info, cal0_info, synth_info,
        channels, cal_iters, n_frames, rf_off=0):
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
    print('Initializing constants to 1')
    const = np.ones(channels, dtype=complex)
    load_constants(roach, const, cal0_info)
     
    rigol.turn_output_off(1)
    if(rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn off!')
    if(rf_off!=0):
        rigol.turn_output_off(2)
        if(rigol.get_status(2)):
            raise Exception('Channel 2 doesnt turn off!')
    print('Computing constants')
    ab_ratios,ab,aa,bb = compute_calibration(roach, adc0_info, adc1_info,
        channels=channels, iters=cal_iters, n_frames=n_frames)

    #cold source 
    print('Cold Measuremet')
    rigol.turn_output_on(2)
    if(not rigol.get_status(2)):
        raise Exception('Channel 2 doesnt turn on!')

    cold_ideal_rf, cold_ideal_lo, cold_cal_rf, cold_cal_lo = synth_meas(roach, ab_ratios, 
                                                                        cal0_info, synth_info, channels)

    print('Hot Measurment')
    rigol.turn_output_on(1)
    if(not rigol.get_status(1)):
        raise Exception('Channel 1 doesnt turn on!')
    time.sleep(1.5)
    hot_ideal_rf, hot_ideal_lo, hot_cal_rf, hot_cal_lo = synth_meas(roach, ab_ratios, 
                                                                        cal0_info, synth_info, channels)
    return [cold_ideal_rf, cold_ideal_lo, cold_cal_rf, cold_cal_lo,
            hot_ideal_rf, hot_ideal_lo, hot_cal_rf, hot_cal_lo, ab_ratios]


def turn_on_sequence(rigol, rs_supply, psg_source, sleep_time=0.5):
    """ 
        rigol channels are connected this way
          1: noise source (for the RF branch)
          2: rf amplifier
          3: if amplifier

        rs power supply channels 
          1: noise source (for the LO) 
          2: LO noise amps 
          3: Claudio amp (12V)
    """
    print('set voltages...')
    rigol.set_voltage(1,28)
    rigol.set_voltage(2,5)
    rigol.set_voltage(3,5)
    
    rs_supply.set_voltage(1, 28)
    rs_supply.set_voltage(2, 5)
    rs_supply.set_voltage(3, 12)
    
    rs_supply.set_current(1, 1)
    rs_supply.set_current(2, 3)
    rs_supply.set_current(3, 0.6)
    
    print('checking voltages')
    ###carefull, the rs dont allow to check the voltages and currents!
    v1 = rigol.get_voltage(1)
    v2 = rigol.get_voltage(2)
    v3 = rigol.get_voltage(3)

    if([v1,v2,v3] != [28,5,5]):
        raise Exception('Read voltages dont match!!')
    
    print('Turning on IF amplifiers')
    rigol.turn_output_on(3)
    time.sleep(sleep_time)
    state = rigol.get_status(3)
    if(not state):
        raise Exception('The channel 3 doesnt turn on!')
    print('Turning on LO')
    psg_source.turn_output_on()
    time.sleep(sleep_time)
    state = psg_source.instr.query('outp?')
    if(state == '0\n'):
        raise Exception('PSG doesnt turn on!')
    print('Turning on RF amplifiers')
    rigol.turn_output_on(2)
    time.sleep(sleep_time)
    state = rigol.get_status(2)
    if(not state):
        raise Exception('The channel 2 doesnt turn on!')


def turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=0.5):
    """ 
        rigol channels are connected this way
          1: noise source (for the RF branch)
          2: rf amplifier
          3: if amplifier

        rs power supply channels 
          1: noise source (for the LO) 
          2: LO noise amps 
          3: Claudio amp (12V)
    """
    print('Turning off LO noise')
    rs_supply.turn_output_off(1)
    time.sleep(sleep_time)

    print('Turning off LO amps')
    rs_supply.turn_output_off(2)
    time.sleep(sleep_time)

    print('Turning off ZVA')
    rs_supply.turn_output_off(3)
    time.sleep(sleep_time)
    
    print('Turning off RF Noise')
    rigol.turn_output_off(1)
    time.sleep(sleep_time)
    state = rigol.get_status(1)
    if(state):
        raise Exception('The channel 1 doesnt turn off!')

    print('Turning off RF amplifiers')
    rigol.turn_output_off(2)
    time.sleep(sleep_time)
    state = rigol.get_status(2)
    if(state):
        raise Exception('The channel 2 doesnt turn off!')
    print('Turning off LO')
    psg_source.turn_output_off()
    time.sleep(sleep_time)
    state = psg_source.instr.query('outp?')
    if(state == '1\n'):
        raise Exception('PSG doesnt turn off!')
    print('Turning off IF amplifiers')
    rigol.turn_output_off(3)
    time.sleep(sleep_time)
    state = rigol.get_status(3)
    if(state):
        raise Exception('The channel 3 doesnt turn off!')


def turn_on_LO_noise(rs_supply, sleep_time=0.1):
    print('Turning on ZVA amp')
    rs_supply.turn_output_on(3)
    time.sleep(sleep_time)
    print('Turning on LO noise amps')
    rs_supply.turn_output_on(2)
    time.sleep(sleep_time)
    print('Turning on LO noise')
    rs_supply.turn_output_on(1)
    time.sleep(sleep_time)

def turn_off_LO_noise(rs_supply, sleep_time=0.1):
    print('Turning off LO noise')
    rs_supply.turn_output_off(1)
    time.sleep(sleep_time)
    print('Turning off LO noise amps')
    rs_supply.turn_output_off(2)
    time.sleep(sleep_time)
    print('Turning off ZVA amp')
    rs_supply.turn_output_off(3)
    time.sleep(sleep_time)


def lnr_computation(hot_rf, cold_rf, hot_lo, cold_lo):
    lnr = 1.*(hot_rf-cold_rf)/(hot_lo-cold_lo)+1
    return lnr

def Tsys_computation(T_cold, T_hot, cold_pow, hot_pow):
    """
    """
    y_factor= 1.*np.sum(hot_pow)/np.sum(cold_pow)
    Te = (T_hot-y_factor*T_cold)/(y_factor-1)
    return Te
