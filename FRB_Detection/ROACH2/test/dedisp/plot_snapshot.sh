#!/bin/bash
plot_snapshots.py \
    --ip         192.168.0.40 \
    `#--bof        reduce_spect.fpg` \
    --upload      \
    --snapnames  snapshot adcsnap1 \
    --dtype      ">b" \
    --nsamples   200
