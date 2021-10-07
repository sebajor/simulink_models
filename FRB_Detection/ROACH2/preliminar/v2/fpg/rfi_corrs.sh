#!/bin/bash
source configuration.sh 

python codes/rfi_corrs.py \
    --ip $(echo $ROACH_IP) \
    --bof $(echo $BOF_FILE) \
    --acc $(echo $RFI_ACC) \
