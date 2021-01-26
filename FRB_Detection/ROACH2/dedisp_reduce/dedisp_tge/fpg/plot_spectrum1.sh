#!/bin/bash
source configuration.sh
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof       $(echo $BOF_FILE)` \
    --upload     \
    --bramnames spec1_0 spec1_1 spec1_2 spec1_3 \
                spec2_0 spec2_1 spec2_2 spec2_3 \
    --nspecs    2 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((3184))
