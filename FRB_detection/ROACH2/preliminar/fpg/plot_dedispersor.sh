#!/bin/bash
source configuration.sh

python2 codes/plot_dedispersor.py \
    --ip    $(echo $ROACH_IP) \
    --DM    80 160 240 320 400 480

    
    
