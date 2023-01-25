#!/bin/bash

calibrate_adc5g.py \
    -i 192.168.1.12\
    -gf 10\
    -gp -8\
    --zdok0snap adcsnap0 adcsnap1 \
    --zdok1snap adcsnap2 adcsnap3 \
    --ns 128\
    -dm -bw 600 -psn -psp
    #-dm -do -di -bw 600 -psn -psp
