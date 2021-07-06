#!/bin/bash
plot_spectra.py \
    --ip        192.168.0.40\
    `#--bof       rfidet_div.bof.gz `\
    --upload     \
    --bramnames dout0_0 dout0_1 dout0_2 dout0_3 \ 
                dout1_0 dout1_1 dout1_2 dout1_3 \ 
    --nspecs    2 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((2**8))
