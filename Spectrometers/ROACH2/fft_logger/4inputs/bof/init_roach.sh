#!/bin/bash
source configuration.sh

python2 init_roach.py \
    --ip    $(echo $ROACH_IP)\
    --boffile $(echo $BOF_FILE)\
    --upload 

