#!/bin/bash
source configuration.sh

plot_snapshots.py \
    --ip         192.168.1.12\
    --snapnames  adcsnap0 adcsnap1 adcsnap2 adcsnap3 \
    --dtype      ">i1" \
    --nsamples   200
