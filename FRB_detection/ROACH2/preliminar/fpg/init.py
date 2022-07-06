import calandigital as calan
import numpy as np
import sys, time, corr
sys.path.append('codes')
import utils, control

###
### hyperparameters
###
roach_ip ='192.168.1.18'
boffile = 'arte_new2.fpg'

##harcoded parameters
fpga_clk = 150.*10**6
bw = 600.
flow = 1200.
nchannels = 2048.

##dedispersors
##(the dedispersor output and the treshold is a 20_10UFix)
DMs = [80,160,240,320,400,480]
thresh = [1,1,1,1, 1, 1]     ## for each DM the detection threshold is 
                                        ## mov avg+thresh
#10Gbe log
log_time = 10.**-2                       ##10Gbe frame rate

#rfi detection
rfi_acc_len = 256                       ##rfi subsystem accumulation
rfi_thresh = 0.8                        ##over rfi_thresh is considered as rfi event
rfi_hold = 0.5                          ##if an rfi event is detected we dont allow an FRB 
                                        ##detection for rfi_hold seconds
#ring buffer parameters
adc_gain = 1                            ##the ADC samples are reduced to 4 bits per sample, this parameter
                                        ##multiplies each ADC sample to modify its range
sock_addr = ('10.0.0.29',1234)          ##ip, port of the computers
                                        ##roach will transmit from  10.0.0.45, 1234
dram_frames = 2
#channels to flag
flags = np.arange(20).tolist()
flags = flags+[1024]

###
###
###


#roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)
roach = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(2)

roach_control = control.roach_control(roach)
roach_control.set_snap_trigger()

roach_control.flag_channels(flags)

###compute the necessary accumulations
dedisp_acc = utils.compute_accs(flow+bw/2, bw, nchannels, DMs)
dedisp_acc = np.array(dedisp_acc)//2

##dedispersor accumulation
for i in range(len(dedisp_acc)):
    roach_control.set_accumulation(dedisp_acc[i], thresh=thresh[i], num=1+i)


##rfi accumulation
roach_control.set_accumulation(rfi_acc_len, thresh=rfi_thresh, num=31)
roach_control.set_accumulation(rfi_hold, thresh=0, num=30)

#initialize subsystem
roach_control.initialize_10gbe(integ_time=log_time)
roach_control.enable_10gbe()

#initialize ring buffer subsystem
#roach_control.set_ring_buffer_gain(adc_gain)
#roach_control.initialize_dram(addr=sock_addr, n_pkt=dram_frames)
#roach_control.write_dram()


#enable rfi subsytem
#roach_control.enable_rfi_subsystem()

roach_control.reset_accumulators()
roach_control.enable_dedispersor_acc()



