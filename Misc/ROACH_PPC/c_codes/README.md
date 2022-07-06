# PowerPC info

The microprocessor in the ROACH system is a POWERPC440 with BORPH as the OS.
The PowerPc and the FPGA talks using an on chip peripheral bus, where the PowerPC acts as a Master of the bus and has access to the registers and memories connected to the bus (the yellow blocks of the simulink diagrams). For the PowerPC point of view each memory and register of the FPGA has an address assigned and Linux map that into the file in /dev/mem and to write/read you have to use the mmap command.
If you are wondering where are the addresses of the memories/registers is in the core_info.m or in the XPS_ROACH*_base/core_info.tab

The OS that runs in the PowerPC is BORPH which is a minimal flavor of Linux. It comes with a telnet connection in the port 7147 where you could send katcp commands. The casper people use the katcp commands to write/read the registers and for that they made the corr and casperfpga python libraries to interface with the telnet connection.
Is important to note that even that the PPC440 is a 64 bit the OS is of 32bits.

# PowerPC cross compilation
Like the system is write-protected we cant easily install programs, so a backdoor is to compile executable scripts in C, C++.
To cross compile you would need the following compilers:
`powerpc-linux-gnu-gcc` 
`powerpc-linux-gnu-gfortran`
`powerpc-linux-gnu-g++`

The basic command to compile the C code input.c into the executable out is:
`powerpc-linux-gnu-gcc -static input.c -o out_file`

That should generate the file out_file. Now you should need pass the executable to the powerPC, this steps worked for me:
1. Log into the PowerPC using telnet `telnet <roach_ip>`
2. Inside the PowerPC moves into a writeable folder like /tmp
3. Run `nc -l <roach_ip> -p 1234 > out`
4. Open a second terminal and run `nc -w 5 <roach_ip> < 1234 out_file `

That sends the out_file to the PowerPC and it receive it and call it out. Also to run it you have to give it execution execution permissions `chmod +x out`



