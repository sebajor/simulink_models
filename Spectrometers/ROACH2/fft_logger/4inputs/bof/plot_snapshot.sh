#!/bin/bash
source configuration.sh

plot_snapshots.py \
    --ip         $(ROACH_IP) 
    --upload      \
    --snapnames  adcsnap0 adcsnap1 adcsnap2 adcsnap3\
    --dtype      ">b" \
    --nsamples   200
