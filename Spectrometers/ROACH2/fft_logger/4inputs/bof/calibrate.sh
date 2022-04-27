#!/bin/bash
source configuration.sh

calibrate_adc5g.py \
    -i $(echo $ROACH_IP)\
    -gf 10\
    -gp -8\
    --zdok0snaps adcsnap0 adcsnap1\
    --zdok1snaps adcsnap2 adcsnap3\
    -dm -bw 1200 -psn -psp
    #-dm -do -di -bw 600 -psn -psp
