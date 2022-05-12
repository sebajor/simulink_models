#!/bin/bash
source configuration.sh

python2 plot_antennas.py \
    --ip    $(echo $ROACH_IP) 
    
