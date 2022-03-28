import numpy as np


##hyperparamters
roach_ip = '192.168.1.12'
syn_acc_len = 1024
cal_acc_len = 1024

channels = 2048
bw = 1080

cal_iters = 10  #number of reading to calibrate
n_frames = 32   #number of fft frames that reads per iter

rf_off = 0   #if its distinct to 0, turn off the RF amps to calculate constants

#folder to save data
save_path = 'lo_pow_search'

##rigol info
rigol_ip = '192.168.1.38'
hot_channel = 1

#rs power supply info
rs_ip = '192.168.1.48'
rs_port = 4040

#psg info
"""
psg_info= { 'type':'visa',
            'connection': 'TCPIP::192.168.1.31::INSTR',
            'def_freq':13700,
            'def_power':6
        }
"""
psg_info= { 'type':'visa',
            'connection': 'TCPIP::192.168.1.31::INSTR',
            'def_freq':15300,
            'def_power':6
        }

test_lo_power = [14,15,3]#[11,13,3]#[9,13, 5] #low pow, high_pow, number of steps

##Noise source parameters
noise_enr_db = 15  #goes from 14-16 dB
#ENR = 10log10((T_on-T_off)/T0)
T0 = 290
T_hot = 10**(noise_enr_db/10.)*T0+T0
T_cold = T0


#roach power memories
pow0_info = { 'brams': 
                ['dout_a2_0', 'dout_a2_1', 'dout_a2_2', 
                'dout_a2_3', 'dout_a2_4', 'dout_a2_5', 
                'dout_a2_6', 'dout_a2_7'],
                'bitwidth': 64,
                'addrwidth':8,
                'dtype':'>Q'
        }

pow1_info = { 'brams': 
                ['dout_b2_0', 'dout_b2_1', 'dout_b2_2', 'dout_b2_3', 
                 'dout_b2_4', 'dout_b2_5', 'dout_b2_6', 'dout_b2_7'],
                'bitwidth': 64,
                'addrwidth':8,
                'dtype':'>Q'
        }

cross_info = { 'bram_re':
                ['dout_ab_re0','dout_ab_re1','dout_ab_re2','dout_ab_re3',
                 'dout_ab_re4','dout_ab_re5','dout_ab_re6','dout_ab_re7'
                    ],
                'bram_im' :
                ['dout_ab_im0','dout_ab_im1','dout_ab_im2','dout_ab_im3',
                 'dout_ab_im4','dout_ab_im5','dout_ab_im6','dout_ab_im7'
                    ],
                'bitwidth': 64,
                'addrwidth':8,
                'dtype':'>q'
        }



##calibration constants memories
cal0_info = {   'bram_re':[ 'bram_mult0_0_bram_re', 'bram_mult0_1_bram_re', 
                            'bram_mult0_2_bram_re', 'bram_mult0_3_bram_re', 
                            'bram_mult0_4_bram_re', 'bram_mult0_5_bram_re',
                            'bram_mult0_6_bram_re', 'bram_mult0_7_bram_re'],
                'bram_im':[ 'bram_mult0_0_bram_im', 'bram_mult0_1_bram_im', 
                            'bram_mult0_2_bram_im', 'bram_mult0_3_bram_im', 
                            'bram_mult0_4_bram_im', 'bram_mult0_5_bram_im',
                            'bram_mult0_6_bram_im', 'bram_mult0_7_bram_im'],
                'bitwidth': 32,
                'bit_pt': 27
        }

cal1_info = {   'bram_re':[ 'bram_mult1_0_bram_re', 'bram_mult1_1_bram_re', 
                            'bram_mult1_2_bram_re', 'bram_mult1_3_bram_re', 
                            'bram_mult1_4_bram_re', 'bram_mult1_5_bram_re',
                            'bram_mult1_6_bram_re', 'bram_mult1_7_bram_re'],
                'bram_im':[ 'bram_mult1_0_bram_im', 'bram_mult1_1_bram_im', 
                            'bram_mult1_2_bram_im', 'bram_mult1_3_bram_im', 
                            'bram_mult1_4_bram_im', 'bram_mult1_5_bram_im',
                            'bram_mult1_6_bram_im', 'bram_mult1_7_bram_im'],
                'bitwidth': 32,
                'bit_pt': 27
        }

##synth memories
synth_info = {   'brams': ['dout0_0','dout0_1','dout0_2','dout0_3',
                          'dout0_4','dout0_5','dout0_6','dout0_7'],
                'bitwidth': 64,
                'addrwidth': 8,
                'dtype':    '>Q'
        }
