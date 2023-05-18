#!/bin/bash
plot_spectra.py \
    --ip 192.168.1.20\
    --fpg rfsoc_complex_correlator.fpg \
    -bn adc0_0 adc0_1 adc0_2 adc0_3 adc0_4 adc0_5 adc0_6 adc0_7 \
        adc1_0 adc1_1 adc1_2 adc1_3 adc1_4 adc1_5 adc1_6 adc1_7 \
        adc2_0 adc2_1 adc2_2 adc2_3 adc2_4 adc2_5 adc2_6 adc2_7 \
        adc3_0 adc3_1 adc3_2 adc3_3 adc3_4 adc3_5 adc3_6 adc3_7 \
    --nspecs 4\
    --addrwidth 8\
    --datawidth 64\
    -bw 1966.08\
    --nbits 14\
    --countreg cnt_rst\
    --accreg acc_len\
    --acclen 1024\
    -u \
    -c 

