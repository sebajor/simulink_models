import ctypes, struct, os
import numpy as np
import h5py
import ipdb

def parse_dram_data(bin_file, out_file='dram_data.hdf5',cdll_loc='./parse_data.so'):
    """
    bin_file:   binary file with the DRAM data
    out_file:   output filename
    cdll_loc:   location of the parse_data.so 
    """
    lib = ctypes.CDLL(cdll_loc)
    lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
    lib.freeptr.argtype = ctypes.c_void_p
    lib.freeptr.restype = None 

    file_size = os.path.getsize(bin_file)   #in bytes
    chunk = 3*2**15

    fr = open(bin_file, 'rb')
    iters= file_size//chunk
    fw = h5py.File(out_file, 'w')
    adc0 = fw.create_dataset('adc0', (iters*chunk*2,), dtype='b', chunks=(4*chunk,))
    adc1 = fw.create_dataset('adc1', (iters*chunk*2,), dtype='b', chunks=(4*chunk,))
    adc2 = fw.create_dataset('adc2', (iters*chunk*2,), dtype='b', chunks=(4*chunk,))
    for i in range(iters):
        print(i)
        #ipdb.set_trace()
        raw_data = fr.read(chunk)
        dat = lib.parse_data(raw_data, len(raw_data))
        dat_char = np.frombuffer(dat[:chunk*2], dtype='b')
        lib.freeptr(dat)
        dat_char = dat_char.reshape([-1, 24])
        dat0 = (dat_char[:,:8])[:,::-1].flatten()
        dat1 = (dat_char[:,8:16])[:,::-1].flatten()
        dat2 = (dat_char[:,16:24])[:,::-1].flatten()
        adc0[i*chunk*2//3:(i+1)*chunk*2//3] = dat0
        adc1[i*chunk*2//3:(i+1)*chunk*2//3] = dat1
        adc2[i*chunk*2//3:(i+1)*chunk*2//3] = dat2
    fr.close()
    fw.close()
    


        




