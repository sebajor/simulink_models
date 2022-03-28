import corr, time
import calandigital as calan

###
### Hyperparamters
###
roach_ip = '192.168.0.40'
boffile = 'packet_test.bof.gz'

source = ([192,168,2,3], 1234)  #source ip, source port
dest = ([192,168,2,10], 1234)   #dest ip, source port
tx_core = 'ten_Gbe_v2'

tge_pkt = 1024
read_sleep = 100            #sleep between packets

write_burst = 511           #the pkt generator will write write_burst+1 data points 
                            #per burst + one header
write_sleep = 512*512#2048*512

fpga_clk = 150.*10**6

###
###
###
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1) 
time.sleep(1)

dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
port = source[1]
mac_base = (2<<40)+(2<<32)

#configure the 10Gbe module
roach.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)

roach.write_int('ip', dest_ip)
roach.write_int('port', port)

#configure the packetizer
roach.write_int('pkt_len', tge_pkt)
roach.write_int('read_sleep', read_sleep)

#configure the sample generator 
roach.write_int('write_burst', write_burst)
roach.write_int('write_sleep', write_sleep)

#start test
roach.write_int('rst',0)
roach.write_int('en_write', 1)

