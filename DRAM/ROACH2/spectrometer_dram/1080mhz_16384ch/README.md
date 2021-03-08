Spectrometer followed by a dram ring buffer and output the data through
the fpga ethernet.

The FFT has 16384 channels and the writing/reading control signals
are contained in the "control1" register and the ring_configuration register
which is internally handled by the python class "dram_class".

To take a look at the spectrometer and the snapshot you could issue the scripts
./plot_snaplshot and ./plot_spectrum.sh

(Use them with care, depending on the configuration on those files could modify 
the accumulation lenght or rst the system) 


##############################################################################
Ethernet interface

The ethernet interface uses a gmii if the communication is uninterrupted the
computer buffers quickly start to drop packages, to avoid that we sent an 
8192*n_pkt bits where n_pkt is a dram_class parameter, the dram_class sends a 
trigger to the fpga to send a package, and only allows send a new one when 
the pc finishes receiving the previous one (I think this could hang the program)

The default configuration of the computers has a shallow rx fifos, so to increase
the data rate is good to issue the following commands:

sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400
sudo sysctl -w net.core.optmem_max=26214400
sudo sysctl -w net.core.optmem_max=26214400
sudo sysctl -w net.core.netdev_max_backlog=300000


Payload structure:
The accumulated output is 64 bits and we have 8 parallel channels, that give 
us 512 bits each cycle and the dram accepts 288 bits and you need to present 
them at least 2 cycles, so we divided the 512 in two 256 parts and add a 32 
bit counter to check that everything works (and because its a headache
found a factors between 288 and 512, (512*9=288*16?, puaj)).

So for example when receiving the data from the fpga the first values should be

0:32        chan0[0]
32:64       chan0[1]
64:96       chan1[0]
96:128      chan1[1]
128:160     chan2[0]
160:192     chan2[1]
192:224     chan3[0]
224:256     chan3[1]
256:288     count0
288:320     chan4[0]
320:352     chan4[1]
352:384     chan5[0]
384:416     chan5[1]
416:448     chan6[0]
448:480     chan6[1]
480:512     chan7[0]
512:544     chan7[1]
544:576     count1


Where the channels are divided in 32 bits words so we have a low and high word.

The read_data.py shows how to read and plot an spectrogram from the data acquired.
(If you try to plot everything your pc will hang)

##############################################################################
Check list:
-Modify the roach ip address in the init.py file and in the configuration.sh

-Increase the fifo lenght using the commmands in the eth part.

-You have to force the interface to have the same ip address that you give 
at the dram_class python script.

In ubuntu go to Settings-Network-Wired --> IPV4 mark Manual instead of
DHCP and put( this are the default values): 
addr: 10.0.0.29     netmask:255.255.255.255     Gateway:10.0.0.1

Make sure thats correct issuing the command "ip a" (with the roach turn on) and
you should see something like:

2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 82:a8:4c:65:7f:93 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.29/32 brd 10.0.0.29 scope global noprefixroute enp2s0
       valid_lft forever preferred_lft forever
    inet6 fe80::cdc:dd8e:7d1b:49ae/64 scope link
       valid_lft forever preferred_lft forever


