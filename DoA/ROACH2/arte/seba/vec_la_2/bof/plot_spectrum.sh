#!/bin/bash
plot_spectra.py \
    --ip        192.168.0.40       \
    `--bof        vec_no_linalg.bof.gz`\
    --upload     \
    --bramnames dout_0a_0 dout_0a_1 dout_0a_2 dout_0a_3 \
                dout_0c_0 dout_0c_1 dout_0c_2 dout_0c_3 \
    --nspecs    2 \
    --addrwidth 9 \
    --datawidth 64 \
    --bandwidth 600 \
    --nbits     8 \
    --countreg  cnt_rst \
    --accreg    acc_len \
    --acclen    $((1024))
