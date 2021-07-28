#!/bin/bash
source configuration.sh

python rank2.py \
    --ip $(echo $ROACH_IP) \
    --bof $(echo $BOF_FILE) \
    --acc 1024 \
