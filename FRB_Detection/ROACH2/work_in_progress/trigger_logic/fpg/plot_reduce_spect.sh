#!/bin/bash
source configuration.sh
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof     $(echo $BOF_FILE)` \
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
