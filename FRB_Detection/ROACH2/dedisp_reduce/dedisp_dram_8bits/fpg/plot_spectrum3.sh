#!/bin/bash
plot_spectra.py \
    --ip        192.168.1.14 \
    `#--bof       frbd_64ch_600mhz.bof.gz` \
    --upload      \
    --bramnames small_spec2 \
    --nspecs    1 \
    --addrwidth 6 \
    --datawidth 32 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((2**1))
