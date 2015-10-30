#!/bin/bash 
FILES=$1

for fullfile in $FILES
do
    filename=$(basename "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo $filename
    ffmpeg -v 0 -i $fullfile $filename".wav"
done
 
