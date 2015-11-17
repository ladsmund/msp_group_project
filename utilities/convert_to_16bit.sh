#!/bin/bash

# This will convert all .wav files in the current directory to 16 bit
# (it should prompt for each to overwrite since it's using the same filename)
for i in *.wav; do ffmpeg -v 1 -y -i $i -sample_fmt s16 $i; done
