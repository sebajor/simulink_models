#!/bin/bash
plot_spectra.py \
    --ip        192.168.1.12\
    --bramnames dout0_0 dout0_1 dout0_2 dout0_3 dout0_4 dout0_5 dout0_6 dout0_7 \
    --nspecs    1 \
    --addrwidth 8 \
    --datawidth 64 \
    --bandwidth 1080 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    cal_acc_len \
    --acclen    $((2**8))
