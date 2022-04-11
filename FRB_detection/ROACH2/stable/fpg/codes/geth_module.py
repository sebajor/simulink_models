import corr, time


def config_tge(fpga, source=([192,168,2,3], 1234), dest=([192,168,2,10], 1234),
                tx_core='ten_Gbe_v2',fpga_clk=150.*10**6, refresh=10**-3):
    """
    source  : ip, port
    dest    : ip, port
    tx_core : name of the 10gbe yellow block in the module
    fpga_clk: 
    refresh : its the rate at which a spectrum is sent
    """
    dest_ip = (dest[0][0]*(2**24)+dest[0][1]*(2**16)+dest[0][2]*(2**8)+dest[0][3])
    source_ip = (source[0][0]*(2**24)+source[0][1]*(2**16)+source[0][2]*(2**8)+source[0][3])
    port = source[1]
    mac_base = (2<<40)+(2<<32)
    nchnls  = 2048/4   ##number of channels/parallel streams
    acc = int(round(refresh/nchnls*fpga_clk))
    
    idle_cycle = 2**10# 2**15 #1024   ##check!
    pkt_size = 1024-3   ##recheck!
    
    fpga.write_int('ip_sel', 3)
    time.sleep(0.1)
    fpga.write_int('ip_addr', dest_ip)
    time.sleep(0.1)
    fpga.write_int('ip_sel',4)
    time.sleep(0.1)
    fpga.write_int('ip_addr', port)
    time.sleep(0.1)
    fpga.write_int('ip_sel',0)

    
    
    fpga.tap_start('tx_tap',tx_core,mac_base+source_ip,source_ip,port)
    fpga.write_int('cnt_rst',1)
    fpga.write_int('geth_pack_pkt_size', pkt_size) ##change the name of the ssubsys!!!!
    fpga.write_int('geth_pack_idle_cycle', idle_cycle)
    fpga.write_int('acc_len', acc)
    ##to start the transmition set cnt_rst to low!



    

