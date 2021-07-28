#!/bin/bash
source configuration.sh

python plot_antennas.py \
    --ip    $(echo $ROACH_IP) 
    
