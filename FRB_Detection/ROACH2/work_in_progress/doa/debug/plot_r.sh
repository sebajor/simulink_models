#!/bin/bash
plot_spectra.py \
    --ip        192.168.0.40       \
    `--bof        vec_no_linalg.bof.gz`\
    --upload     \
    --bramnames r11_0 r11_1 r11_2 r11_3 \
                r22_0 r22_1 r22_2 r22_3 \  
    --nspecs    2 \
    --addrwidth 9 \
    --datawidth 16 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    doa_acc \
    --acclen    $((8))
