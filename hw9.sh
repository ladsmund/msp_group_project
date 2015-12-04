#!/bin/bash

#scales=( PythagDodecaphonic Meantone EvenTempered )
scales=( Meantone EvenTempered )
inst=ScaleSynth
basefreq=528
score=scores/mary.mscore

echo "Playing \"Mary had a little lamb\"..."

for scale in ${scales[@]}; do 
    echo "with the $scale scale..."
    koshka/homework9.py -i "$inst $scale $basefreq" $score
done

