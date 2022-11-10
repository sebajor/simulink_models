##Preliminar model:

- [x] 4 spectrometers with 2048 channels.
- [x] 2 inputs ffts were complex added (beamform).
- [x] Beamformed channel spectrum reduction (2048->64) 
- [x] 10Gbe log of the beamformed spectra with parametrizable accumulation.
- [x] Nmea GPS timestamp.
- [x] 3 inputs are bit reduced to 4 bits per sample and save in a DRAM ring buffer.
- [x] Dump the ring buffer data using a 1000mbps ethernet. (To do, allow package drop)
- [x] 10 Dedispersors  (Currently 11)
- [x] moving average and moving variance of the dedispersor output to detect event.
- [x] FFT channel Flaging.
- [x] RFI ranking. (Currently calculate the coherency of the rfi input and the beamformed). 
- [ ] Direction of arrival. (seems to be much harder...)
- [ ] GPS Timestamp
