#!/bin/bash
plot_snapshots.py \
    --ip         192.168.1.12 \
    --upload      \
    --snapnames  adcsnap0 adcsnap1\
    --dtype      ">b" \
    --nsamples   200
