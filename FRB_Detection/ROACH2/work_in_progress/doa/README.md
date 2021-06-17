#Roadmap:

##Submodules:
- [x] Incoherent Dedispersor (mapped to brams not srl16(shif registers)!, synth report max clock 333.5mhz).
- [ ] 10x Dedispersors at different DMs.(currently we have 4)
- [x] 4 adc running at 1200 MHz, looking at the 3rd Nyquist zone (1200-1800).
- [x] 4x2048 FFTs, complex add 3 of them to synthesize the beam.
- [x] Re-bin the beam spectrum to 64 channles (in order to save memory in the dedispersor).
- [ ] Logic to detect the increasing in the dedispersed power to trigger a possible detection ( could be moving average+moving variance).
- [ ] Reduce the 8 bits of the 3 ADC input antennas to save it in the DRAM (AGC).
- [x] Save 4 bit input in DRAM using a ring buffer like scheme. Stop it when a FRB is detected.
- [x] In order to dump the DRAM data quicker to a pc, send it using the 1Geth. (it takes aprox 3min).
- [x] Send the accumulate beam spectrum using the 10Gbe.
- [ ] GPS, DOA, RFI in the header of the 10GBe spectrum. (currently we have only timestamp) 
- [x] For both (1Gbe and 10GBe) we need a time multiplexor or Parallel input Serial output.
- [ ] RFI ranking.
- [ ] DOA of the source. Using Unitary Esprit.
- [ ] Triggering logic. Dedispersed Power above some threshold, not RFI and DOA!= Horizon.


##Tasks
- [x] Generate synthetic FRB.
- [x] Test using cables.
- [ ] Test using antennas.  
