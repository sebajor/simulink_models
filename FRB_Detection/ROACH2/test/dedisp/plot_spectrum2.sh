#!/bin/bash
plot_spectra.py \
    --ip        192.168.0.40 \
    `#--bof       reduce_spect.fpg` \
    --upload      \
    --bramnames test \
    --nspecs    1 \
    --addrwidth 6 \
    --datawidth 32 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((2**1))
