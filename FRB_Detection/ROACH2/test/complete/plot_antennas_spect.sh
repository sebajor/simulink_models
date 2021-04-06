#!/bin/bash
source configuration.sh
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof       $(echo $BOF_FILE)` \
    --upload     \
    --bramnames spec1_0 spec1_1 spec1_2 spec1_3 \
                spec2_0 spec2_1 spec2_2 spec2_3 \
                spec1_4 spec1_5 spec1_6 spec1_7 \
                spec2_4 spec2_5 spec2_6 spec2_7 \
    --nspecs    4 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((128))
