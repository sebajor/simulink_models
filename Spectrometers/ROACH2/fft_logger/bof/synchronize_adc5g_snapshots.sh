#!/bin/bash
synchronize_adc5g_snapshots.py\
    --ip 192.168.1.18\
    --genpow -3\
    --genfreq 10\
    -bw 1080\
    --addrwidth 10\
    --datawidth 8
    #--delayregs ['adc0_delay', 'adc1_delay']\
    #--snapregs ['adcsnap0','adcsnap1']\
    #--snaptrig snap_trig
