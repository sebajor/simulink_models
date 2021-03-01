#!/bin/bash
plot_snapshots.py \
    --ip         192.168.1.14 \
    `#--bof        dedisp_sync.fpg` \
    --upload      \
    --snapnames  adcsnap0 \
    --dtype      ">i1" \
    --nsamples   200
