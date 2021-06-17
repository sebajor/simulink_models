import corr, time

def init_gps(fpga):
    """ initialize gps
    """
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
