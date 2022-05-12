#!/bin/bash
source configuration.sh

python2 plot_rfi_signals.py \
    --ip    $(echo $ROACH_IP) 
