#!/bin/bash
source configuration.sh

python codes/plot_antennas.py \
    --ip    $(echo $ROACH_IP) 
    
