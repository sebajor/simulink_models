#!/bin/bash

calibrate_adc5g.py \
    -i 192.168.1.18\
    -gf 10\
    -gp -8\
    --zdok0snaps adcsnap0\
    --zdok1snaps adcsnap1\
    -dm -do -di -bw 1080 -psn -psp
    #-dm -do -di -bw 600 -psn -psp
