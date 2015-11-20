#!/bin/sh

echo "*****************"
echo "Run harness test"
python -m unittest discover -p *ptolemy* koshka/

echo "*****************"
echo "Play ptolemy scale"
./koshka/koshka.py scores/ptolemy_scale.txt --no_gui

echo "*****************"
echo "Play bembe wheel"
./koshka/koshka.py scores/bembe_wheel.txt --no_gui --loop 1