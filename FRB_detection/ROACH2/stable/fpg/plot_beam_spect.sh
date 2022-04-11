#!/bin/bash
source configuration.sh
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof     $(echo $BOF_FILE)` \
    --upload      \
    --bramnames beam0 beam1 beam2 beam3 \
    --nspecs    1 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((128))
