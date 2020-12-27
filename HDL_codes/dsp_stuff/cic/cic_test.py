import cocotb, struct
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.binary import BinaryValue
import numpy as np
import struct

def int2bin(in_data, bin_point):
    """in_data must be a list with the values!
    This function returns the binary representation of the data 
    and concatenate it
    """
    dat = (in_data*2**bin_point).astype(int)
    bin_data = struct.pack('>'+str(len(in_data))+'h', *dat); 
    return bin_data

def bin2int(in_data, bin_point):
    ##dat = struct.unpack('>'+str(len(in_data)/4)+'i', in_data)
    ##int_data = dat/2.**bin_point
    """Esta parte no funciona!!
    parallel = 4; mask=0xFFFFFFFF
    out = np.zeros(parallel)
    for i in range(parallel):
        out[i] = ((in_data>>i)&mask)
    bin_data  = struct.pack('>4I', *(out.astype(int)))
    out = np.array(struct.unpack('>4i', bin_data))
    output = out/(2.**bin_point)
    return output
    """
    #ahora si funca chuchetumare!!!
    parallel=4;
    #out = np.zeros(parallel)
    #for i in range(parallel):
    #    out[i] = int(in_data[32*(i+1):32*i], 2)
    #output = out/2.**bin_point
    output = np.array(struct.unpack('>4i',in_data))/2**bin_point
    return output




@cocotb.test()
async def cic_test(dut):
    clock = Clock(dut.clk_in, 10, units='ns')
    cocotb.fork(clock.start())
    dut.rst <= 0;
    dut.din <= 0;
    await ClockCycles(dut.clk_in, 4)
    ## impulse response, must be finite
    dut.din <= 1;
    await ClockCycles(dut.clk_in, 1)
    dut.din <= 0;
    for i in range(2**7):
        await ClockCycles(dut.clk_in, 1)
    ##test 2 step response, must be decimation**stages = 8^3=512=0x200
    dut.din <= 1;
    await ClockCycles(dut.clk_in, 2**7)







