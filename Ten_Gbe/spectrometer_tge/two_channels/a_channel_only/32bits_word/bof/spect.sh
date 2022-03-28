#!/bin/bash
plot_spectra.py \
    --ip        192.168.1.18\
    --bof        spectrometer_tge.bof.gz \
    --upload     \
    --bramnames dout_0a_0 dout_0a_1 dout_0a_2 dout_0a_3 \
    --nspecs    1 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((2048))
