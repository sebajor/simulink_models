#!/bin/bash
source configuration.sh

python codes/plot_rfi_rank.py \
    --ip $(echo $ROACH_IP) \
    --bof $(echo $BOF_FILE) \
    --acc $(echo $RFI_ACC) \
