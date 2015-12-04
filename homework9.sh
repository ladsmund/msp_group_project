#!/bin/bash

scales=( PythagDodecaphonic Meantone12Tone EvenTempered )
inst=ScaleSynth
basefreq=528
speed=160
score=scores/mary.mscore

echo "Part 1"
echo "Playing \"Mary had a little lamb\"..."

for scale in ${scales[@]}; do 
    echo "with the $scale scale..."
    koshka/homework9.py -i "$inst $scale $basefreq" $score -s $speed
done


echo ""
echo "Part 2"
echo "Compare intervals between tuning systems"

echo "What is the difference in cents and Hz of the M3 interval of Pythag Dodecaphonic and Ptolemy?"
./koshka/homework9_scales.py PythagDodecaphonic PtolemyNaturalChromatic -i0 '4' -i1 '4' -f $basefreq

echo "What is the difference in cents and Hz of the whole tone (M2) of the Meantone and ET systems?"
./koshka/homework9_scales.py Meantone EvenTempered -i0 '2' -i1 '2' -f $basefreq

echo "What is the difference in cents and Hz of the fifth interval in ET and Ptolemy?"
./koshka/homework9_scales.py EvenTempered PtolemyNaturalChromatic -i0 '7' -i1 '7' -f $basefreq




