import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
import time, h5py, os
from utils import *
from hyperparams import *
from calandigital.instruments.rigol_dp832 import rigol_dp832
from calandigital.instruments import generator
from calandigital.instruments.rs_hmp4040 import rs_hmp4040

def pseudo_lnr(rf, lo, nolo_rf):
    out = (lo-nolo_rf)/np.abs(rf-nolo_rf)
    return out

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

lo_pow = 15
lo_freq = 15.3 ##freq


save_path ='simple'
if(not os.path.exists(save_path)):
    os.makedirs(save_path)

img_path = save_path+'/images'
if(not os.path.exists(img_path)):
    os.makedirs(img_path)

if(rf_off!=0):
    name = 'lo'+format(lo_pow, '.2f')+'_rf_off'
else:
    name = 'lo'+format(lo_pow, '.2f')+'_rf_on'

#name = 'new_'+name
#name = 'long_cable_if_'+name
#name = name+'_filt_630_att10'
name = name+'_filt_800_att10_1attIF'

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
psg_source.set_freq_ghz(lo_freq)
##initialize system


#initialize the constants
print('Initializing constants to 1')
const = np.ones(channels, dtype=complex)
load_constants(roach, const, cal0_info)
load_constants(roach, const, cal1_info)

print('Starting measurement !')

psg_source.set_power_dbm(lo_pow)
turn_on_sequence(rigol,rs_supply, psg_source, sleep_time=3)
time.sleep(2)
turn_on_LO_noise(rs_supply, sleep_time=3)
time.sleep(5)


#calibrated
rigol.turn_output_off(1)
if(rigol.get_status(1)):
    raise Exception('Channel 1 doesnt turn off!')
if(rf_off!=0):
    rigol.turn_output_off(2)
    if(rigol.get_status(2)):
        raise Exception('Channel 2 doesnt turn off!')

print('Computing constants')
ab_ratios,ab,aa,bb = compute_calibration(roach, pow0_info, pow1_info, cross_info)

rigol.turn_output_on(2)
if(not rigol.get_status(2)):
    raise Exception('Channel 2 doesnt turn on!')


load_constants(roach, np.ones(channels, dtype=complex), cal1_info)
load_constants(roach, ab_ratios, cal0_info)
print('RF cal')
time.sleep(1)
rf_cal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach, -ab_ratios, cal0_info)
print('LO cal')
time.sleep(1)
lo_cal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach,np.ones(channels, dtype=complex), cal0_info)
print('RF ideal')
time.sleep(1)
rf_ideal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach,-np.ones(channels, dtype=complex), cal0_info)
print('LO ideal')
time.sleep(1)
lo_ideal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])

#nolo
turn_off_LO_noise(rs_supply, sleep_time=2)
time.sleep(1)

load_constants(roach, np.ones(channels, dtype=complex), cal1_info)
load_constants(roach, ab_ratios, cal0_info)
print('nolo RF cal')
time.sleep(1)
nolo_rf_cal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach, -ab_ratios, cal0_info)
print('nolo LO cal')
time.sleep(1)
nolo_lo_cal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach,np.ones(channels, dtype=complex), cal0_info)
print('nolo RF ideal')
time.sleep(1)
nolo_rf_ideal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


load_constants(roach,-np.ones(channels, dtype=complex), cal0_info)
print('nolo LO ideal')
time.sleep(1)
nolo_lo_ideal = calan.read_interleave_data(roach, synth_info['brams'],
        synth_info['addrwidth'], synth_info['bitwidth'], synth_info['dtype'])


##analog 
turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=2)

os.system('play -nq -t alsa synth 1 sine 440')
print("Connect the 0 deg combiner")
raw_input("Press enter when you are ready")

turn_on_sequence(rigol, rs_supply, psg_source, sleep_time=2)
time.sleep(1)
turn_on_LO_noise(rs_supply, sleep_time=2)
time.sleep(1)
print('RF analog')
rf_ana = calan.read_interleave_data(roach, pow0_info['brams'], 
        pow0_info['addrwidth'],pow0_info['bitwidth'], pow0_info['dtype'])

turn_off_LO_noise(rs_supply, sleep_time=2)
time.sleep(1)
print('nolo RF analog')
nolo_rf_ana = calan.read_interleave_data(roach, pow0_info['brams'], 
        pow0_info['addrwidth'],pow0_info['bitwidth'], pow0_info['dtype'])


turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=2)

os.system('play -nq -t alsa synth 1 sine 440')
print("Connect the 180 deg combiner")
raw_input("Press enter when you are ready")

turn_on_sequence(rigol, rs_supply, psg_source, sleep_time=2)
time.sleep(1)
turn_on_LO_noise(rs_supply, sleep_time=2)
print('LO analog')
time.sleep(1)
lo_ana = calan.read_interleave_data(roach, pow0_info['brams'], 
        pow0_info['addrwidth'],pow0_info['bitwidth'], pow0_info['dtype'])

turn_off_LO_noise(rs_supply, sleep_time=2)
print('nolo LO analog')
time.sleep(1)
nolo_lo_ana = calan.read_interleave_data(roach, pow0_info['brams'], 
        pow0_info['addrwidth'],pow0_info['bitwidth'], pow0_info['dtype'])


turn_off_sequence(rigol, rs_supply, psg_source, sleep_time=2)





f = h5py.File(save_path+'/'+name+'.hdf5', 'w') 
dset0= f.create_dataset('rf_cal', data=rf_cal)
dset1= f.create_dataset('lo_cal', data=lo_cal)
dset2= f.create_dataset('nolo_rf_cal', data=nolo_rf_cal)
dset3= f.create_dataset('nolo_lo_cal', data=nolo_lo_cal)

dset4= f.create_dataset('rf_ideal', data=rf_ideal)
dset5= f.create_dataset('lo_ideal', data=lo_ideal)
dset6= f.create_dataset('nolo_rf_ideal', data=nolo_rf_ideal)
dset7= f.create_dataset('nolo_lo_ideal', data=nolo_lo_ideal)

dset8= f.create_dataset('rf_ana', data=rf_ana)
dset9= f.create_dataset('lo_ana', data=lo_ana)
dsetA= f.create_dataset('nolo_rf_ana', data=nolo_rf_ana)
dsetB= f.create_dataset('nolo_lo_ana', data=nolo_lo_ana)

dsetC= f.create_dataset('aa', data=aa)
dsetD= f.create_dataset('bb', data=bb)
dsetE= f.create_dataset('ab', data=ab, dtype=complex)
dsetF= f.create_dataset('ab_ratios', data=ab_ratios, dtype=complex)


f.close()


fig = plt.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

ax1.plot(freq, 10*np.log10(rf_cal), label='rf')
ax1.plot(freq, 10*np.log10(lo_cal), label='lo')
ax1.plot(freq, 10*np.log10(nolo_rf_cal), label='nolo rf')
ax1.grid()
ax1.set_ylim(35,80)
ax1.set_title('Cal')
ax1.set_ylabel('db')
ax1.set_xlabel('MHz')

ax2.plot(freq, 10*np.log10(rf_ideal), label='rf')
ax2.plot(freq, 10*np.log10(lo_ideal), label='lo')
ax2.plot(freq, 10*np.log10(nolo_rf_ideal), label='nolo rf')
ax2.grid()
ax2.set_ylim(35,80)
ax2.set_title('Ideal')
ax1.set_xlabel('MHz')

ax3.plot(freq, 10*np.log10(rf_ana), label='rf')
ax3.plot(freq, 10*np.log10(lo_ana), label='lo')
ax3.plot(freq, 10*np.log10(nolo_rf_ana), label='nolo rf')
ax3.grid()
ax3.set_ylim(35,80)
ax3.set_title('Analog')
ax3.legend()
ax1.set_xlabel('MHz')

plt.tight_layout()
plt.savefig(img_path+'/'+name+'.png')
#plt.close()

fig2 = plt.figure()

lnr_cal = pseudo_lnr(rf_cal, lo_cal, nolo_rf_cal)
lnr_ideal = pseudo_lnr(rf_ideal, lo_ideal, nolo_rf_ideal)
lnr_ana = pseudo_lnr(rf_ana, lo_ana, nolo_rf_ana)

plt.plot(freq, 10*np.log10(lnr_cal), label='cal')
plt.plot(freq, 10*np.log10(lnr_ideal), label='ideal')
plt.plot(freq, 10*np.log10(lnr_ana), label='analog')
plt.ylabel('lnr dB')
plt.xlabel('MHz')
plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig(img_path+'/lnr_'+name+'.png')

plt.show()

rs_supply.instr.close()
rigol.instr.close()
psg_source.instr.close()
