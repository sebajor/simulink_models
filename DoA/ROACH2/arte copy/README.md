#ARTE Direction of arrival

The models of this folders are based in unitary Esprit algorithms but we use
a FFT to multiplex in frequency.

The pointwise_doa takes every channel of the FFT and calculate the direction of arrival in each one.
The band_doa adds adjacent channels to form bands and calculate the direction of arrival in the band.


To keep the system manageable is super important to keep the bitwidths in a reasonable size, for that we made a preliminar model to collect data and then simulate to obtain the good bitwidths.

The codes are taken from [here](https://github.com/sebajor/verilog_codes/). You could use the testbench to find the bitwidhts.


