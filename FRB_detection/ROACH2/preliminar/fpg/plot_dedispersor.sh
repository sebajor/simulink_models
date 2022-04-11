#!/bin/bash
source configuration.sh

python2 codes/plot_dedispersor.py \
    --ip    $(echo $ROACH_IP) \
    --DM    100 \

    
    
