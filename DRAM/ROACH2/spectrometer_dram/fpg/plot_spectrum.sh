#!/bin/bash
source configuration.sh
plot_spectra.py \
    --ip        $(echo $ROACH_IP) \
    `#--bof       $(echo $BOF_FILE)` \
    --upload     \
    --bramnames dout0_0 dout0_1 dout0_2 dout0_3 \
                dout0_4 dout0_5 dout0_6 dout0_7 \
    --nspecs    1 \
    --addrwidth 10 \
    --datawidth 64 \
    --bandwidth 1080 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((3184))
