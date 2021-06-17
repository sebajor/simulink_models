import numpy as np
import time
import calandigital as calan


def uesprit_v1(fpga):
    fpga.write_int('doa_en',3)
    time.sleep(0.1)
    fpga.write_int('doa_en',1)
    r11_brams = ['r11_0','r11_1', 'r11_2', 'r11_3']
    r22_brams = ['r22_0','r22_1', 'r22_2', 'r22_3']
    r12_brams = ['r12_0','r12_1', 'r12_2', 'r12_3']
    r11 = calan.read_interleave_data(fpga, r11_brams, 9, 32, dtype='>u4')
    r22 = calan.read_interleave_data(fpga, r22_brams, 9, 32, dtype='>u4')
    r12 = calan.read_interleave_data(fpga, r12_brams, 9, 32, dtype='>i4')
    r11 = np.mean(r11)
    r22 = np.mean(r22)
    r12 = np.mean(r12)
    r21 = r12
    lamb1 = (r11+r22+np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    lamb2 = (r11+r22-np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    #estas debiesen ser las fases
    mu1 = 2*np.arctan((r11-lamb1)/r12)
    mu2 = 2*np.arctan((r11-lamb2)/r12)

    return [mu1, mu2, lamb1, lamb2]


def uesprit_v2(fpga):
    fpga.write_int('doa_en',3)
    time.sleep(0.1)
    fpga.write_int('doa_en',1)
    r11acc_bram = 'r11_acc'
    r22acc_bram = 'r22_acc'
    r12acc_bram = 'r12_acc'
    r11 = calan.read_data(fpga, r11acc_bram, awidth=10, dwidth=32, dtype='>u4')
    r22 = calan.read_data(fpga, r22acc_bram, awidth=10, dwidth=32, dtype='>u4')
    r12 = calan.read_data(fpga, r12acc_bram, awidth=10, dwidth=32, dtype='>i4')
    r21 = r12
    lamb1 = (r11+r22+np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    lamb2 = (r11+r22-np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    #estas debiesen ser las fases
    mu1 = 2*np.arctan((r11-lamb1)/r12)
    mu2 = 2*np.arctan((r11-lamb2)/r12)
    mu1 = np.median(mu1)
    mu2 = np.median(mu2)
    return [mu1,mu2, np.median(lamb1), np.median(lamb2)]



