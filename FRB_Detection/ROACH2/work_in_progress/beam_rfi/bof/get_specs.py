import calandigital as calan
import numpy as np

def get_specs(fpga):
    spec1_0, spec1_1 = calan.read_deinterleave_data(fpga, 'spec1_0', 2, 9, 64, '>u4')
    spec1_2, spec1_3 = calan.read_deinterleave_data(fpga, 'spec1_1', 2, 9, 64, '>u4')
    spec1 = np.vstack([spec1_0,spec1_1,spec1_2,spec1_3]).reshape((-1,), order='F')

    spec2_0, spec2_1 = calan.read_deinterleave_data(fpga, 'spec2_0', 2, 9, 64, '>u4')
    spec2_2, spec2_3 = calan.read_deinterleave_data(fpga, 'spec2_1', 2, 9, 64, '>u4')
    spec2 = np.vstack([spec2_0,spec2_1,spec2_2,spec2_3]).reshape((-1,), order='F')

    spec3_0, spec3_1 = calan.read_deinterleave_data(fpga, 'spec3_0', 2, 9, 64, '>u4')
    spec3_2, spec3_3 = calan.read_deinterleave_data(fpga, 'spec3_1', 2, 9, 64, '>u4')
    spec3 = np.vstack([spec3_0,spec3_1,spec3_2,spec3_3]).reshape((-1,), order='F')

    spec4_0, spec4_1 = calan.read_deinterleave_data(fpga, 'spec4_0', 2, 9, 64, '>u4')
    spec4_2, spec4_3 = calan.read_deinterleave_data(fpga, 'spec4_1', 2, 9, 64, '>u4')
    spec4 = np.vstack([spec4_0,spec4_1,spec4_2,spec4_3]).reshape((-1,), order='F')
    return [spec1, spec2, spec3, spec4]
