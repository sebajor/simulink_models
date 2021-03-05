To use the DRAM in ROACH2 you must download the files from
https://drive.google.com/drive/folders/1HEWYgPYy3wasy5DEs6vIWRkCNkZZGLSI
and replace the content of mlib_devel. 

This dram block was shared by Mike Movius.

You also need to update the kernel of the ROACH2.. check calandigital page
(comming soon, in the meanwhile you could follow the instructions
https://docs.google.com/document/d/1tqw4C6uZ6EULl1OykTFL_vQTnK52UBr0aYqTg44E5wg
)

Dram block Info:
    -You need to use the .fpg file!!! the bof doesnt works :(
    
    -The din is 288 bits always.
    
    -It has 2**25 address available--> 2**25*288/8 = 1.125GB
    
    -To write: Keep address and data for 2 cycles and at the same
    time keep the RWn low and cmd_valid high.
    
    -To read: keep the addr for 2 cycles, put RWn high and toggle 
    the cmd_valid. After som unknown umber of cycles you start 
    to see the output data with the rd_valid signal high.
    The output data comes out with half of the frequency, ie if
    you ask for addresses 0-1 the response is going to take 4 cycles
    0-0-1-1
    
    -The change of Rwn is costly, is better to mantain the state of
    the dram and not allow the writing/read with the valid signal.
    
    -PPC interface: The powerpc only reads 256 of the 288 data bits
    so you lost 32 bits which gives you 1GB available. The 32 bits are
    distributed as 8 bits every 64 ie the 288 word is break it down in
    the following format: 64-8-64-8-64-8-64-8 where you could read
    the 64 bits witht the PPC (this is due the OPB bus works with 
    32 bit data). By the way, in order to not generate confussion
    in the FPGA you have access to the 288 bits.

    -PPC interface2: The read_dram of the corr package doesnt work.
    To read the data you have to use the register ddr3_mem which allows
    you to access to 0x04000000 bytes (or bits?) this is our "page_size"
    To control the page number you can use the ddr3_ctrl register.
    For example if we set the ddr3_ctrl=3 the data in mem correspond
    to [3*page_size, 4*page_size-1]. 

    -PPC interface3:The data in the PPC appears duplicated (maybe thats
    the reason why we only could access half of the memory)

    -PPC interface4: To use the PPC interface you dont have to be
    using the DRAM in the fpga, ie dont validate the command in the
    fpga.

    
    -The wr_be is a bit masking. To save the 288 bits just set it 
    to 2**36-1

    -The signals cmd_ack, rd_tag, phy_ready, cmd_tag are not really
    usefull.

    

Hardware Info:
    -Our ROACH has the RDimm M393B5773 o 2GB. It has 3 banks,
    10 columns, 15 rows in a single rank. The RDimm uses 9 bits
    per address. Check the ddr3_controller_v2_1_0.mpd to check the
    parameters of the DRAM and if they are consistent with your 
    DRAM module.
    
    -In the simulink block, the address gets mapped into col-row-bank
    with the columns the least significant bits (check ui_cmd.v file)
    The standard recomendation is not jumping between rows because you
    have to pay it with dead time (you can read in burst when addressing
    columns)

    -The usual to do is read/write burstly. Note also like the dqs
    are 72 pins we are always writing 4 DRAM addresses.

    
-------------------------------------------------------------------
Misc: 
    In some models we use the ctypes python library to speed up some 
    functions. Usually because we reduce the samples to a 4 bit representation
    which is not supported by the typical parser libraries. So we made
    a wrapper for that sort of function. 
    As example, to comile the c code "testlib.c" to be used by the python
    ctypes package you have to issue the command:

    gcc -shared -Wl,-soname,testlib -o testlib.so -fPIC testlib.c
   



