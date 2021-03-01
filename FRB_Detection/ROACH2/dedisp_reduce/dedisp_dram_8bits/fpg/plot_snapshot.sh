#!/bin/bash
plot_snapshots.py \
    --ip         192.168.1.14 \
    `#--bof        frb2_v3.fpg` \
    --upload      \
    --snapnames  snapshot adcsnap1 \
    --dtype      ">b" \
    --nsamples   200
