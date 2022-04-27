#!/bin/bash
source configuration.sh

python2 plot_spectrum.py \
    --ip $(echo $ROACH_IP)
