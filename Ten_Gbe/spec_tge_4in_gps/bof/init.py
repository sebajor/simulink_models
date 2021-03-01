import numpy as np
import calandigital as calan
import time
from geth_module import config_tge


def init_gps(fpga):
    fpga.write_int('gps_ctrl',1)
    fpga.write_int('gps_ctrl',0)
    timedata = time.localtime()
    mmdd = ((timedata.tm_mon-1)*30+timedata.tm_mday)*60*60*24  ##current month and day in seconds
                                                        ##we take the month as 31 days..could be
                                                        ##fixed, but should be a bunch of if-else's
    fpga.write_int('gps_ddmmyy', mmdd)
    print("To continue the gps recv must have located some sources")
    conf = raw_input('its ready?(y/n)')
    if(conf=='y'):
        print('Programming ublox')
        fpga.write_int('gps_ctrl', 2)
        time.sleep(0.5)
        fpga.write_int('gps_ctrl',0b100)
        fpga.write_int('gps_ctrl',0)
        print('reading time from gps')
        current_time = gps_read(fpga)
        print(current_time)

    
def gps_read(fpga):
    toy = fpga.read_int('sec')
    days = int(toy/(24.*3600))
    hours =int((toy%(24.*3600))/3600)
    minutes = int((toy%(24.*3600)%3600)/60)
    secs = toy%(24.*3600)%3600%60
    out = str(days)+'day'+str(hours)+':'+str(minutes)+':'+str(secs)
    #print(out)
    return out
     


IP = '192.168.0.40'
boffile ='spec_tge_gps.bof.gz'

n_chann = 2**11/4   ##we have 4 parallel data streams
log_time = 10.*10**-3    ##log every 10ms
clk_freq = 150.*10**6
acc = int(round(log_time/n_chann*clk_freq))



fpga = calan.initialize_roach(boffile=boffile, ip=IP, upload=1)
time.sleep(1)

init_gps(fpga)
time.sleep(1)
config_tge(fpga)
fpga.write_int('cnt_rst',0)   #start transfer!



spec = calan.read_interleave_data(fpga, brams=['dout_0a_0', 'dout_0a_1',
                                  'dout_0a_2', 'dout_0a_3'], awidth=9, dwidth=64,
                                  dtype='>u8')


