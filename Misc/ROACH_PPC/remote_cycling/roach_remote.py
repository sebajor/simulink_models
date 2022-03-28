import serial as serial
import ftdi
import defs_r2_ats as defs


global REV;
REV = 2

def ftdi_write(interface, data, retries = 3):
    retry = 0
    while retry < retries:
        res = ftdi.ftdi_write_data(interface, data, 1)
        if res == 1:
            retry = retries
        else:
            print c.WARNING + 'WARNING: FTDI write failed, retrying.' + c.ENDC
            retry += 1
            time.sleep(0.5)
    return res

def open_ftdi_d():
    ftdi_int_err = {-1:'unknown interface', -2:'usb device unavailable'}
    f = ftdi.ftdi_context()
    ftdi.ftdi_init(f)
    res = ftdi.ftdi_set_interface(f, ftdi.INTERFACE_D)
    if res <> 0:
        raise Exception('FTDI Interface ERROR: %s' %ftdi_int_err[res])
    res = ftdi.ftdi_usb_open(f, defs.R2_VID, defs.R2_PID)
    if res <> 0:
        raise Exception('FTDI Open ERROR: %s' %ftdi_open_err[res])
    return f

def power_force(ftdi_obj, state):
    # Rev1: force power on: PCTRL_EN (bit5), PCTRL_ONn (bit4)
    # Rev2: force power on: PCTRL_EN (bit5), PCTRL_ON (bit4) 
    rev1_on = '\x20'
    rev1_off = '\x30'
    rev2_on = '\x30'
    rev2_off = '\x20'
    if REV == 1 and state == 'on':
      byte = rev1_on
    elif REV == 1 and state == 'off':
      byte = rev1_off
    elif REV == 2 and state == 'on':
      byte = rev2_on
    else:
      byte = rev2_off
    return ftdi_write(ftdi_obj, byte)


def power_on():
    ftdi_obj = open_ftdi_d()
    power_force(ftdi_obj, 'on')

    
def power_off():
    ftdi_obj = open_ftdi_d()
    power_force(ftdi_obj, 'off')

ser_port = '/dev/ttyUSB2'
baud = 115200
state = ['off', 'on']





