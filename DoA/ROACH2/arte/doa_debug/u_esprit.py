import numpy as np
import calandigital as calan

def uesprit_v1(fpga):
    """Takes the correlation matrix and calculate the phase between
    signals using the typical uesprit algo
    """
    autocor_bram = [['x11_0', 'x11_1'], ['x22_0', 'x22_1']]
    crosscor_bram = ['x12_0', 'x12_1']
    r11_0, r11_1 = calan.read_deinterleave_data(fpga, bram=autocor_bram[0][0], dfactor=2,
            awidth=9, dwidth=64, dtype='>u4')
    r11_2, r11_3 = calan.read_deinterleave_data(fpga, autocor_bram[0][1], dfactor=2,
            awidth=9, dwidth=64, dtype='>u4')
    r11 = (np.vstack([r11_0, r11_1, r11_2, r11_3]).T).flatten()
    r22_0, r22_1 = calan.read_deinterleave_data(fpga, bram=autocor_bram[1][0], dfactor=2,
            awidth=9, dwidth=64, dtype='>u4')
    r22_2, r22_3 = calan.read_deinterleave_data(fpga, autocor_bram[1][1], dfactor=2,
            awidth=9, dwidth=64, dtype='>u4')
    r22 = (np.vstack([r22_0, r22_1, r22_2, r22_3]).T).flatten()

    r12_0, r12_1 = calan.read_deinterleave_data(fpga, bram=crosscor_bram[0], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    r12_2, r12_3 = calan.read_deinterleave_data(fpga, crosscor_bram[1], dfactor=2,
            awidth=9, dwidth=64, dtype='>i4')
    r12 = (np.vstack([r12_0, r12_1, r12_2, r12_3]).T).flatten()

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
    """ Takes the integrated values of the correlation matrix ie sum(channels)
    and calculate typical uesprit
    """
    r11 = calan.read_data(fpga, 'xr11_acc', awidth=8, dwidth=64, dtype='>u8')
    r12 = calan.read_data(fpga, 'xr12_acc', awidth=8, dwidth=64, dtype='>i8')
    r22 = calan.read_data(fpga, 'xr22_acc', awidth=8, dwidth=64, dtype='>u8')
    r21 = r12
    lamb1 = (r11+r22+np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    lamb2 = (r11+r22-np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    #estas debiesen ser las fases
    mu1 = 2*np.arctan((r11-lamb1)/r12)
    mu2 = 2*np.arctan((r11-lamb2)/r12)
    mu1 = np.median(mu1)
    mu2 = np.median(mu2)
    return [mu1,mu2, np.median(lamb1), np.median(lamb2)]


def uesprit_v3(fpga, freq,samples=1024, fs=600):
    """Takes the spectrum and calcuale uesprit usign just one channel 
    """
    dft_len = 2048*2
    k = int(round(1.*freq/fs*dft_len))
    print("channel number %i"%k)
    r11_chan = np.zeros([samples])
    r22_chan = np.zeros([samples])
    r12_chan = np.zeros([samples])
    for i in range(samples):
        autocor_bram = [['x11_0', 'x11_1'], ['x22_0', 'x22_1']]
        crosscor_bram = ['x12_0', 'x12_1']
        r11_0, r11_1 = calan.read_deinterleave_data(fpga, bram=autocor_bram[0][0], dfactor=2,
                awidth=9, dwidth=64, dtype='>u4')
        r11_2, r11_3 = calan.read_deinterleave_data(fpga, autocor_bram[0][1], dfactor=2,
                awidth=9, dwidth=64, dtype='>u4')
        r11 = (np.vstack([r11_0, r11_1, r11_2, r11_3]).T).flatten()
        r22_0, r22_1 = calan.read_deinterleave_data(fpga, bram=autocor_bram[1][0], dfactor=2,
                awidth=9, dwidth=64, dtype='>u4')
        r22_2, r22_3 = calan.read_deinterleave_data(fpga, autocor_bram[1][1], dfactor=2,
                awidth=9, dwidth=64, dtype='>u4')
        r22 = (np.vstack([r22_0, r22_1, r22_2, r22_3]).T).flatten()

        r12_0, r12_1 = calan.read_deinterleave_data(fpga, bram=crosscor_bram[0], dfactor=2,
                awidth=9, dwidth=64, dtype='>i4')
        r12_2, r12_3 = calan.read_deinterleave_data(fpga, crosscor_bram[1], dfactor=2,
                awidth=9, dwidth=64, dtype='>i4')
        r12 = (np.vstack([r12_0, r12_1, r12_2, r12_3]).T).flatten()
        r11_chan[i] = r11[k]
        r22_chan[i] = r22[k]
        r12_chan[i] = r12[k]
    r11 = np.mean(r11_chan)
    r12 = np.mean(r12_chan)
    r22 = np.mean(r22_chan)
    r21 = r12
    lamb1 = (r11+r22+np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    lamb2 = (r11+r22-np.sqrt((r11+r22)**2-4*(r11*r22-r12*r21)))/2
    #estas debiesen ser las fases
    mu1 = 2*np.arctan((r11-lamb1)/r12)
    mu2 = 2*np.arctan((r11-lamb2)/r12)
    return [mu1, mu2, lamb1, lamb2]
