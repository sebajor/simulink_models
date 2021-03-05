#!/bin/bash
source configuration.sh
plot_snapshots.py \
    --ip         $(echo $ROACH_IP) \
    `#--bof      $(echo $BOF_FILE)` \
    --upload      \
    --snapnames  adcsnap0 \
    --dtype      ">b" \
    --nsamples   200
