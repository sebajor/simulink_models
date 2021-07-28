#!/bin/bash
source configuration.sh
python plot_ranking.py \
    --ip $(echo $ROACH_IP) \
    --bof $(echo $BOF_FILE) \
    --acc 1024 \
