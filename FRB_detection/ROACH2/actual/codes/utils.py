import calandigital as calan
import numpy as np
import os



def relative_phase(data0, data1, freq, fs=1200, dft_len=2048):
    """
    Get the relative phase between two snapshots using a dft 
    """
    k = round(freq/fs*dft_len%dft_len)
    twidd_factor = np.exp(-1j*2*np.pi*np.arange(dft_len)*k/dft_len)
    dft0 = np.mean(data0*twidd_factor)
    dft1 = np.mean(data1*twidd_factor)
    correlation = dft0*np.conj(dft1)
    phase = np.angle(correlation)
    return phase



def get_antenas(roach, dwidth=32, dtype='>I'):
    """
    Obtain the antennas spectrums
    """
    brams = ['antenna_0','antenna_1', 'antenna_2', 'antenna_3']
    antenas = np.zeros([4, 2048])
    for i in range(len(brams)):
        antenas[i,:] =  calan.read_data(roach, brams[i], awidth=11,dwidth=dwidth,dtype=dtype)
    return antenas

def get_beam(roach, dwidth=32, dtype='>I'):
    """
    Obtain synthesized beam spectrum
    """
    beam = calan.read_data(roach, 'beam', awidth=11, dwidth=dwidth, dtype=dtype)
    return beam



def get_dedispersed_power(roach, index):
    """get dedispersed power 
    """
    data = calan.read_data(roach, 'dedisp'+str(index), awidth=10, dwidth=32, dtype='>I')
    return data


def get_dedispersed_mov_avg(roach, index):
    """Get the moving average over the dedispersed power
    """
    data = calan.read_data(roach, 'avg'+str(index), awidth=10, dwidth=32, dtype='>I')
    return data

def disp_time(dm, flow, fhigh):
    """
    Compute dispersed FRB duration.
    :param dm: Dispersion measure in [pc*cm^-3]
    :param flow: Lower frequency of FRB in [MHz]
    :param fhigh: Higher frequency of FRB in [MHz]
    """
    # DM formula (1e-3 to change from ms to s)
    k = 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]
    td = k*dm*(flow**-2 - fhigh**-2)*1e-3
    return td


def compute_accs(fcenter, bw, nchnls, DMs):
    k= 4.16e6 # formula constant [MHz^2*pc^-1*cm^3*ms]

    flow    = fcenter - bw/2 # MHz
    fhigh   = fcenter + bw/2 # MHz
    iffreqs = np.linspace(0, bw, nchnls/32, endpoint=False)
    rffreqs = iffreqs + flow
    Ts      = 1/(2*bw) # us
    tspec   = Ts*nchnls # us

    binsize = iffreqs[1]
    fbin_low = rffreqs[-2]+binsize/2
    fbin_high = rffreqs[-1]+binsize/2
    accs = []
    for dm in DMs:
        disptime = disp_time(dm, fbin_low, fbin_high)
        acc = 1.*disptime*1e6/tspec
        accs.append(int(round(acc)))
    print('Computed accumulations: '+ str(accs))
    return accs


#class to read the 10gbe data

class read_10gbe_data():
    """Class to read the data comming from the 10Gbe
    """
    def __init__(self, filename):
        """ Filename: name of the file to read from
        """
        self.f = open(filename, 'rb')
        ind = self.find_first_header()
        self.f.seek(ind*4)
        size = os.path.getsize(filename)
        self.n_spect = (size-ind*4)//(2052*4)


    def find_first_header(self):
        """ Find the first header in the file bacause after the header is the first
        FFT channel.
        """
        data = np.frombuffer(self.f.read(2052*4), '>I')
        ind = np.where(data==0xaabbccdd)[0][0]
        return ind

    def get_spectra(self, number):
        """
        number  :   requested number of spectrums
        You have to be aware that you have enough data to read in the n_spect
        """
        spect = np.frombuffer(self.f.read(2052*4*number), '>I')
        spect = spect.reshape([-1, 2052])
        self.n_spect -= number
        return spect[:,4:]

    def get_complete(self):
        """
        read the complete data, be carefull on the sizes of your file
        """
        data = self.get_spectra(self.n_spect)
        return data

    def close_file(self):
        self.f.close()


##some bitwise operations

def set_bit(data, bit_ind):
    """
    set the bit_ind but dont touch the others
    """
    data |= (1<<bit_ind)
    return data

def clear_bit(data, bit_ind):
    """
    clear the bit_ind but dont touch the others
    """
    data &= ~(1<<bit_ind)
    return data

def flip_bit(data, bit_ind):
    """
    change the bit_ind status
    """
    data ^= (1<<bit_ind)
    return data

def get_bit(data, bit_ind):
    bit = data & (1<<bit_ind)
    return bit


def write_bitfield(prev_state, word, bitfield):
    """ prev_state  :   the word previous word, over you are going to write
        word        :   the word you want to write into the bitfield
        bitfield    :   start and end of the bitfield
    """
    if((word<<bitfield[0])> 2**bitfield[1]):
        raise Exception('The word is grater than the bitfield')
    mask = (2**(bitfield[1]-bitfield[0])-1)<<bitfield[0]
    clean_state = prev_state & ~(mask)  ##check
    new_state = clean_state | (word<<bitfield[0])
    return new_state


###debug functions
def get_resample_beam(roach, dwidth=32, dtype='>I'):
    data = calan.read_data(roach, 'debug_acc', awidth=6,dwidth=dwidth, dtype=dtype)
    return data

def get_acc_resample_beam(roach, dwidth=32, dtype='>I'):
    data = calan.read_data(roach, 'debug_acc', awidth=6,dwidth=dwidth, dtype=dtype)
    return data

def get_rfi_signals(roach):
    corr_spect = calan.read_data(roach, 'rfi_corr', 11, 16, '>h')
    pow_spect = calan.read_data(roach, 'rfi_pow', 11, 16, '>h')
    #fix an indexing problem
    corr_spect = (corr_spect.reshape([-1,4])[:,::-1]).flatten()
    pow_spect = (pow_spect.reshape([-1,4])[:,::-1]).flatten()
    return [corr_spect, pow_spect]

def get_rfi_score(roach):
    bram_name = 'rfi_flag'
    score = calan.read_data(roach, bram_name, 9, 64, '>h')
    score = (score.reshape([-1,4])[:,::-1]).flatten()
    score /= 2.**13
    return score

 
