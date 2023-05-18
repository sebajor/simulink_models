#!/bin/bash
python3 plot_correlation.py \
    --ip 192.168.1.20\
    --fpg rfsoc_if_calibrator.fpg \
    -bn corr01_0 corr01_1 corr01_2 corr01_3 corr01_4 corr01_5 corr01_6 corr01_7 \
    --nspecs 1\
    --addrwidth 8\
    --datawidth 64\
    -bw 1966.08\
    --nbits 14\
    --countreg cnt_rst\
    --accreg acc_len_cal\
    --acclen 1024\

