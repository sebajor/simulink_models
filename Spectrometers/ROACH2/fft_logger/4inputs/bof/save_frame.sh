#!/bin/bash
source configuration.sh

python2 save_frame.py \
    --ip $(echo $ROACH_IP) \
    -f arte_tone.hdf5\
    -n 32