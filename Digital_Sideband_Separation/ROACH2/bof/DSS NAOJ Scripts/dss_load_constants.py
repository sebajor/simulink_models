#!/usr/bin/python
import argparse, tarfile
import numpy as np
import calandigital as cd

# model parameters
nchannels      = 2048
consts_nbits   = 32
consts_binpt   = 27
# constants where USB is maximized (LSB is rejected)
bram_consts_usb_re = ['bram_mult0_0_bram_re', 'bram_mult0_1_bram_re',
                      'bram_mult0_2_bram_re', 'bram_mult0_3_bram_re',
                      'bram_mult0_4_bram_re', 'bram_mult0_5_bram_re',
                      'bram_mult0_6_bram_re', 'bram_mult0_7_bram_re']
bram_consts_usb_im = ['bram_mult0_0_bram_im', 'bram_mult0_1_bram_im',
                      'bram_mult0_2_bram_im', 'bram_mult0_3_bram_im',
                      'bram_mult0_4_bram_im', 'bram_mult0_5_bram_im',
                      'bram_mult0_6_bram_im', 'bram_mult0_7_bram_im']
# constants where LSB is maximized (USB is rejected)
bram_consts_lsb_re = ['bram_mult1_0_bram_re', 'bram_mult1_1_bram_re',
                      'bram_mult1_2_bram_re', 'bram_mult1_3_bram_re',
                      'bram_mult1_4_bram_re', 'bram_mult1_5_bram_re',
                      'bram_mult1_6_bram_re', 'bram_mult1_7_bram_re']
bram_consts_lsb_im = ['bram_mult1_0_bram_im', 'bram_mult1_1_bram_im',
                      'bram_mult1_2_bram_im', 'bram_mult1_3_bram_im',
                      'bram_mult1_4_bram_im', 'bram_mult1_5_bram_im',
                      'bram_mult1_6_bram_im', 'bram_mult1_7_bram_im']

if __name__ == '__main__':
    # if used as main script, read command line argmuments 
    # and starts roach communication
    parser = argparse.ArgumentParser(
        description="Load calibration constants from a compressed file or \
            command line input.")
    parser.add_argument("-i", "--ip", dest="ip", required=True,
        help="ROACH IP address.")
    parser.add_argument("-b", "--bof", dest="boffile",
        help="Boffile to load into the FPGA.")
    parser.add_argument("-u", "--upload", dest="upload", action="store_true",
        help="If used, upload .bof from PC memory (ROACH2 only).")
    parser.add_argument("-li", "--load_ideal", dest="load_ideal", action="store_true",
        help="If used, load ideal constant, else use calibration constants \
        from caldir.")
    parser.add_argument("-ic", "--ideal_const", dest="ideal_const", default="0+1j",
        help="Ideal constant to load value to load.")
    parser.add_argument("-cd", "--caldir", dest="caldir",
        help="Directory from where extract the calibration constants. \
        Assumes it is compressed in .tar.gz format.")
    args = parser.parse_args()

    roach = cd.initialize_roach(args.ip, boffile=args.boffile, upload=args.upload)
    bm_load_constants(roach, args.load_ideal, complex(args.ideal_const), args.caldir)

def dss_load_constants(roach, load_ideal, ideal_const=0+1j, caldir=""):
    """
    Load load digital sideband separation constants.
    :param roach: FpgaClient object to communicate with roach.
    :param load_ideal: if True, load ideal constant, else use calibration 
        constants from caldir.
    :param ideal_const: ideal constant value to load.
    :param caldir: .tar.gz directory with the calibration data.
    """
    if load_ideal:
        print("Using ideal constant " + str(ideal_const) + ".")
        consts_usb = ideal_const * np.ones(nchannels, dtype=np.complex64)
        consts_lsb = ideal_const * np.ones(nchannels, dtype=np.complex64)
    else: # use calibrated constants
        print("Using constants from calibration directory.")
        consts_lsb, consts_usb = compute_consts(caldir)

    print("Loading constants...")
    load_comp_constants(roach, consts_usb, bram_consts_usb_re, bram_consts_usb_im)
    load_comp_constants(roach, consts_lsb, bram_consts_lsb_re, bram_consts_lsb_im)
    print("done")

def compute_consts(caldir):
    """
    Compute constants using tone calibration info.
    :param caldir: calibration directory.
    :return: calibration constants.
    """
    caldata = get_caldata(caldir)
    
    # get arrays
    a2_toneusb = caldata['a2_toneusb']; a2_tonelsb = caldata['a2_tonelsb']
    b2_toneusb = caldata['b2_toneusb']; b2_tonelsb = caldata['b2_tonelsb']
    ab_toneusb = caldata['ab_toneusb']; ab_tonelsb = caldata['ab_tonelsb']

    # consts usb are computed with tone in lsb, because you want to cancel out lsb,
    # the same for consts lsb
    consts_usb =         -1 * ab_tonelsb  / b2_tonelsb #  ab*   / bb* = a/b
    consts_lsb = -1 * np.conj(ab_toneusb) / a2_toneusb # (ab*)* / aa* = a*b / aa* = b/a

    return consts_lsb, consts_usb

def get_caldata(datadir):
    """
    Extract calibration data from directory compressed as .tar.gz.
    """
    tar_file = tarfile.open(datadir)
    caldata = np.load(tar_file.extractfile('caldata.npz'))

    return caldata

def load_comp_constants(roach, consts, bram_re, bram_im):
    """
    Load complex constants into ROACH bram. Real and imaginary parts
    are loaded in separated bram blocks.
    :param roach: FpgaClient object to communicate with roach
    :param consts: complex constants array.
    :param bram_re: bram block name for real part.
    :param bram_im: bram block name for imaginary part.
    """
    # separate real and imaginary
    consts_re = np.real(consts)
    consts_im = np.imag(consts)

    # convert data into fixed point representation
    consts_re_fixed = cd.float2fixed(consts_re, consts_nbits, consts_binpt, warn=True)
    consts_im_fixed = cd.float2fixed(consts_im, consts_nbits, consts_binpt, warn=True)

    # load data
    cd.write_interleaved_data(roach, bram_re, consts_re_fixed)
    cd.write_interleaved_data(roach, bram_im, consts_im_fixed)
