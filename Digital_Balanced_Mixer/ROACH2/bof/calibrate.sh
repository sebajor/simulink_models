#!/bin/bash

calibrate_adc5g.py \
    -i 192.168.1.12\
    --genname TCPIP::192.168.1.39::INSTR \
    --genfreq 10\
    --genpow -3\
    --zdok0snaps adcsnap0\
    --zdok1snaps adcsnap1\
    -dm -do -di -bw 1080 -psn -psp
    #-dm -do -di -bw 600 -psn -psp
