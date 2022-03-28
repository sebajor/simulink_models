Model to test the 10GBe connection between ROACH and a computer.

The model generate a burst with a parametrizable length and then sleep for
a parametrizable cycles.
The burst consist in one header 0xaabbccdd, 0xaabbccdd, 0xaabbccdd, 0xaabbccdd
and the payload consist in a counter that goes from (0, lenght-1).

You could check for different data rates, lenghts and see when the system start to loss
packets.

The packetizer is just a FIFO and a fsm in charge to read the the subwords 
to write them into the TenGBe module. So you should check also that the data rate
dont fill the FIFO.

The HDL and the simulation files could be found [here](https://github.com/sebajor/verilog_codes)
