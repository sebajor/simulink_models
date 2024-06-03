import numpy as np

test_parameters = {}

fpga_ip = '192.168.1.23'
fpg_file = 'rfsoc_if_calibrator.fpg'

lmx_file = 'rfsoc4x2_LMX_REF_245M76_OUT_491M52.txt'
lmk_file = 'rfsoc4x2_PL_122M88_REF_245M76.txt'

##calibration parameters
acc_len = 2**14
chnl_step = 32
sleeping = 0.01

##rf parameters
##correlator adc0-1
lo_gen_name_01 = 'TCPIP::192.168.1.33::INSTR'
rf_gen_name_01 = 'TCPIP::192.168.1.34::INSTR'
lo_freq_01 = 3.1     #GHz
lo_power01 = 0       #dBm
rf_power_01 =-12    #dBm

#correlator adc2-3
lo_gen_name_23 =  'TCPIP::192.168.1.33::INSTR'
rf_gen_name_23 = 'TCPIP::192.168.1.34::INSTR'
lo_freq_23 = 3.1    #GHz
lo_power_23 = -12#0     #dBm
rf_power_23 = 0#-12   #dBm


##options when characterizing the system
load_constant = True    
load_ideal = True
ideal_constant = 1j
inverted = True

##calibration folder
debug_folder = 'debug'  ##None if you dont want to store the debug data



#model parameters
adc_bits = 14
bandwidth = 3932.16/2
cal_acc_len = 'acc_len_cal'
synth_acc_len = 'acc_len_synth'
cnt_rst = 'cnt_rst'
bram_addr_width = 8
bram_data_width = 64
pow_dtype = '>u8'
cross_dtype = '>i8'
const_nbits = 16
const_binpt = 10


##
adc0_brams = ['adc0_'+str(i) for i in range(8)]
adc1_brams = ['adc1_'+str(i) for i in range(8)]
cross01_brams = ['corr01_'+str(i) for i in range(8)]
cal01_0 = ['calibrator_0_bram_mult_'+str(x) for x in range(8)]
cal01_1 = ['calibrator_1_bram_mult_'+str(x) for x in range(8)]
synth01_0 = ['cal0_'+str(x) for x in range(8)]
synth01_1 = ['cal1_'+str(x) for x in range(8)]



nchannels = 2**bram_addr_width*len(adc0_brams)
if_freqs = np.linspace(0, bandwidth, nchannels, endpoint=False)
test_channels = range(1,nchannels, chnl_step)
if_test_freqs = if_freqs[test_channels]  #MHz
rf_freqs_usb_01 = lo_freq_01+(if_freqs/1e3)   #GHz
rf_freqs_lsb_01 = lo_freq_01-(if_freqs/1e3)   #GHz
dBFS = 6.02*adc_bits+1.76+10*np.log10(nchannels)

dss01 = {}
dss01['aa_brams'] = adc0_brams
dss01['bb_brams'] = adc1_brams
dss01['ab_brams'] = cross01_brams
dss01['cal0'] = cal01_0
dss01['cal1'] = cal01_1
dss01['rf_power'] = rf_power_01
dss01['rf_freqs'] = {}
dss01['rf_freqs']['usb'] = rf_freqs_usb_01
dss01['rf_freqs']['lsb'] = rf_freqs_lsb_01
dss01['lo'] = {}
dss01['lo']['genname'] = lo_gen_name_01
dss01['lo']['freq'] = lo_freq_01
dss01['lo']['power'] = lo_power01
dss01['rf'] = {}
dss01['rf']['genname'] = rf_gen_name_01
dss01['rf']['power'] = rf_power_01
dss01['synth0'] = synth01_0
dss01['synth1'] = synth01_1





##
adc2_brams = ['adc2_'+str(i) for i in range(8)]
adc3_brams = ['adc3_'+str(i) for i in range(8)]
cross23_brams = ['corr23_'+str(i) for i in range(8)]
cal23_0 = ['calibrator_2_bram_mult_'+str(x) for x in range(8)]
cal23_1 = ['calibrator_3_bram_mult_'+str(x) for x in range(8)]
synth23_0 = ['cal2_'+str(x) for x in range(8)]
synth23_1 = ['cal3_'+str(x) for x in range(8)]
#rf stuffs
rf_freqs_usb_23 = lo_freq_23+(if_freqs/1e3)   #GHz
rf_freqs_lsb_23 = lo_freq_23-(if_freqs/1e3)   #GHz

dss23 = {}
dss23['aa_brams'] = adc2_brams
dss23['bb_brams'] = adc3_brams
dss23['ab_brams'] = cross23_brams
dss23['cal0'] = cal23_0
dss23['cal1'] = cal23_1
dss23['rf_power'] = rf_power_23
dss23['rf_freqs'] = {}
dss23['rf_freqs']['usb'] = rf_freqs_usb_23
dss23['rf_freqs']['lsb'] = rf_freqs_lsb_23
dss23['lo'] = {}
dss23['lo']['genname'] = lo_gen_name_23
dss23['lo']['freq'] = lo_freq_23
dss23['lo']['power'] = lo_power_23
dss23['rf'] = {}
dss23['rf']['genname'] = rf_gen_name_23
dss23['rf']['power'] = rf_power_23
dss23['synth0'] = synth23_0
dss23['synth1'] = synth23_1


###put all the info in test_parameters 
test_parameters["fpga_ip"] = fpga_ip
test_parameters["fpg_file"] = fpg_file
test_parameters["lmx_file"] = lmx_file
test_parameters["lmk_file"] = lmk_file
test_parameters["adc_bits"] = adc_bits
test_parameters["bandwidth"] = bandwidth
test_parameters["cal_acc_len"] = cal_acc_len
test_parameters["synth_acc_len"] = synth_acc_len
test_parameters["cnt_rst"] = cnt_rst
test_parameters["bram_addr_width"] = bram_addr_width
test_parameters["bram_data_width"] = bram_data_width
test_parameters["pow_dtype"] = pow_dtype
test_parameters["cross_dtype"] = cross_dtype
test_parameters["const_nbits"] = const_nbits
test_parameters["const_binpt"] = const_binpt
test_parameters["dss01"] = dss01
test_parameters["dss23"] = dss23
test_parameters["acc_len"] = acc_len
test_parameters["chnl_step"] = chnl_step
test_parameters["sleeping"] = sleeping
test_parameters["load_constant"] = load_constant
test_parameters["load_ideal"] = load_ideal
test_parameters["nchannels"] = nchannels
test_parameters["if_freqs"] = if_freqs
test_parameters["test_channels"] = test_channels
test_parameters["if_test_freqs"] = if_test_freqs
test_parameters["dBFS"] = dBFS
test_parameters['debug_folder'] = debug_folder
test_parameters['ideal_constant'] = ideal_constant
test_parameters['inverted'] = inverted
