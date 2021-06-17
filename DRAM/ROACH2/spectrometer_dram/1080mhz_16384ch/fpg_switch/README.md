This model you could set the packet lenght. Like we bought a TL-SG105E
switch it only has 1Mb of buffer memory it drops the messages even when 
we optimize the transfer.

The model in the previous folder has a fix value in the parameter 
ring_buffer/gbe_pkt_size of 7918, here we have control over that parameter.
Everything else is the same.


To use the switch you have to manually set the ip address in the roach
for that use an usb cable and write:
    ifconfig eth0 10.0.0.5 netmask 255.255.255.0 up

