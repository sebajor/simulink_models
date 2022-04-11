import numpy as np
import corr, struct, time

IP ='192.168.0.40'
bof = 'basic_dram.fpg'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(0.5)
fpga.upload_program_bof(bof , 3000)
time.sleep(0.5)

fpga.write_int('addr',0)
fpga.write_int('en_read', 0)   #dont allow fpga reading
fpga.write_int('input0', 1234)
fpga.write_int('input1', 5678)

fpga.write_int('write',1); fpga.write_int('write',0)

fpga.write_int('ddr3_ctrl', 0)
dat = struct.unpack('>16I', fpga.read('ddr3_mem', 64))
print(dat)
#look that even if I wrote only addr 0 the data appears duplicated

##write the first word in page 2
fpga.write_int('addr', 0x04000000/256/2*8) 
#the word size is 256, and the data is duplicated, x8 to pass it to bits
fpga.write_int('input0', 1010)
fpga.write_int('input1', 2020)
fpga.write_int('write',1); fpga.write_int('write',0)

fpga.write_int('ddr3_ctrl',1)
dat = struct.unpack('>16I', fpga.read('ddr3_mem', 64))
print(dat)







