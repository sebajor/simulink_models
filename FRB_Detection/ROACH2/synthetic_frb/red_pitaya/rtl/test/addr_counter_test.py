from cocotb.triggers import ClockCycles
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
import cocotb


@cocotb.test()
async def addr_counter_test(dut, iters=1500):
    clk = Clock(dut.clk, 10, 'ns')
    cocotb.fork(clk.start())
    dut.en <=0;
    dut.decimate <= 4;
    await ClockCycles(dut.clk, 3)
    #start counting
    dut.en <= 1;
    await ClockCycles(dut.clk, iters)
    dut.en <=0;
    await ClockCycles(dut.clk, 1)
    dut.en <= 1
    await ClockCycles(dut.clk, iters)
