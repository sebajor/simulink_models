All the fpg were compiled with a sampling frequency of 3932.16MHz, 
downconverted using a different NCO frequency and then decimated by two.

rfsoc_complex.fpg was compiled with -0.98304 GHz at the NCO. Like we are using decimation 2 
the spectrum goes from (0,1966.08)

rfsoc_complex_inverted.fpg was compiled with 0.98304 GHz at the NCO. Here like we are using
a positive frequency we end up with the negative portion of the spectrum and the spectrum 
from (1966.08,0).

rfsoc_complex_shifted.fpg was compiled with 0.78304 GHz at the NCO. Here we have the 
frequency from (-200, 1766.08). In this case the filter response is clear.
