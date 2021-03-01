#!/bin/bash
plot_spectra.py \
    --ip        192.168.1.14 \
    `#--bof       reduce_spect.fpg` \
    --upload     \
    --bramnames spec1_0 spec1_1 spec1_2 spec1_3 \
    --nspecs    1 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((2**3))
