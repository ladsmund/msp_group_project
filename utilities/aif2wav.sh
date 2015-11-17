#!/bin/bash
#FILES=$1

for i in *.aif; do ffmpeg -v 0 -i ${i} `echo ${i} | tr aif wav`; done

#for fullfile in $FILES
#do
#    filename=$(basename "$fullfile")
#    extension="${filename##*.}"
#    filename="${filename%.*}"
#    echo $filename
#    ffmpeg -v 0 -i $fullfile $filename".wav"
#done
 
