import calandigital as calan
import numpy as np
import h5py, time, os, sys
import argparse


parser = argparse.ArgumentParser(
    description="intialize roach")

parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-f" "--filename", dest="filename", default='data.hdf5',
        help="Output file location")
parser.add_argument("-n", "-number", dest="n", default=1,
        help="number of frames to save")


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


def main():
    args = parser.parse_args()
    roach = calan.initialize_roach(args.ip)
    time.sleep(1)
    adc0_data = np.zeros([2**11, 32*int(args.n)], dtype=complex)
    adc1_data = np.zeros([2**11, 32*int(args.n)], dtype=complex)
    adc0_bram = ['dout0_0', 'dout0_1', 'dout0_2', 'dout0_3',
                 'dout0_4', 'dout0_5', 'dout0_6', 'dout0_7']
    adc1_bram = ['dout1_0', 'dout1_1', 'dout1_2', 'dout1_3',
                 'dout1_4', 'dout1_5', 'dout1_6', 'dout1_7']
    for i in range(int(args.n)):
        print('iter %i' %i)
        roach.write_int('cnt_rst', 2)
        roach.write_int('cnt_rst', 0)
        time.sleep(0.5)
        re, im = read_brams(roach, adc0_bram,14,32,'>i')
        data0 = re+1j*im
        data0 = data0.reshape([-1,2048])
        re, im = read_brams(roach, adc1_bram,14,32,'>i')
        data1 = re+1j*im
        data1 = data1.reshape([-1,2048])
        adc0_data[:,32*i:32*(i+1)] = data0.T 
        adc1_data[:,32*i:32*(i+1)] = data1.T 
    f = h5py.File((args.filename), 'w')
    datset0 = f.create_dataset('adc0', dtype=complex, data=adc0_data)
    datset1 = f.create_dataset('adc1', dtype=complex, data=adc1_data)
    f.close() 

if __name__ == '__main__':
    main()
