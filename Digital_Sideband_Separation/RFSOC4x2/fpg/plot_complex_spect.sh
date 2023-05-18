#!/bin/bash
plot_spectra.py \
    --ip 192.168.1.20\
    -bn adc2_0 adc2_1 adc2_2 adc2_3 adc2_4 adc2_5 adc2_6 adc2_7 \
        adc3_0 adc3_1 adc3_2 adc3_3 adc3_4 adc3_5 adc3_6 adc3_7 \
        cal2_0 cal2_1 cal2_2 cal2_3 cal2_4 cal2_5 cal2_6 cal2_7 \
        cal3_0 cal3_1 cal3_2 cal3_3 cal3_4 cal3_5 cal3_6 cal3_7 \
    --nspecs 4\
    --addrwidth 8\
    --datawidth 64\
    -bw 1966.08\
    --nbits 14\
    --countreg cnt_rst\
    --accreg acc_len_cal\
    --acclen 1024\
    -c 
    #--fpg rfsoc_if_calibrator.fpg \
