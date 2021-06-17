import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal


def frb_freq_curve(DM, f1, f2, n_samp=8192):
    """
     inputs:
        DM in pc*cm**3
        f1, f2 in mhz
     outputs:
        f in MHz
        t in seconds 
    """
    ##wrong!!! the t must be linear!
    ti = 4.149*10**3*DM*f1**(-2)
    tf = 4.149*10**3*DM*f2**(-2)
    t = np.linspace(ti,tf,n_samp)
    f = np.sqrt(4.149*10**3*DM/t)
    #t = 4.149*10**3*DM*f**(-2)
    return [t-t[0],f]


def frb_width_curve(
