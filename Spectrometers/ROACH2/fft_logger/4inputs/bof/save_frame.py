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

    adc0_data = np.zeros([2**11, 16*int(args.n)], dtype=complex)
    adc1_data = np.zeros([2**11, 16*int(args.n)], dtype=complex)
    adc2_data = np.zeros([2**11, 16*int(args.n)], dtype=complex)
    adc3_data = np.zeros([2**11, 16*int(args.n)], dtype=complex)
    adc_data = [adc0_data, adc1_data, adc2_data, adc3_data]

    adc_bram0 = ['dout_0a_0', 'dout_0a_1', 'dout_0a_2', 'dout_0a_3']
    adc_bram1 = ['dout_0c_0', 'dout_0c_1', 'dout_0c_2', 'dout_0c_3']
    adc_bram2 = ['dout_1a_0', 'dout_1a_1', 'dout_1a_2', 'dout_1a_3']
    adc_bram3 = ['dout_1c_0', 'dout_1c_1', 'dout_1c_2', 'dout_1c_3']
    bram_names = [adc_bram0, adc_bram1, adc_bram2, adc_bram3]

    for i in range(int(args.n)):
        print('iter %i' %i)
        roach.write_int('cnt_rst', 2)
        roach.write_int('cnt_rst', 0)
        time.sleep(0.5)
        for j in range(4):
            re, im = read_brams(roach, bram_names[j],14,16,'>h')
            data = re+1j*im
            data = data.reshape([-1,2048])
            adc_data[j][:,16*i:16*(i+1)] = data.T
    f = h5py.File((args.filename), 'w')
    datset0 = f.create_dataset('adc0', dtype=complex, data=adc_data[0])
    datset1 = f.create_dataset('adc1', dtype=complex, data=adc_data[1])
    datset2 = f.create_dataset('adc2', dtype=complex, data=adc_data[2])
    datset3 = f.create_dataset('adc3', dtype=complex, data=adc_data[3])
    f.close()

if __name__ == '__main__':
    main()
